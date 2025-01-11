"""
Utility for managing state transition rules
"""
import numpy as np
try:
    from .state import Flags, State
except Exception as exp:
    print(str(exp))
    from state import Flags, State


class Handler:
    def __init__(self, dark_mode: bool, hex_str: str = None, from_bytes: bytes = None) -> None:
        """
        New instance of Handler
        """
        self.state: State = State()
        self.dark_mode = dark_mode

        if hex_str is not None:
            self.state.from_hex(hex_str=hex_str)
        elif from_bytes is not None:
            self.state.state = np.frombuffer(from_bytes, dtype=np.uint8)
        self.matrix = self.state.to_matrix()

    def test_mode(self, horizon: int, axis: int) -> int:
        """
        Check if flag at given axis and horizon is of the same mode as Handler
        :param horizon: The horizon index in descending order
        :param axis: The axis index
        :return:
        """
        if self.matrix[7 - horizon][axis] == Flags.Void.value:
            return 0
        if (
            (self.dark_mode and (self.matrix[7 - horizon][axis] > Flags.Horizon.value)) or
            ((not self.dark_mode) and (self.matrix[7 - horizon][axis] < Flags.Horizon.value))
        ):
            return 1
        return -1

    def rule_monotone(self, horizon: int, axis: int) -> list[(int, int)]:
        """
        Computes all possible rules for a Monotone
        :param horizon: The horizon index
        :param axis: The axis index
        :return:
        """
        possible_rules = []
        orientation = -1 if self.dark_mode else 1
        
        if -1 < (horizon + orientation) < 8 and self.test_mode(horizon + orientation, axis) != 1:
            possible_rules.append((horizon + orientation, axis))

            if (
                -1 < (horizon + 2 * orientation) < 8 and
                self.test_mode(horizon + orientation, axis) == 0 and (
                    (self.dark_mode and horizon == 6) or
                    ((not self.dark_mode) and (horizon == 1))
                )
            ):
                if self.test_mode(horizon + 2 * orientation, axis) != 1:
                    possible_rules.append((horizon + 2 * orientation, axis))

        if (
            (-1 < (horizon + orientation) < 8 and
             -1 < (axis - 1) < 8) and
            self.test_mode(horizon + orientation, axis - 1) == -1
        ):
            possible_rules.append((horizon + orientation, axis - 1))

        if (
            (-1 < (horizon + orientation) < 8 and
             -1 < (axis + 1) < 8) and
            self.test_mode(horizon + orientation, axis + 1) == -1
        ):
            possible_rules.append((horizon + orientation, axis + 1))

        return possible_rules

    def rule_pivot(self, horizon: int, axis: int) -> list[(int, int)]:
        """
        Computes all possible rules for a Pivot

        The Pivot rules in an "L" shape:
        - Two squares in one orientation and one unit perpendicular.
        - rules are unaffected by dark/light mode.

        :param horizon: The horizon index.
        :param axis: The axis index.
        :return: A list of valid rules as (horizon, axis).
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

        # Filter out rules that go out of bounds or are invalid
        for new_horizon, new_axis in pivot_rules:
            if 0 <= new_horizon < 8 and 0 <= new_axis < 8:
                # Only add if the move is valid based on the mode
                mode_check = self.test_mode(new_horizon, new_axis)
                if mode_check != 1:  # Exclude rules blocked by same-mode flags
                    possible_rules.append((new_horizon, new_axis))

        return possible_rules

    def rule_slope(self, horizon: int, axis: int) -> list[(int, int)]:
        """
        Computes all possible rules for a Slope.

        The Slope rules diagonally in all orientations:
        - rules are blocked by flags on its path.
        - Can capture alternate flags but cannot move past them.

        :param horizon: The horizon index.
        :param axis: The axis index.
        :return: A list of valid rules as (horizon, axis).
        """
        possible_rules = []

        # orientation vectors for diagonal rules
        orientations = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dh, da in orientations:
            new_horizon, new_axis = horizon, axis

            while True:
                new_horizon += dh
                new_axis += da

                # Check boundaries
                if not (0 <= new_horizon < 8 and 0 <= new_axis < 8):
                    break

                mode_check = self.test_mode(new_horizon, new_axis)

                if mode_check == 1:  # Same-mode flag blocks the path
                    break
                elif mode_check == -1:  # alternate flag, capture possible
                    possible_rules.append((new_horizon, new_axis))
                    break
                else:  # Valid empty unit
                    possible_rules.append((new_horizon, new_axis))

        return possible_rules

    def rule_stride(self, horizon: int, axis: int) -> list[(int, int)]:
        """
        Computes all possible rules for a Stride

        The Slope rules straight in all orientations:
        - rules are blocked by flags on its path.
        - Can capture alternate flags but cannot move past them.

        :param horizon: The horizon index.
        :param axis: The axis index.
        :return: A list of valid rules as (horizon, axis).
        """
        possible_rules = []

        # orientation vectors for diagonal rules
        orientations = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dh, da in orientations:
            new_horizon, new_axis = horizon, axis

            while True:
                new_horizon += dh
                new_axis += da

                # Check boundaries
                if not (0 <= new_horizon < 8 and 0 <= new_axis < 8):
                    break

                mode_check = self.test_mode(new_horizon, new_axis)

                if mode_check == 1:  # Same-mode flag blocks the path
                    break
                elif mode_check == -1:  # alternate flag, capture possible
                    possible_rules.append((new_horizon, new_axis))
                    break
                else:  # Valid empty unit
                    possible_rules.append((new_horizon, new_axis))

        return possible_rules

    def rule_radius(self, horizon: int, axis: int) -> list[(int, int)]:
        """
        Computes all possible rules for a Radius.

        The Slope rules straight or diagonally in all orientations:
        - rules are blocked by flags on its path.
        - Can capture alternate flags but cannot move past them.

        :param horizon: The horizon index.
        :param axis: The axis index.
        :return: A list of valid rules as (horizon, axis).
        """
        possible_rules = []

        # orientation vectors for diagonal rules
        orientations = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dh, da in orientations:
            new_horizon, new_axis = horizon, axis

            while True:
                new_horizon += dh
                new_axis += da

                # Check boundaries
                if not (0 <= new_horizon < 8 and 0 <= new_axis < 8):
                    break

                mode_check = self.test_mode(new_horizon, new_axis)

                if mode_check == 1:  # Same-mode flag blocks the path
                    break
                elif mode_check == -1:  # alternate flag, capture possible
                    possible_rules.append((new_horizon, new_axis))
                    break
                else:  # Valid empty unit
                    possible_rules.append((new_horizon, new_axis))

        return possible_rules

    def rule_anchor(self, horizon: int, axis: int) -> list[(int, int)]:
        """
        Computes all possible rules for an Anchor.

        The Anchor rules one unit in any orientation:
        - Horizontally, vertically, or diagonally.
        - Cannot move to squares occupied by same-mode flags.

        :param horizon: The horizon index.
        :param axis: The axis index.
        :return: A list of valid rules as (horizon, axis).
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
            if 0 <= new_horizon < 8 and 0 <= new_axis < 8:
                mode_check = self.test_mode(new_horizon, new_axis)
                if mode_check != 1:  # Exclude rules blocked by same-mode flags
                    possible_rules.append((new_horizon, new_axis))

        return possible_rules

    def all_possible_rules(self) -> list[((int, int), list[(int, int)])]:
        possible_rules = []
        for horizon in range(8):
            for axis in range(8):
                if self.test_mode(horizon, axis) == 1:
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


if __name__ == "__main__":
    from state import Flag2Unicode

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
    for (horizon, axis), rules in handler.all_possible_rules():
        flag = handler.matrix[7 - horizon][axis]
        print(horizon, axis, Flag2Unicode.get(flag), flag, rules)

    handler.dark_mode = True
    for (horizon, axis), rules in handler.all_possible_rules():
        flag = handler.matrix[7 - horizon][axis]
        print(horizon, axis, Flag2Unicode.get(flag), flag, rules)

