"""
Modes, Unicodes, Flags, and DebugModes.

Classes
-------
- Modes: Enumeration for modes.
- Unicodes: Enumeration for Unicode characters used in the state representation.
- Flags: Enumeration for flags used in the state representation.
- DebugModes: Enumeration for debug modes.

Dictionaries
------------
- Flag2Unicode: Mapping of flag values to Unicode characters.

Modes
-----
- Attributes
    - Light: Light mode.
    - Dark: Dark mode.

Unicodes
--------
- Attributes
    - Outlined_Monotone: Unicode for outlined monotone.
    - Outlined_Pivot: Unicode for outlined pivot.
    - Outlined_Slope: Unicode for outlined slope.
    - Outlined_Stride: Unicode for outlined stride.
    - Outlined_Radius: Unicode for outlined radius.
    - Outlined_Anchor: Unicode for outlined anchor.
    - Filled_Monotone: Unicode for filled monotone.
    - Filled_Pivot: Unicode for filled pivot.
    - Filled_Slope: Unicode for filled slope.
    - Filled_Stride: Unicode for filled stride.
    - Filled_Radius: Unicode for filled radius.
    - Filled_Anchor: Unicode for filled anchor.
    - Void_Unicode: Unicode for void.
    - Invalid_Unicode: Unicode for invalid.

Flags
-----
- Attributes
    - Void: Void flag.
    - Light_Monotone: Light monotone flag.
    - Light_Pivot: Light pivot flag.
    - Light_Slope: Light slope flag.
    - Light_Stride: Light stride flag.
    - Light_Radius: Light radius flag.
    - Light_Anchor: Light anchor flag.
    - Horizon: Horizon flag.
    - Dark_Monotone: Dark monotone flag.
    - Dark_Pivot: Dark pivot flag.
    - Dark_Slope: Dark slope flag.
    - Dark_Stride: Dark stride flag.
    - Dark_Radius: Dark radius flag.
    - Dark_Anchor: Dark anchor flag.

DebugModes
----------
- Attributes
    - Release: Release mode.
    - Innovation: Innovation mode.

Testing and QA
==============
Classes
-------
- TestConstants: Unit tests for the constants.

TestConstants
-------------
- Methods
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
    Light = 'light'
    Dark = 'dark'

class Unicodes(Enum):
    """
    Enumeration for Unicode characters used in the state representation.
    """
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
    """
    Enumeration for flags used in the state representation.
    """
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

class DebugModes(Enum):
    """
    Enumeration for debug modes.
    """
    Release = 'release'
    Innovation = 'innovation'

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

if getenv('DEBUGMODE') == DebugModes.Innovation.value:
    import unittest

    class TestConstants(unittest.TestCase):
        """
        Unit tests for the constants defined in this module.
        """

        def test_modes_enum(self):
            """
            Test the Modes enumeration values.
            """
            self.assertEqual(Modes.Light.value, 'light')
            self.assertEqual(Modes.Dark.value, 'dark')

        def test_unicodes_enum(self):
            """
            Test the Unicodes enumeration values.
            """
            self.assertEqual(Unicodes.Outlined_Monotone.value, '♙')
            self.assertEqual(Unicodes.Outlined_Pivot.value, '♘')
            self.assertEqual(Unicodes.Outlined_Slope.value, '♗')
            self.assertEqual(Unicodes.Outlined_Stride.value, '♖')
            self.assertEqual(Unicodes.Outlined_Radius.value, '♕')
            self.assertEqual(Unicodes.Outlined_Anchor.value, '♔')
            self.assertEqual(Unicodes.Filled_Monotone.value, '♟')
            self.assertEqual(Unicodes.Filled_Pivot.value, '♞')
            self.assertEqual(Unicodes.Filled_Slope.value, '♝')
            self.assertEqual(Unicodes.Filled_Stride.value, '♜')
            self.assertEqual(Unicodes.Filled_Radius.value, '♛')
            self.assertEqual(Unicodes.Filled_Anchor.value, '♚')
            self.assertEqual(Unicodes.Void_Unicode.value, '　')
            self.assertEqual(Unicodes.Invalid_Unicode.value, '⁇')

        def test_flags_enum(self):
            """
            Test the Flags enumeration values.
            """
            self.assertEqual(Flags.Void.value, 0x0)
            self.assertEqual(Flags.Light_Monotone.value, 0x1)
            self.assertEqual(Flags.Light_Pivot.value, 0x2)
            self.assertEqual(Flags.Light_Slope.value, 0x3)
            self.assertEqual(Flags.Light_Stride.value, 0x4)
            self.assertEqual(Flags.Light_Radius.value, 0x5)
            self.assertEqual(Flags.Light_Anchor.value, 0x6)
            self.assertEqual(Flags.Horizon.value, 0x8)
            self.assertEqual(Flags.Dark_Monotone.value, 0xA)
            self.assertEqual(Flags.Dark_Pivot.value, 0xB)
            self.assertEqual(Flags.Dark_Slope.value, 0xC)
            self.assertEqual(Flags.Dark_Stride.value, 0xD)
            self.assertEqual(Flags.Dark_Radius.value, 0xE)
            self.assertEqual(Flags.Dark_Anchor.value, 0xF)

        def test_flag2unicode_mapping(self):
            """
            Test the Flag2Unicode dictionary mapping.
            """
            self.assertEqual(Flag2Unicode[Flags.Void.value], Unicodes.Void_Unicode.value)
            self.assertEqual(Flag2Unicode[Flags.Light_Monotone.value], Unicodes.Outlined_Monotone.value)
            self.assertEqual(Flag2Unicode[Flags.Light_Pivot.value], Unicodes.Outlined_Pivot.value)
            self.assertEqual(Flag2Unicode[Flags.Light_Slope.value], Unicodes.Outlined_Slope.value)
            self.assertEqual(Flag2Unicode[Flags.Light_Stride.value], Unicodes.Outlined_Stride.value)
            self.assertEqual(Flag2Unicode[Flags.Light_Radius.value], Unicodes.Outlined_Radius.value)
            self.assertEqual(Flag2Unicode[Flags.Light_Anchor.value], Unicodes.Outlined_Anchor.value)
            self.assertEqual(Flag2Unicode[Flags.Dark_Monotone.value], Unicodes.Filled_Monotone.value)
            self.assertEqual(Flag2Unicode[Flags.Dark_Pivot.value], Unicodes.Filled_Pivot.value)
            self.assertEqual(Flag2Unicode[Flags.Dark_Slope.value], Unicodes.Filled_Slope.value)
            self.assertEqual(Flag2Unicode[Flags.Dark_Stride.value], Unicodes.Filled_Stride.value)
            self.assertEqual(Flag2Unicode[Flags.Dark_Radius.value], Unicodes.Filled_Radius.value)
            self.assertEqual(Flag2Unicode[Flags.Dark_Anchor.value], Unicodes.Filled_Anchor.value)

    if __name__ == '__main__':
        unittest.main()
