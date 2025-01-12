"""
States and interface for encoding and decoding states.

Classes
-------
- State: Represents the state of the system with methods to convert between different representations.
    - Attributes:
        - state: The internal state represented as a numpy array.
    - Methods:
        - __init__: Initializes a new instance of State.
        - to_matrix: Converts State into a 64-element uint8 matrix.
        - from_matrix: Loads State from a 64-element uint8 matrix.
        - to_hex: Converts the 32-byte State to a hex string representation of 64 hex characters.
        - from_hex: Converts a 64-character hex string into a 32-byte State.
        - to_str: Returns a string representation of the state.
        - __str__: Returns a string representation of the state.

Testing and QA
==============
Classes
-------
- TestState: Unit tests for the State class.
    - Methods:
        - setUp: Sets up the test case environment.
        - test_to_matrix: Tests the to_matrix method.
        - test_from_matrix: Tests the from_matrix method.
        - test_to_hex: Tests the to_hex method.
        - test_from_hex: Tests the from_hex method.
        - test_to_str: Tests the to_str method.
"""
from os import getenv
import numpy as np
from .constants import FLAG2UNICODE, Unicodes, DebugModes

class State:
    """
    Represents the state of the system with methods to convert between different representations.
    """
    def __init__(self):
        """
        Initializes a new instance of State.
        """
        self.state = np.empty((32,), dtype=np.uint8)

    def to_matrix(self) -> np.ndarray:
        """
        Converts State into a 64-element uint8 matrix.

        Returns
        -------
        np.ndarray
            A 2D numpy array of shape (8, 8) and dtype uint8.
        """
        matrix = np.empty((64,), dtype=np.uint8)
        for idx in range(32):
            byte = self.state[idx]
            matrix[idx * 2] = (byte & 0xF0) >> 4
            matrix[idx * 2 + 1] = byte & 0x0F
        return matrix.reshape((8, 8))

    def from_matrix(self, matrix: np.ndarray) -> 'State':
        """
        Loads State from a 64-element uint8 matrix.

        Parameters
        ----------
        matrix : np.ndarray
            A 2D numpy array of shape (8, 8) and dtype uint8.

        Returns
        -------
        State
            The state object itself.
        """
        flat_matrix = matrix.flatten()
        for idx in range(32):
            self.state[idx] = (flat_matrix[idx * 2] << 4) | flat_matrix[idx * 2 + 1]
        return self

    def to_hex(self) -> str:
        """
        Converts the 32-byte State to a hex string representation of 64 hex characters.

        Returns
        -------
        str
            A string of 64 hex characters representing the State.
        """
        return ''.join(f'{byte:02x}' for byte in self.state)

    def from_hex(self, hex_str: str) -> 'State':
        """
        Converts a 64-character hex string into a 32-byte State.

        Parameters
        ----------
        hex_str : str
            A string of 64 hex characters.

        Returns
        -------
        State
            The state object itself.
        """
        for idx in range(32):
            byte_pair = hex_str[idx * 2: idx * 2 + 2]
            self.state[idx] = int(byte_pair, 16)
        return self

    def to_str(self) -> str:
        """
        Returns a string representation of the state.

        Returns
        -------
        str
            String representation of the state.
        """
        matrix = self.to_matrix()
        state_str = ''
        for row in matrix:
            for cell in row:
                symbol = FLAG2UNICODE.get(cell, Unicodes.INVALID_UNICODE.value)
                state_str += symbol
            state_str += '\n'
        return state_str

    def __str__(self) -> str:
        """
        Returns a string representation of the state.

        Returns
        -------
        str
            String representation of the state.
        """
        return self.to_str()

if getenv('DEBUGMODE') == DebugModes.INNOVATION.value:
    import unittest

    class TestState(unittest.TestCase):
        """
        Unit tests for the State class.
        """

        def setUp(self):
            """
            Sets up the test case environment.
            """
            self.state = State()

        def test_to_matrix(self):
            """
            Tests the to_matrix method.
            """
            self.state.state = np.array([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0] * 4, dtype=np.uint8)
            expected_matrix = np.array([
                [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8],
                [0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0x0],
                [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8],
                [0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0x0],
                [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8],
                [0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0x0],
                [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8],
                [0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0x0],
            ], dtype=np.uint8)
            np.testing.assert_array_equal(self.state.to_matrix(), expected_matrix)

        def test_from_matrix(self):
            """
            Tests the from_matrix method.
            """
            matrix = np.array([
                [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8],
                [0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0x0],
                [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8],
                [0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0x0],
                [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8],
                [0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0x0],
                [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8],
                [0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0x0],
            ], dtype=np.uint8)
            expected_state = np.array([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0] * 4, dtype=np.uint8)
            self.state.from_matrix(matrix)
            np.testing.assert_array_equal(self.state.state, expected_state)

        def test_to_hex(self):
            """
            Tests the to_hex method.
            """
            self.state.state = np.array([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0] * 4, dtype=np.uint8)
            expected_hex = '123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0'
            self.assertEqual(self.state.to_hex(), expected_hex)

        def test_from_hex(self):
            """
            Tests the from_hex method.
            """
            hex_str = '123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0'
            expected_state = np.array([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0] * 4, dtype=np.uint8)
            self.state.from_hex(hex_str)
            np.testing.assert_array_equal(self.state.state, expected_state)

        def test_to_str(self):
            """
            Tests the to_str method.
            """
            self.state.state = np.array([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0] * 4, dtype=np.uint8)
            expected_str = (
                '♙♘♗♖♕♔⁇⁇\n'
                '⁇♟♞♝♜♛♚　\n'
                '♙♘♗♖♕♔⁇⁇\n'
                '⁇♟♞♝♜♛♚　\n'
                '♙♘♗♖♕♔⁇⁇\n'
                '⁇♟♞♝♜♛♚　\n'
                '♙♘♗♖♕♔⁇⁇\n'
                '⁇♟♞♝♜♛♚　\n'
            )
            self.assertEqual(self.state.to_str(), expected_str)

    if __name__ == '__main__':
        unittest.main()
