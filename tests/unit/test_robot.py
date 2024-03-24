from unittest.mock import MagicMock, patch

import pytest

from toy_robot_simulation.robot import Direction, Location, Offset, Robot, Table


class TestLocation:
    def test_location_can_be_added_with_another_location(self):
        assert Location(1, 2) + Location(3, 4) == Location(4, 6)

    def test_location_can_be_added_with_an_offset(self):
        assert Location(1, 2) + Offset(3, 4) == Location(4, 6)

    def test_location_cannot_be_added_to_an_offset(self):
        with pytest.raises(TypeError):
            _ = Offset(1, 2) + Location(3, 4)

    @pytest.mark.parametrize("fail_value", [1, 1.0, True, "str", [], (), {}, set()])
    def test_location_cannot_be_added_with_any_other_types(self, fail_value):
        with pytest.raises(TypeError) as ex_ctx:
            _ = Location(1, 2) + fail_value
        ex_ctx.match(f"Cannot add type {fail_value.__class__.__name__} to a Location.")


class TestRobot:
    @pytest.fixture
    def robot(self):
        return Robot()

    @pytest.fixture
    def default_table(self):
        return Table(5, 5)

    @pytest.fixture
    def default_location(self):
        return Location(0, 0)

    @pytest.fixture
    def default_direction(self):
        return Direction.NORTH

    def test_initializes_with_null_table(self, robot):
        assert robot.table is None

    def test_initializes_with_null_location(self, robot):
        assert robot.location is None

    def test_initializes_with_null_direction(self, robot):
        assert robot.direction is None

    def test_place_succeeds_on_correct_bounds(
        self, robot, default_table, default_location, default_direction
    ):
        robot.place(default_table, default_location, default_direction)

        assert robot.table == default_table
        assert robot.location == default_location
        assert robot.direction == default_direction

    @pytest.mark.parametrize("wrong_location", [Location(-1, -1), Location(5, 5)])
    def test_place_ignores_incorrect_bounds(
        self, robot, default_table, default_direction, wrong_location
    ):
        robot.place(default_table, wrong_location, default_direction)

        assert robot.table is None
        assert robot.location is None
        assert robot.direction is None

    @pytest.mark.parametrize(
        "initial_direction, expected_turn_direction",
        [
            [Direction.NORTH, Direction.WEST],
            [Direction.EAST, Direction.NORTH],
            [Direction.SOUTH, Direction.EAST],
            [Direction.WEST, Direction.SOUTH],
        ],
    )
    def test_turn_left_changes_direction_to_expected_value(
        self, robot, default_table, default_location, initial_direction, expected_turn_direction
    ):
        robot.place(default_table, default_location, initial_direction)
        robot.turn_left()

        assert robot.direction == expected_turn_direction

    def test_turn_left_ignored_if_unplaced(self, robot):
        robot.turn_left()

        assert robot.direction is None

    @pytest.mark.parametrize(
        "initial_direction, expected_turn_direction",
        [
            [Direction.NORTH, Direction.EAST],
            [Direction.EAST, Direction.SOUTH],
            [Direction.SOUTH, Direction.WEST],
            [Direction.WEST, Direction.NORTH],
        ],
    )
    def test_turn_right_changes_direction_to_expected_value(
        self, robot, default_table, default_location, initial_direction, expected_turn_direction
    ):
        robot.place(default_table, default_location, initial_direction)
        robot.turn_right()

        assert robot.direction == expected_turn_direction

    def test_turn_right_ignored_if_unplaced(self, robot):
        robot.turn_right()

        assert robot.direction is None

    @pytest.mark.parametrize(
        "initial_location, direction, move_count, expected_location",
        [
            [Location(2, 2), Direction.NORTH, 1, Location(2, 3)],
            [Location(2, 2), Direction.NORTH, 2, Location(2, 4)],
            [Location(2, 2), Direction.EAST, 1, Location(3, 2)],
            [Location(2, 2), Direction.EAST, 2, Location(4, 2)],
            [Location(2, 2), Direction.SOUTH, 1, Location(2, 1)],
            [Location(2, 2), Direction.SOUTH, 2, Location(2, 0)],
            [Location(2, 2), Direction.WEST, 1, Location(1, 2)],
            [Location(2, 2), Direction.WEST, 2, Location(0, 2)],
        ],
    )
    def test_move_changes_location_to_expected_value(
        self, robot, default_table, initial_location, direction, move_count, expected_location
    ):
        robot.place(default_table, initial_location, direction)
        for _ in range(move_count):
            robot.move()

        assert robot.location == expected_location

    def test_move_ignored_if_unplaced(self, robot):
        robot.move()

        assert robot.location is None

    @pytest.mark.parametrize(
        "location, direction, expected_print_arg",
        [
            [Location(0, 1), Direction.NORTH, "Output: 0,1,NORTH"],
            [Location(1, 2), Direction.EAST, "Output: 1,2,EAST"],
            [Location(2, 3), Direction.SOUTH, "Output: 2,3,SOUTH"],
            [Location(3, 4), Direction.WEST, "Output: 3,4,WEST"],
        ],
    )
    def test_report_prints_current_location_and_direction(
        self, robot, default_table, location, direction, expected_print_arg
    ):
        mocked_print = MagicMock()

        robot.place(default_table, location, direction)
        with patch("builtins.print", mocked_print):
            robot.report()

        mocked_print.assert_called_with(expected_print_arg)

    def test_report_ignored_if_unplaced(self, robot):
        mocked_print = MagicMock()

        with patch("builtins.print", mocked_print):
            robot.report()

        mocked_print.assert_not_called()
