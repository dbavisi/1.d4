"""
Utility for packing and unpacking states and handlers
"""
from os import path, mkdir, replace
try:
    from .core.state import Modes, Flags, State
    from .core.handler import Handler
except Exception as exp:
    print(str(exp))
    from core.state import Modes, Flags, State
    from core.handler import Handler

root_dir = '..'
store_dir = path.join(root_dir, '.store')


def pack(handler: Handler):
    mode_dir = path.join(store_dir,
                         Modes.Dark.value if handler.dark_mode else Modes.Light.value)
    alt_mode_dir = path.join(store_dir,
                             Modes.Light.value if handler.dark_mode else Modes.Dark.value)
    file_name = path.join(mode_dir, handler.state.to_hex() + '.raw')
    queue_file_name = path.join(alt_mode_dir, 'queue.raw')

    if not path.exists(store_dir):
        mkdir(store_dir)
    if not path.exists(mode_dir):
        mkdir(mode_dir)
    if not path.exists(alt_mode_dir):
        mkdir(alt_mode_dir)

    if path.exists(file_name) and path.isfile(file_name):
        return

    with open(queue_file_name, 'ab+') as queue:
        with open(file_name, 'wb') as store:
            for (horizon, axis), possible_rules in handler.all_possible_rules():
                source = (horizon << 4) | axis
                source_matrix = handler.matrix.copy()
                flag = source_matrix[7 - horizon][axis]
                source_matrix[7 - horizon][axis] = Flags.Void.value

                for (new_horizon, new_axis) in possible_rules:
                    destination = (new_horizon << 4) | new_axis
                    new_matrix = source_matrix.copy()
                    new_matrix[7 - new_horizon][new_axis] = flag

                    new_state = State().from_matrix(new_matrix)
                    new_state_bytes = new_state.state.tobytes()

                    store.write(bytes([0x78, source, destination]))
                    store.write(new_state_bytes)

                    new_state_hex_str = new_state.to_hex()
                    new_state_file_name = path.join(alt_mode_dir, new_state_hex_str + '.raw')
                    if not path.exists(new_state_file_name):
                        queue.write(new_state_bytes)


def process_queue(dark_mode: bool, batch_size=500):
    mode_dir = path.join(store_dir,
                         Modes.Dark.value if dark_mode else Modes.Light.value)
    queue_file_name = path.join(mode_dir, 'queue.raw')
    temp_file_name = path.join(mode_dir, 'queue.temp.raw')

    if not path.exists(queue_file_name) or not path.isfile(queue_file_name):
        return

    count = 0
    with open(temp_file_name, 'wb') as temp_queue:
        with open(queue_file_name, 'rb') as queue:
            while True:
                if count < batch_size:
                    state = queue.read(32)
                    if not state:
                        break
                    handler = Handler(dark_mode, from_bytes=state)
                    pack(handler)
                    count += 1
                else:
                    break

            temp_queue.write(queue.read())
    replace(temp_file_name, queue_file_name)


if __name__ == '__main__':
    import numpy as np

    # Standard state
    init_state = np.array([
        [
            Flags.Dark_Stride.value,
            Flags.Dark_Pivot.value,
            Flags.Dark_Slope.value,
            Flags.Dark_Anchor.value,
            Flags.Dark_Radius.value,
            Flags.Dark_Slope.value,
            Flags.Dark_Pivot.value,
            Flags.Dark_Stride.value,
        ],
        [Flags.Dark_Monotone.value] * 4 + [0] * 4,
        [0] * 8,
        [0] * 4 + [Flags.Dark_Monotone.value] * 4,
        [Flags.Light_Monotone.value] * 8,
        [0] * 8,
        [0] * 8,
        [
            Flags.Light_Stride.value,
            Flags.Light_Pivot.value,
            Flags.Light_Slope.value,
            Flags.Light_Radius.value,
            Flags.Light_Anchor.value,
            Flags.Light_Slope.value,
            Flags.Light_Pivot.value,
            Flags.Light_Stride.value,
        ],
    ], dtype=np.uint8)
    init_state_hex_str = State().from_matrix(matrix=init_state).to_hex()

    # Create instance of Handler and load standard state
    handler = Handler(dark_mode=False, hex_str=init_state_hex_str)

    print(handler.state)
    pack(handler)

    handler.dark_mode = True
    pack(handler)

    process_queue(False, batch_size=5)
    process_queue(True, batch_size=10)