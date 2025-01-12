"""
Main file, driver code
"""
from os import path
import numpy as np
from src.core.constants import Flags, STORE_DIR
from src.core.state import State
from src.core.handler import Handler
from src.core.store import pack, process_queue

if path.exists(STORE_DIR):
    process_queue(True)
    process_queue(False)
else:
    # Standard state
    init_state = np.array([
        [
            Flags.DARK_STRIDE.value,
            Flags.DARK_PIVOT.value,
            Flags.DARK_SLOPE.value,
            Flags.DARK_ANCHOR.value,
            Flags.DARK_RADIUS.value,
            Flags.DARK_SLOPE.value,
            Flags.DARK_PIVOT.value,
            Flags.DARK_STRIDE.value,
        ],
        [Flags.DARK_MONOTONE.value] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [Flags.LIGHT_MONOTONE.value] * 8,
        [
            Flags.LIGHT_STRIDE.value,
            Flags.LIGHT_PIVOT.value,
            Flags.LIGHT_SLOPE.value,
            Flags.LIGHT_RADIUS.value,
            Flags.LIGHT_ANCHOR.value,
            Flags.LIGHT_SLOPE.value,
            Flags.LIGHT_PIVOT.value,
            Flags.LIGHT_STRIDE.value,
        ],
    ], dtype=np.uint8)
    init_state_hex_str = State().from_matrix(matrix=init_state).to_hex()

    # Create instance of Handler and load standard state
    handler = Handler(dark_mode=False, hex_str=init_state_hex_str)
    pack(handler)
