"""
Utility functions and classes for logging and directory management.

Classes
-------
- DirectoryTrie: A trie-like structure for storing and checking directory paths.
    - Attributes:
        - root: Root node of the trie.
    - Methods:
        - insert: Inserts a directory path into the trie.
        - exists: Checks if a directory path exists in the trie.

Functions
---------
- check_and_create_path: Checks and creates the specified path if it does not exist.
- buglog: Synchronous and multi-threaded debug logger method.
"""
import sys
from queue import Queue
from os import path, makedirs, getenv
from logging import Formatter, StreamHandler, getLogger, DEBUG
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from datetime import datetime
from .constants import DebugModes, MAX_LOG_SIZE

class DirectoryTrie:
    """
    A trie-like structure for storing and checking directory paths.
    """
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

log_queue = Queue()
logform = '%(asctime)s %(filename)s:%(lineno)d %(message)s'

if getenv('DEBUGMODE') != DebugModes.INNOVATION.value:
    handler = StreamHandler(sys.stdout)
else:
    timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    bugfile = path.join('.buglog', f'buglog_{timestamp}.log')
    check_and_create_path('.buglog')
    handler = RotatingFileHandler(bugfile, maxBytes=MAX_LOG_SIZE, backupCount=10)

handler.setFormatter(Formatter(logform))
queue_handler = QueueHandler(log_queue)
queue_listener = QueueListener(log_queue, handler)
queue_listener.start()

logger = getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(queue_handler)
buglog = logger.debug
