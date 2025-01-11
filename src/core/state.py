"""
Modes, Unicodes, Flags, State and interface for encoding and decoding states.

Classes
=======
  - Modes
  - Unicodes
  - Flags
  - State

State
=====
Attributes
  - state
Methods
  - __init__
  - to_matrix
  - from_matrix
  - to_hex
  - from_hex
  - to_str
  - __str__
"""
from enum import Enum
import numpy as np


class Modes(Enum):
    Light = 'light'
    Dark = 'dark'


class Unicodes(Enum):
    Outlined_Monotone = '♙'
    Outlined_Pivot = '♘'
    Outlined_Slope = '♗'
    Outlined_Stride = '♖'
    Outlined_Radius = '♕'
    Outlined_Anchor = '♔'

    Filled_Monotone = '♟'
    Filled_Pivot = '♞'
    Filled_Slope = '♝'
    Filled_Stride = '♜'
    Filled_Radius = '♛'
    Filled_Anchor = '♚'

    Void_Unicode = '　'
    Invalid_Unicode = '⁇'


class Flags(Enum):
    Void = 0x0

    Light_Monotone = 0x1
    Light_Pivot = 0x2
    Light_Slope = 0x3
    Light_Stride = 0x4
    Light_Radius = 0x5
    Light_Anchor = 0x6

    Horizon = 0x8

    Dark_Monotone = 0xA
    Dark_Pivot = 0xB
    Dark_Slope = 0XC
    Dark_Stride = 0xD
    Dark_Radius = 0xE
    Dark_Anchor = 0xF


Flag2Unicode = {
    Flags.Void.value: Unicodes.Void_Unicode.value,

    Flags.Light_Monotone.value: Unicodes.Outlined_Monotone.value,
    Flags.Light_Pivot.value: Unicodes.Outlined_Pivot.value,
    Flags.Light_Slope.value: Unicodes.Outlined_Slope.value,
    Flags.Light_Stride.value: Unicodes.Outlined_Stride.value,
    Flags.Light_Radius.value: Unicodes.Outlined_Radius.value,
    Flags.Light_Anchor.value: Unicodes.Outlined_Anchor.value,

    Flags.Dark_Monotone.value: Unicodes.Filled_Monotone.value,
    Flags.Dark_Pivot.value: Unicodes.Filled_Pivot.value,
    Flags.Dark_Slope.value: Unicodes.Filled_Slope.value,
    Flags.Dark_Stride.value: Unicodes.Filled_Stride.value,
    Flags.Dark_Radius.value: Unicodes.Filled_Radius.value,
    Flags.Dark_Anchor.value: Unicodes.Filled_Anchor.value,
}


class State:
    def __init__(self) -> None:
        """
        New instance of State
        """
        self.state = np.empty((32,), dtype=np.uint8)

    def to_matrix(self) -> np.ndarray:
        """
        Converts State into a 64-element uint8 matrix
        :return: np.ndarray: A 2D numpy array of shape (8, 8) and dtype uint8
        """
        matrix = np.empty((64,), dtype=np.uint8)
        for idx in range(32):
            byte = self.state[idx]
            matrix[idx * 2] = (byte & 0xF0) >> 4
            matrix[idx * 2 + 1] = byte & 0x0F
        return matrix.reshape((8, 8))

    def from_matrix(self, matrix: np.ndarray) -> 'State':
        """
        Load State from a 64-element uint8 matrix
        :param matrix: np.ndarray: A 2D numpy array of shape (8, 8) and dtype uint8
        :return: State: The state object itself
        """
        flat_matrix = matrix.flatten()
        for idx in range(32):
            self.state[idx] = (flat_matrix[idx * 2] << 4) | flat_matrix[idx * 2 + 1]
        return self

    def to_hex(self) -> str:
        """
        Convert the 32-byte State to a hex string representation of 64 hex characters.
        :return: str: A string of 64 hex characters representing the State.
        """
        return ''.join(f'{byte:02x}' for byte in self.state)

    def from_hex(self, hex_str: str) -> 'State':
        """
        Converts a 64-character hex string into a 32-byte State.
        :param hex_str: str: A string of 64 hex characters.
        :return: State: The state object itself.
        """
        for idx in range(32):
            byte_pair = hex_str[idx * 2: idx * 2 + 2]
            self.state[idx] = int(byte_pair, 16)

        return self

    def to_str(self) -> str:
        """
        String representation of the state
        :return: String representation of the state
        """
        matrix = self.to_matrix()
        state_str = ''
        for row in matrix:
            for cell in row:
                symbol = Flag2Unicode.get(cell, Unicodes.Invalid_Unicode.value)
                state_str += symbol
            state_str += '\n'
        return state_str

    def __str__(self) -> str:
        """
        String representation of the state
        :return: String representation of the state
        """
        return self.to_str()


if __name__ == '__main__':
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

    # Create instance of State and load standard state
    state = State()
    state.from_matrix(matrix=init_state)

    # Print various representations of state
    print(state.state)
    print(state.to_matrix())
    print(state.to_hex())
    print(state.to_str())
