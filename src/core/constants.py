"""
Enumerations and constants.

Classes
-------
- Modes: Enumeration for modes.
    - Attributes:
        - LIGHT: Light mode.
        - DARK: Dark mode.

- ModeCheck: Enumeration for mode check results.
    - Attributes:
        - VOID: Represents a void flag.
        - SAME_MODE: Represents a flag of the same mode.
        - DIFFERENT_MODE: Represents a flag of a different mode.

- Unicodes: Enumeration for Unicode characters used in the state representation.
    - Attributes:
        - OUTLINED_MONOTONE: Outlined monotone Unicode character.
        - OUTLINE_PIVOT: Outline pivot Unicode character.
        - OUTLINED_SLOPE: Outlined slope Unicode character.
        - OUTLINED_STRIDE: Outlined stride Unicode character.
        - OUTLINED_RADIUS: Outlined radius Unicode character.
        - OUTLINED_ANCHOR: Outlined anchor Unicode character.
        - FILLED_MONOTONE: Filled monotone Unicode character.
        - FILLED_PIVOT: Filled pivot Unicode character.
        - FILLED_SLOPE: Filled slope Unicode character.
        - FILLED_STRIDE: Filled stride Unicode character.
        - FILLED_RADIUS: Filled radius Unicode character.
        - FILLED_ANCHOR: Filled anchor Unicode character.
        - VOID_UNICODE: Void Unicode character.
        - INVALID_UNICODE: Invalid Unicode character.

- Flags: Enumeration for flags used in the state representation.
    - Attributes:
        - VOID: Void flag.
        - LIGHT_MONOTONE: Light monotone flag.
        - LIGHT_PIVOT: Light pivot flag.
        - LIGHT_SLOPE: Light slope flag.
        - LIGHT_STRIDE: Light stride flag.
        - LIGHT_RADIUS: Light radius flag.
        - LIGHT_ANCHOR: Light anchor flag.
        - HORIZON: Horizon flag.
        - DARK_MONOTONE: Dark monotone flag.
        - DARK_PIVOT: Dark pivot flag.
        - DARK_SLOPE: Dark slope flag.
        - DARK_STRIDE: Dark stride flag.
        - DARK_RADIUS: Dark radius flag.
        - DARK_ANCHOR: Dark anchor flag.

- DebugModes: Enumeration for debug modes.
    - Attributes:
        - RELEASE: Release mode.
        - INNOVATION: Innovation mode.

Constants
---------
- FLAG2UNICODE: Mapping of flag values to Unicode characters.
- STORE_DIR: Directory where the store files are saved.
- HANDLER_DIR: Directory where the handler files are saved.
- QUEUE_DIR: Directory where the queue files are saved.
- FILE_EXTENSION: File extension for the stored files.
- MAX_QUEUE_SIZE: Maximum size of the queue in bytes.

Testing and QA
==============
Classes
-------
- TestConstants: Unit tests for the constants.
    - Methods:
        - test_modes_enum: Test the Modes enumeration values.
        - test_unicodes_enum: Test the Unicodes enumeration values.
        - test_flags_enum: Test the Flags enumeration values.
        - test_flag2unicode_mapping: Test the Flag2Unicode dictionary mapping.
"""
from enum import Enum
from os import getenv

class Modes(Enum):
    """
    Enumeration for modes.
    """
    LIGHT = 'light'
    DARK = 'dark'

class ModeCheck(Enum):
    """
    Enumeration for mode check results.
    """
    VOID = 0
    SAME_MODE = 1
    DIFFERENT_MODE = -1

class Unicodes(Enum):
    """
    Enumeration for Unicode characters used in the state representation.
    """
    OUTLINED_MONOTONE = '♙'
    OUTLINE_PIVOT = '♘'
    OUTLINED_SLOPE = '♗'
    OUTLINED_STRIDE = '♖'
    OUTLINED_RADIUS = '♕'
    OUTLINED_ANCHOR = '♔'

    FILLED_MONOTONE = '♟'
    FILLED_PIVOT = '♞'
    FILLED_SLOPE = '♝'
    FILLED_STRIDE = '♜'
    FILLED_RADIUS = '♛'
    FILLED_ANCHOR = '♚'

    VOID_UNICODE = '　'
    INVALID_UNICODE = '⁇'

class Flags(Enum):
    """
    Enumeration for flags used in the state representation.
    """
    VOID = 0x0

    LIGHT_MONOTONE = 0x1
    LIGHT_PIVOT = 0x2
    LIGHT_SLOPE = 0x3
    LIGHT_STRIDE = 0x4
    LIGHT_RADIUS = 0x5
    LIGHT_ANCHOR = 0x6

    HORIZON = 0x8

    DARK_MONOTONE = 0xA
    DARK_PIVOT = 0xB
    DARK_SLOPE = 0XC
    DARK_STRIDE = 0xD
    DARK_RADIUS = 0xE
    DARK_ANCHOR = 0xF

class DebugModes(Enum):
    """
    Enumeration for debug modes.
    """
    RELEASE = 'release'
    INNOVATION = 'innovation'

FLAG2UNICODE: dict[int, str] = {
    Flags.VOID.value: Unicodes.VOID_UNICODE.value,

    Flags.LIGHT_MONOTONE.value: Unicodes.OUTLINED_MONOTONE.value,
    Flags.LIGHT_PIVOT.value: Unicodes.OUTLINE_PIVOT.value,
    Flags.LIGHT_SLOPE.value: Unicodes.OUTLINED_SLOPE.value,
    Flags.LIGHT_STRIDE.value: Unicodes.OUTLINED_STRIDE.value,
    Flags.LIGHT_RADIUS.value: Unicodes.OUTLINED_RADIUS.value,
    Flags.LIGHT_ANCHOR.value: Unicodes.OUTLINED_ANCHOR.value,

    Flags.DARK_MONOTONE.value: Unicodes.FILLED_MONOTONE.value,
    Flags.DARK_PIVOT.value: Unicodes.FILLED_PIVOT.value,
    Flags.DARK_SLOPE.value: Unicodes.FILLED_SLOPE.value,
    Flags.DARK_STRIDE.value: Unicodes.FILLED_STRIDE.value,
    Flags.DARK_RADIUS.value: Unicodes.FILLED_RADIUS.value,
    Flags.DARK_ANCHOR.value: Unicodes.FILLED_ANCHOR.value,
}

STORE_DIR: str = '.store'
HANDLER_DIR: str = '.handlers'
QUEUE_DIR: str = '.queue'
FILE_EXTENSION: str = '.raw'

MAX_PROCESS_QUEUE: int = 8192
MAX_QUEUE_SIZE: int = MAX_PROCESS_QUEUE * 32

if getenv('DEBUGMODE') == DebugModes.INNOVATION.value:
    import unittest

    class TestConstants(unittest.TestCase):
        """
        Unit tests for the constants defined in this module.
        """

        def test_modes_enum(self):
            """
            Test the Modes enumeration values.
            """
            self.assertEqual(Modes.LIGHT.value, 'light')
            self.assertEqual(Modes.DARK.value, 'dark')

        def test_modecheck_enum(self):
            """
            Test the ModeCheck enumeration values.
            """
            self.assertEqual(ModeCheck.VOID.value, 0)
            self.assertEqual(ModeCheck.SAME_MODE.value, 1)
            self.assertEqual(ModeCheck.DIFFERENT_MODE.value, -1)

        def test_unicodes_enum(self):
            """
            Test the Unicodes enumeration values.
            """
            self.assertEqual(Unicodes.OUTLINED_MONOTONE.value, '♙')
            self.assertEqual(Unicodes.OUTLINE_PIVOT.value, '♘')
            self.assertEqual(Unicodes.OUTLINED_SLOPE.value, '♗')
            self.assertEqual(Unicodes.OUTLINED_STRIDE.value, '♖')
            self.assertEqual(Unicodes.OUTLINED_RADIUS.value, '♕')
            self.assertEqual(Unicodes.OUTLINED_ANCHOR.value, '♔')
            self.assertEqual(Unicodes.FILLED_MONOTONE.value, '♟')
            self.assertEqual(Unicodes.FILLED_PIVOT.value, '♞')
            self.assertEqual(Unicodes.FILLED_SLOPE.value, '♝')
            self.assertEqual(Unicodes.FILLED_STRIDE.value, '♜')
            self.assertEqual(Unicodes.FILLED_RADIUS.value, '♛')
            self.assertEqual(Unicodes.FILLED_ANCHOR.value, '♚')
            self.assertEqual(Unicodes.VOID_UNICODE.value, '　')
            self.assertEqual(Unicodes.INVALID_UNICODE.value, '⁇')

        def test_flags_enum(self):
            """
            Test the Flags enumeration values.
            """
            self.assertEqual(Flags.VOID.value, 0x0)
            self.assertEqual(Flags.LIGHT_MONOTONE.value, 0x1)
            self.assertEqual(Flags.LIGHT_PIVOT.value, 0x2)
            self.assertEqual(Flags.LIGHT_SLOPE.value, 0x3)
            self.assertEqual(Flags.LIGHT_STRIDE.value, 0x4)
            self.assertEqual(Flags.LIGHT_RADIUS.value, 0x5)
            self.assertEqual(Flags.LIGHT_ANCHOR.value, 0x6)
            self.assertEqual(Flags.HORIZON.value, 0x8)
            self.assertEqual(Flags.DARK_MONOTONE.value, 0xA)
            self.assertEqual(Flags.DARK_PIVOT.value, 0xB)
            self.assertEqual(Flags.DARK_SLOPE.value, 0xC)
            self.assertEqual(Flags.DARK_STRIDE.value, 0xD)
            self.assertEqual(Flags.DARK_RADIUS.value, 0xE)
            self.assertEqual(Flags.DARK_ANCHOR.value, 0xF)

        def test_flag2unicode_mapping(self):
            """
            Test the Flag2Unicode dictionary mapping.
            """
            self.assertEqual(FLAG2UNICODE[Flags.VOID.value], Unicodes.VOID_UNICODE.value)
            self.assertEqual(FLAG2UNICODE[Flags.LIGHT_MONOTONE.value], Unicodes.OUTLINED_MONOTONE.value)
            self.assertEqual(FLAG2UNICODE[Flags.LIGHT_PIVOT.value], Unicodes.OUTLINE_PIVOT.value)
            self.assertEqual(FLAG2UNICODE[Flags.LIGHT_SLOPE.value], Unicodes.OUTLINED_SLOPE.value)
            self.assertEqual(FLAG2UNICODE[Flags.LIGHT_STRIDE.value], Unicodes.OUTLINED_STRIDE.value)
            self.assertEqual(FLAG2UNICODE[Flags.LIGHT_RADIUS.value], Unicodes.OUTLINED_RADIUS.value)
            self.assertEqual(FLAG2UNICODE[Flags.LIGHT_ANCHOR.value], Unicodes.OUTLINED_ANCHOR.value)
            self.assertEqual(FLAG2UNICODE[Flags.DARK_MONOTONE.value], Unicodes.FILLED_MONOTONE.value)
            self.assertEqual(FLAG2UNICODE[Flags.DARK_PIVOT.value], Unicodes.FILLED_PIVOT.value)
            self.assertEqual(FLAG2UNICODE[Flags.DARK_SLOPE.value], Unicodes.FILLED_SLOPE.value)
            self.assertEqual(FLAG2UNICODE[Flags.DARK_STRIDE.value], Unicodes.FILLED_STRIDE.value)
            self.assertEqual(FLAG2UNICODE[Flags.DARK_RADIUS.value], Unicodes.FILLED_RADIUS.value)
            self.assertEqual(FLAG2UNICODE[Flags.DARK_ANCHOR.value], Unicodes.FILLED_ANCHOR.value)

        def test_constants(self):
            """
            Test the constants values.
            """
            self.assertEqual(STORE_DIR, '.store')
            self.assertEqual(HANDLER_DIR, '.handlers')
            self.assertEqual(QUEUE_DIR, '.queue')
            self.assertEqual(FILE_EXTENSION, '.raw')
            self.assertEqual(MAX_QUEUE_SIZE, 1024 * 1024)

    if __name__ == '__main__':
        unittest.main()
