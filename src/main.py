"""
Main file, driver code
"""
from os import path
import numpy as np
try:
    from .core.state import Flags, State
    from .core.handler import Handler
    from .pack import pack, process_queue
except Exception as exp:
    print(str(exp))
    from core.state import Flags, State
    from core.handler import Handler
    from pack import pack, process_queue

if path.exists('.store'):
    process_queue(True)
    process_queue(False)
else:
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
        [Flags.Dark_Monotone.value] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [Flags.Light_Monotone.value] * 8,
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
    pack(handler)
