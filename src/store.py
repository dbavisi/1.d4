"""
Utility for packing and unpacking states and handlers, and managing directory paths.

Functions
---------
- ensure_directories_exist: Ensures that the specified directories exist.
- write_state_to_store: Writes the state information to the store file.
- partitioned_filename: Returns a partitioned filename by splitting the hex string into groups of 16 characters.
- pack: Packs the handler's state and possible rules into files.
- process_queue: Processes the queue of states for a given mode.
- check_and_create_path: Checks and creates the specified path if it does not exist.

Classes
-------
- QueueController: Manages the queue of states.
    - Attributes:
        - parent_dir: The parent directory for the queue files.
        - max_size: Maximum size of the queue in bytes.
        - active_writer_name: Name of the active writer file.
        - active_writer: Active writer file object.
        - active_writer_size: Size of the active writer file.
        - active_reader_name: Name of the active reader file.
        - active_reader: Active reader file object.
        - active_reader_index: Index of the active reader file.
        - queue_files: List of queue files.
        - usage_count: Usage count of the queue controller.
    - Methods:
        - generate_queue_dir: Generates the queue directory path.
        - generate_file_name: Generates a file name for the queue.
        - __enter__: Enters the context manager.
        - __exit__: Exits the context manager.
        - next_writer: Switches to the next writer file.
        - next_reader: Switches to the next reader file.
        - write: Writes data to the queue.
        - read: Reads data from the queue.

- DirectoryTrie: A trie-like structure for storing and checking directory paths.
    - Attributes:
        - root: Root node of the trie.
    - Methods:
        - insert: Inserts a directory path into the trie.
        - exists: Checks if a directory path exists in the trie.
"""
from os import path, listdir, makedirs, replace, remove, getenv
import time
from .core.constants import (
    Modes, Flags, DebugModes,
    STORE_DIR, HANDLER_DIR, QUEUE_DIR, FILE_EXTENSION,
    MAX_PROCESS_QUEUE, MAX_QUEUE_SIZE
)
from .core.state import State
from .core.handler import Handler

# DirectoryTrie class
class DirectoryTrie:
    def __init__(self):
        self.root = {}

    def insert(self, directory_path):
        parts = directory_path.split(path.sep)
        node = self.root
        for part in parts:
            if part not in node:
                node[part] = {}
            node = node[part]

    def exists(self, directory_path):
        parts = directory_path.split(path.sep)
        node = self.root
        for part in parts:
            if part not in node:
                return False
            node = node[part]
        return True

directory_trie = DirectoryTrie()

# QueueController class
class QueueController:
    def __init__(self, parent_dir, max_size=MAX_QUEUE_SIZE):
        self.parent_dir = parent_dir
        self.max_size = max_size

        self.active_writer_name = None
        self.active_writer = None
        self.active_writer_size = 0

        self.active_reader_name = None
        self.active_reader = None
        self.active_reader_index = -1

        self.queue_files: list[str] = []
        self.usage_count = 0

    @staticmethod
    def generate_queue_dir(dark_mode):
        return path.join(STORE_DIR, Modes.DARK.value if dark_mode else Modes.LIGHT.value, QUEUE_DIR)

    @staticmethod
    def generate_file_name(parent_dir, temp=False):
        prefix = 'temp_' if temp else 'queue_'
        return path.join(parent_dir, f'{prefix}{int(time.time())}{FILE_EXTENSION}')

    def __enter__(self):
        self.usage_count += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.usage_count -= 1
        if self.usage_count == 0:
            if self.active_writer:
                self.active_writer.close()
            if self.active_reader:
                temp_queue_name = self.generate_file_name(self.parent_dir, temp=True)
                with open(temp_queue_name, 'wb') as temp_queue:
                    temp_queue.write(self.active_reader.read())
                self.active_reader.close()
                replace(temp_queue_name, self.active_reader_name)

    def next_writer(self):
        if self.active_writer:
            self.active_writer.close()

        self.active_writer_size = 0
        self.active_writer_name = self.generate_file_name(self.parent_dir)

        self.active_writer = open(self.active_writer_name, 'wb')

    def next_reader(self):
        if self.active_reader:
            self.active_reader.close()
            remove(self.active_reader_name)

        self.active_reader_index += 1
        self.active_reader = None

        if len(self.queue_files) == 0:
            self.queue_files = sorted(path.join(self.parent_dir, f) for f in listdir(self.parent_dir))
            print(f"Queue files: {self.queue_files}")

        if self.active_reader_index < len(self.queue_files):
            self.active_reader_name = self.queue_files[self.active_reader_index]
            self.active_reader = open(self.active_reader_name, 'rb')

    def write(self, data):
        if self.active_writer is None:
            self.next_writer()
        if self.active_writer_size >= self.max_size:
            self.next_writer()
        self.active_writer.write(data)
        self.active_writer_size += len(data)

    def read(self, batch_size):
        if self.active_reader is None:
            self.next_reader()
        while True:
            if self.active_reader is None:
                return
            data = self.active_reader.read(batch_size)
            if not data:
                self.next_reader()
                continue
            yield data

# Functions
def check_and_create_path(path_to_check: str, is_file: bool = False, create_dir: bool = False) -> bool:
    """
    Checks and creates the specified path if it does not exist.

    Parameters
    ----------
    path_to_check : str
        The path to check.
    is_file : bool, optional
        Whether the path is a file, by default False.
    create_dir : bool, optional
        Whether to create the directory if it does not exist, by default False.

    Returns
    -------
    bool
        True if the path exists or was created, False otherwise.
    """
    if not directory_trie.exists(path_to_check):
        if not path.exists(path_to_check):
            if is_file:
                if create_dir:
                    dir_name = path.dirname(path_to_check)
                    makedirs(dir_name, exist_ok=True)
                    directory_trie.insert(dir_name)
                return False
            else:
                makedirs(path_to_check, exist_ok=True)
                directory_trie.insert(path_to_check)
        else:
            directory_trie.insert(path_to_check)
    return True

def write_state_to_store(store, source: int, destination: int, new_state_bytes: bytes) -> None:
    """
    Writes the state information to the store file.

    Parameters
    ----------
    store : file object
        The file object to write to.
    source : int
        The source identifier.
    destination : int
        The destination identifier.
    new_state_bytes : bytes
        The state information in bytes.
    """
    store.write(bytes([0x78, source, destination]))
    store.write(new_state_bytes)

def partitioned_filename(parent_dir: str, hex_str: str) -> str:
    """
    Returns a partitioned filename by splitting the hex string into groups of 16 characters.

    Parameters
    ----------
    parent_dir : str
        The parent directory.
    hex_str : str
        The hex string to partition.

    Returns
    -------
    str
        The partitioned filename.
    """
    step = 8
    parts = [hex_str[i:i + step] for i in range(0, len(hex_str) - 2 * step, step)]
    return path.join(parent_dir, *parts, hex_str + FILE_EXTENSION)

def pack(handler: Handler, qc: QueueController = None) -> bool:
    """
    Packs the handler's state and possible rules into files.

    Parameters
    ----------
    handler : Handler
        The handler object.
    qc : QueueController, optional
        The queue controller, by default None.

    Returns
    -------
    bool
        True if the entry was processed, False otherwise.
    """
    mode_dir = path.join(STORE_DIR, Modes.DARK.value if handler.dark_mode else Modes.LIGHT.value, HANDLER_DIR)
    alt_mode_dir = path.join(STORE_DIR, Modes.LIGHT.value if handler.dark_mode else Modes.DARK.value, HANDLER_DIR)
    file_name = partitioned_filename(mode_dir, handler.state.to_hex())

    check_and_create_path(mode_dir)
    check_and_create_path(alt_mode_dir)

    if check_and_create_path(file_name, is_file=True, create_dir=True):
        print(f"Found pack: {file_name}")
        return False

    if qc is None:
        alt_queue_dir = QueueController.generate_queue_dir(not handler.dark_mode)
        check_and_create_path(alt_queue_dir, create_dir=True)
        qc = QueueController(alt_queue_dir)

    with qc, open(file_name, 'wb') as store:
        for (horizon, axis), possible_rules in handler.all_possible_rules():
            source = (horizon << 4) | axis
            source_matrix = handler.matrix.copy()
            flag = source_matrix[7 - horizon][axis]
            source_matrix[7 - horizon][axis] = Flags.VOID.value

            for (new_horizon, new_axis) in possible_rules:
                destination = (new_horizon << 4) | new_axis
                new_matrix = source_matrix.copy()
                new_matrix[7 - new_horizon][new_axis] = flag

                new_state = State().from_matrix(new_matrix)
                new_state_bytes = new_state.state.tobytes()

                write_state_to_store(store, source, destination, new_state_bytes)

                new_state_hex_str = new_state.to_hex()
                new_state_file_name = partitioned_filename(alt_mode_dir, new_state_hex_str)

                if not check_and_create_path(new_state_file_name, is_file=True):
                    qc.write(new_state_bytes)
                    # print(f"Enqueued: {new_state_file_name}")
                else:
                    print(f"Skipped re-pack: {new_state_file_name}")
    return True

def process_queue(dark_mode: bool, batch_size: int = MAX_PROCESS_QUEUE) -> None:
    """
    Processes the queue of states for a given mode.

    Parameters
    ----------
    dark_mode : bool
        Whether to process the queue in dark mode.
    batch_size : int, optional
        The batch size, by default MAX_PROCESS_QUEUE.
    """
    queue_dir = QueueController.generate_queue_dir(dark_mode)
    alt_queue_dir = QueueController.generate_queue_dir(not dark_mode)

    check_and_create_path(queue_dir)
    check_and_create_path(alt_queue_dir)

    with QueueController(queue_dir) as qc, QueueController(alt_queue_dir) as alt_qc:
        count = 0
        for state in qc.read(32):
            if count >= batch_size:
                break
            handler = Handler(dark_mode, from_bytes=state)
            if pack(handler, alt_qc):
                count += 1

if getenv('DEBUGMODE') == DebugModes.INNOVATION.value:
    if __name__ == '__main__':
        import numpy as np

        init_state = np.array([
            [
                Flags.DARK_STRIDE.value,
                Flags.DARK_PIVOT.value,
                Flags.DARK_SLOPE.value,
                0,
                Flags.DARK_RADIUS.value,
                Flags.DARK_SLOPE.value,
                Flags.DARK_PIVOT.value,
                Flags.DARK_STRIDE.value,
            ],
            [Flags.DARK_MONOTONE.value] * 4 + [0] * 4,
            [0, Flags.DARK_ANCHOR.value, 0, 0, Flags.LIGHT_ANCHOR.value, 0, 0, 0],
            [0] * 4 + [Flags.DARK_MONOTONE.value] * 4,
            [Flags.LIGHT_MONOTONE.value] * 8,
            [0] * 8,
            [0] * 8,
            [
                Flags.LIGHT_STRIDE.value,
                Flags.LIGHT_PIVOT.value,
                Flags.LIGHT_SLOPE.value,
                Flags.LIGHT_RADIUS.value,
                0,
                Flags.LIGHT_SLOPE.value,
                Flags.LIGHT_PIVOT.value,
                Flags.LIGHT_STRIDE.value,
            ],
        ], dtype=np.uint8)
        init_state_hex_str = State().from_matrix(matrix=init_state).to_hex()

        handler = Handler(dark_mode=False, hex_str=init_state_hex_str)

        print(handler.state)
        pack(handler)

        handler.dark_mode = True
        pack(handler)

        process_queue(False, batch_size=5)
        process_queue(True, batch_size=10)
