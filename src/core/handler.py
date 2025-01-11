"""
Utility for managing state transition rules.

Classes
-------
- ModeCheck: Enumeration for mode check results.
- Handler: Manages state transition rules based on the current state and mode.

Functions
---------
- inbounds: Checks if a value is within the range [0, 7] inclusive.

ModeCheck
---------
- Attributes
    - VOID: Represents a void flag.
    - SAME_MODE: Represents a flag of the same mode.
    - DIFFERENT_MODE: Represents a flag of a different mode.

Handler
-------
- Attributes
    - state: The current state of the system.
    - dark_mode: Boolean indicating if the handler is in dark mode.
    - unsafe_anchor: Boolean indicating if the handler is in unsafe anchor mode.
    - matrix: The state represented as a matrix.
    - alternate_handler: An alternate handler for unsafe anchor mode.
    - alternate_rules: A list of alternate rules for unsafe anchor mode.

- Methods
    - __init__: Initializes a new instance of Handler.
    - test_mode: Checks if the flag at a given axis and horizon is of the same mode as Handler.
    - rule_monotone: Computes all possible rules for a Monotone.
    - rule_pivot: Computes all possible rules for a Pivot.
    - compute_rules: Utility method to compute rules based on orientations.
    - rule_slope: Computes all possible rules for a Slope.
    - rule_stride: Computes all possible rules for a Stride.
    - rule_radius: Computes all possible rules for a Radius.
    - rule_anchor: Computes all possible rules for an Anchor.
    - all_possible_rules: Computes all possible rules for all flags in the current state.

Testing and QA
==============
Classes
-------
- TestHandler: Unit tests for the Handler class.

TestHandler
-----------
- Methods
    - setUp: Sets up the test case environment.
    - test_handler: Tests the Handler class.
"""
from os import getenv
import numpy as np
from enum import Enum
if __package__ is None or __package__ == '':
    from constants import Flags, DebugModes
    from state import State
else:
    from .constants import Flags, DebugModes
    from .state import State

class ModeCheck(Enum):
    """
    Enumeration for mode check results.
    """
    VOID = 0
    SAME_MODE = 1
    DIFFERENT_MODE = -1

def inbounds(value: int) -> bool:
    """
    Checks if a value is within the range [0, 7] inclusive.

    Parameters
    ----------
    value : int
        The value to check.

    Returns
    -------
    bool
        True if the value is within the range [0, 7], False otherwise.
    """
    return 0 <= value <= 7

class Handler:
    """
    Manages state transition rules based on the current state and mode.
    """
    def __init__(self, dark_mode: bool, hex_str: str = None, from_bytes: bytes = None, unsafe_anchor: bool = False):
        """
        Initializes a new instance of Handler.

        Parameters
        ----------
        dark_mode : bool
            Boolean indicating if the handler is in dark mode.
        hex_str : str, optional
            Hex string to initialize the state.
        from_bytes : bytes, optional
            Byte array to initialize the state.
        unsafe_anchor : bool, optional
            Boolean indicating if the handler is in unsafe anchor mode.
        """
        self.state: State = State()
        self.dark_mode = dark_mode
        self.unsafe_anchor = unsafe_anchor

        if hex_str is not None:
            self.state.from_hex(hex_str=hex_str)
        elif from_bytes is not None:
            self.state.state = np.frombuffer(from_bytes, dtype=np.uint8)
        self.matrix = self.state.to_matrix()

        self.alternate_handler: Handler | None = None
        self.alternate_rules: list[tuple[tuple[int, int], list[tuple[int, int]]]] = []

    def test_mode(self, horizon: int, axis: int) -> ModeCheck:
        """
        Checks if the flag at a given axis and horizon is of the same mode as Handler.

        Parameters
        ----------
        horizon : int
            The horizon index.
        axis : int
            The axis index.

        Returns
        -------
        ModeCheck
            ModeCheck.VOID if the flag is void, ModeCheck.SAME_MODE if it is of the same mode, ModeCheck.DIFFERENT_MODE otherwise.
        """
        flag = self.matrix[7 - horizon][axis]
        if flag == Flags.Void.value:
            return ModeCheck.VOID
        if (
            (self.dark_mode and (flag > Flags.Horizon.value)) or
            ((not self.dark_mode) and (flag < Flags.Horizon.value))
        ):
            return ModeCheck.SAME_MODE
        return ModeCheck.DIFFERENT_MODE

    def rule_monotone(self, horizon: int, axis: int) -> list[tuple[int, int]]:
        """
        Computes all possible rules for a Monotone.

        Parameters
        ----------
        horizon : int
            The horizon index.
        axis : int
            The axis index.

        Returns
        -------
        list[tuple[int, int]]
            A list of valid rules as (horizon, axis).
        """
        possible_rules = []
        orientation = -1 if self.dark_mode else 1

        forward = horizon + orientation

        if not self.unsafe_anchor:
            if inbounds(forward) and self.test_mode(forward, axis) == ModeCheck.VOID:
                possible_rules.append((forward, axis))

                forward_double = forward + orientation
                if ((
                        (self.dark_mode and horizon == 6) or
                        ((not self.dark_mode) and (horizon == 1))
                    ) and
                    inbounds(forward_double) and
                    self.test_mode(forward_double, axis) == ModeCheck.VOID
                ):
                    possible_rules.append((forward_double, axis))

            if (
                inbounds(forward) and
                inbounds(axis - 1) and
                self.test_mode(forward, axis - 1) == ModeCheck.DIFFERENT_MODE
            ):
                possible_rules.append((forward, axis - 1))

            if (
                inbounds(forward) and
                inbounds(axis + 1) and
                self.test_mode(forward, axis + 1) == ModeCheck.DIFFERENT_MODE
            ):
                possible_rules.append((forward, axis + 1))
        else:
            possible_rules.append((forward, axis - 1))
            possible_rules.append((forward, axis + 1))

        return possible_rules

    def rule_pivot(self, horizon: int, axis: int) -> list[tuple[int, int]]:
        """
        Computes all possible rules for a Pivot.

        The Pivot rules in an "L" shape:
        - Two units straight and one unit perpendicular.
        - Rules are unaffected by dark/light mode.

        Parameters
        ----------
        horizon : int
            The horizon index.
        axis : int
            The axis index.

        Returns
        -------
        list[tuple[int, int]]
            A list of valid rules as (horizon, axis).
        """
        possible_rules = []

        # All potential L-shaped rules
        pivot_rules = [
            (horizon + 2, axis + 1),
            (horizon + 2, axis - 1),
            (horizon - 2, axis + 1),
            (horizon - 2, axis - 1),
            (horizon + 1, axis + 2),
            (horizon + 1, axis - 2),
            (horizon - 1, axis + 2),
            (horizon - 1, axis - 2),
        ]

        for new_horizon, new_axis in pivot_rules:
            if inbounds(new_horizon) and inbounds(new_axis):
                mode_check = self.test_mode(new_horizon, new_axis)
                if mode_check != ModeCheck.SAME_MODE or self.unsafe_anchor:
                    possible_rules.append((new_horizon, new_axis))

        return possible_rules

    def compute_rules(self, horizon: int, axis: int, orientations: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """
        Utility method to compute rules based on orientations.

        Parameters
        ----------
        horizon : int
            The horizon index.
        axis : int
            The axis index.
        orientations : list[tuple[int, int]]
            List of orientation vectors.

        Returns
        -------
        list[tuple[int, int]]
            A list of valid rules as (horizon, axis).
        """
        possible_rules = []

        for dh, da in orientations:
            new_horizon, new_axis = horizon, axis

            while True:
                new_horizon += dh
                new_axis += da

                # Check boundaries
                if not (inbounds(new_horizon) and inbounds(new_axis)):
                    break

                mode_check = self.test_mode(new_horizon, new_axis)

                if mode_check == ModeCheck.SAME_MODE:  # Same-mode flag blocks the path
                    if self.unsafe_anchor:
                        # Special case for unsafe anchor mode
                        possible_rules.append((new_horizon, new_axis))
                    break
                elif mode_check == ModeCheck.DIFFERENT_MODE:  # Alternate flag, capture possible
                    possible_rules.append((new_horizon, new_axis))
                    if self.unsafe_anchor:
                        flag = self.matrix[7 - new_horizon][new_axis]
                        if flag == Flags.Dark_Anchor.value or flag == Flags.Light_Anchor.value:
                            # Special case for unsafe anchor mode
                            continue
                    break
                else:  # Valid empty unit
                    possible_rules.append((new_horizon, new_axis))

        return possible_rules

    def rule_slope(self, horizon: int, axis: int) -> list[tuple[int, int]]:
        """
        Computes all possible rules for a Slope.

        The Slope rules diagonally in all orientations:
        - Rules are blocked by flags on its path.
        - Can capture alternate flags but cannot rule past them.

        Parameters
        ----------
        horizon : int
            The horizon index.
        axis : int
            The axis index.

        Returns
        -------
        list[tuple[int, int]]
            A list of valid rules as (horizon, axis).
        """
        orientations = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self.compute_rules(horizon, axis, orientations)

    def rule_stride(self, horizon: int, axis: int) -> list[tuple[int, int]]:
        """
        Computes all possible rules for a Stride.

        The Stride rules straight in all orientations:
        - Rules are blocked by flags on its path.
        - Can capture alternate flags but cannot rule past them.

        Parameters
        ----------
        horizon : int
            The horizon index.
        axis : int
            The axis index.

        Returns
        -------
        list[tuple[int, int]]
            A list of valid rules as (horizon, axis).
        """
        orientations = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return self.compute_rules(horizon, axis, orientations)

    def rule_radius(self, horizon: int, axis: int) -> list[tuple[int, int]]:
        """
        Computes all possible rules for a Radius.

        The Radius rules straight or diagonally in all orientations:
        - Rules are blocked by flags on its path.
        - Can capture alternate flags but cannot rule past them.

        Parameters
        ----------
        horizon : int
            The horizon index.
        axis : int
            The axis index.

        Returns
        -------
        list[tuple[int, int]]
            A list of valid rules as (horizon, axis).
        """
        orientations = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self.compute_rules(horizon, axis, orientations)

    def rule_anchor(self, horizon: int, axis: int) -> list[tuple[int, int]]:
        """
        Computes all possible rules for an Anchor.

        The Anchor rules one unit in any orientation:
        - Horizontally, vertically, or diagonally.
        - Cannot rule on units occupied by same-mode flags.
        - Cannot rule on a coordinate that is unsafe for the anchor.

        Parameters
        ----------
        horizon : int
            The horizon index.
        axis : int
            The axis index.

        Returns
        -------
        list[tuple[int, int]]
            A list of valid rules as (horizon, axis).
        """
        possible_rules = []

        # All possible orientations for the Anchor
        orientations = [
            (-1, 0), (1, 0),  # Vertical
            (0, -1), (0, 1),  # Horizontal
            (-1, -1), (-1, 1),  # Diagonal
            (1, -1), (1, 1),  # Diagonal
        ]

        for dh, da in orientations:
            new_horizon = horizon + dh
            new_axis = axis + da

            # Check boundaries
            if inbounds(new_horizon) and inbounds(new_axis):
                mode_check = self.test_mode(new_horizon, new_axis)
                if mode_check != ModeCheck.SAME_MODE:
                    # Check if the new coordinate is safe for the anchor
                    is_safe = True
                    if self.alternate_handler is not None:
                        for _, rules in self.alternate_rules:
                            if (new_horizon, new_axis) in rules:
                                is_safe = False
                                break
                    if is_safe:
                        possible_rules.append((new_horizon, new_axis))

        return possible_rules

    def all_possible_rules(self) -> list[tuple[tuple[int, int], list[tuple[int, int]]]]:
        """
        Computes all possible rules for all flags in the current state.

        Returns
        -------
        list[tuple[tuple[int, int], list[tuple[int, int]]]]
            A list of tuples where each tuple contains the coordinate of the flag and a list of valid rules.
        """
        possible_rules = []
        anchor_coord = None

        # If the handler is not in unsafe anchor mode, check if the anchor is safe
        if not self.unsafe_anchor:
            # Find the anchor's coordinate
            for horizon in range(8):
                for axis in range(8):
                    if self.test_mode(horizon, axis) == ModeCheck.SAME_MODE:
                        flag = self.matrix[7 - horizon][axis]
                        if flag == Flags.Dark_Anchor.value or flag == Flags.Light_Anchor.value:
                            anchor_coord = (horizon, axis)
                            break
                if anchor_coord:
                    break

            self.alternate_handler = Handler(not self.dark_mode, hex_str=self.state.to_hex(), unsafe_anchor=True)
            self.alternate_rules = self.alternate_handler.all_possible_rules()

            for _, rules in self.alternate_rules:
                if anchor_coord in rules:
                    # anchor is unsafe, only allow anchor's rules
                    return [(anchor_coord, self.rule_anchor(*anchor_coord))]

        # Compute all possible rules for all flags
        for horizon in range(8):
            for axis in range(8):
                if self.test_mode(horizon, axis) == ModeCheck.SAME_MODE:
                    flag = self.matrix[7 - horizon][axis]
                    if flag == Flags.Dark_Monotone.value or flag == Flags.Light_Monotone.value:
                        possible_rules.append(((horizon, axis), self.rule_monotone(horizon, axis)))
                    elif flag == Flags.Dark_Pivot.value or flag == Flags.Light_Pivot.value:
                        possible_rules.append(((horizon, axis), self.rule_pivot(horizon, axis)))
                    elif flag == Flags.Dark_Slope.value or flag == Flags.Light_Slope.value:
                        possible_rules.append(((horizon, axis), self.rule_slope(horizon, axis)))
                    elif flag == Flags.Dark_Stride.value or flag == Flags.Light_Stride.value:
                        possible_rules.append(((horizon, axis), self.rule_stride(horizon, axis)))
                    elif flag == Flags.Dark_Radius.value or flag == Flags.Light_Radius.value:
                        possible_rules.append(((horizon, axis), self.rule_radius(horizon, axis)))
                    elif flag == Flags.Dark_Anchor.value or flag == Flags.Light_Anchor.value:
                        possible_rules.append(((horizon, axis), self.rule_anchor(horizon, axis)))

        return possible_rules

if getenv('DEBUGMODE') == DebugModes.Innovation.value:
    import unittest
    from constants import Flag2Unicode, TestConstants
    from state import TestState

    class TestHandler(unittest.TestCase):
        """
        Unit tests for Handler class.
        """

        def setUp(self):
            """
            Sets up the test case environment.
            """
            # Standard state
            init_state = np.array([
                [
                    Flags.Dark_Stride.value,
                    Flags.Dark_Pivot.value,
                    Flags.Dark_Slope.value,
                    0,
                    Flags.Dark_Radius.value,
                    Flags.Dark_Slope.value,
                    Flags.Dark_Pivot.value,
                    Flags.Dark_Stride.value,
                ],
                [Flags.Dark_Monotone.value] * 4 + [0] * 4,
                [0, Flags.Dark_Anchor.value, 0, 0, Flags.Light_Anchor.value, 0, 0, 0],
                [0] * 4 + [Flags.Dark_Monotone.value] * 4,
                [Flags.Light_Monotone.value] * 8,
                [0] * 8,
                [0] * 8,
                [
                    Flags.Light_Stride.value,
                    Flags.Light_Pivot.value,
                    Flags.Light_Slope.value,
                    Flags.Light_Radius.value,
                    0,
                    Flags.Light_Slope.value,
                    Flags.Light_Pivot.value,
                    Flags.Light_Stride.value,
                ],
            ], dtype=np.uint8)
            init_state_hex_str = State().from_matrix(matrix=init_state).to_hex()

            # Create instance of Handler and load standard state
            self.handler = Handler(dark_mode=False, hex_str=init_state_hex_str)

        def test_handler(self):
            """
            Tests the Handler class.
            """
            print(self.handler.state)
            for (horizon, axis), rules in self.handler.all_possible_rules():
                flag = self.handler.matrix[7 - horizon][axis]
                print(horizon, axis, Flag2Unicode.get(flag), flag, rules)

            self.handler.dark_mode = True
            for (horizon, axis), rules in self.handler.all_possible_rules():
                flag = self.handler.matrix[7 - horizon][axis]
                print(horizon, axis, Flag2Unicode.get(flag), flag, rules)

    if __name__ == '__main__':
        unittest.main()
