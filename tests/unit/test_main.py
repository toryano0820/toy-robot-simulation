import sys
from unittest.mock import MagicMock, mock_open, patch

import pytest

from toy_robot_simulation.controller import Command, Controller
from toy_robot_simulation.main import TABLE, execute_command, main
from toy_robot_simulation.robot import Direction, Location


class TestMain:
    @pytest.fixture
    def mocked_controller(self):
        return MagicMock(Controller)

    @pytest.mark.parametrize(
        "command_str, command",
        [
            ["PLACE 0,0,NORTH", Command.PLACE],
            ["LEFT", Command.LEFT],
            ["RIGHT", Command.RIGHT],
            ["MOVE", Command.MOVE],
            ["REPORT", Command.REPORT],
        ],
    )
    def test_execute_passes_valid_commands_to_controller(
        self, mocked_controller, command_str, command
    ):
        execute_command(mocked_controller, command_str)

        mocked_controller.execute.assert_called()
        assert mocked_controller.execute.call_args.args[0] == command

    @pytest.mark.parametrize(
        "command_str, location, direction",
        [
            ["PLACE 0,1,NORTH", Location(0, 1), Direction.NORTH],
            ["PLACE 1,2,EAST", Location(1, 2), Direction.EAST],
            ["PLACE 2,3,SOUTH", Location(2, 3), Direction.SOUTH],
            ["PLACE 3,4,WEST", Location(3, 4), Direction.WEST],
        ],
    )
    def test_execute_place_command_passes_valid_arguments_to_controller(
        self,
        mocked_controller,
        command_str,
        location,
        direction,
    ):
        execute_command(mocked_controller, command_str)

        mocked_controller.execute.assert_called_with(Command.PLACE, TABLE, location, direction)

    @pytest.mark.parametrize(
        "wrong_command_str",
        [
            "PLACE 0",
            "PLACE 0,0",
            "PLACE 0,NORTH",
            "PLACE 0,0,WRONG_DIRECTION",
            "TURN_LEFT",
            "TURN_RIGHT",
            "MOVE_NOW",
            "QWERTY",
            "ASD",
        ],
    )
    def test_execute_ignores_invalid_commands(self, mocked_controller, wrong_command_str):
        execute_command(mocked_controller, wrong_command_str)

        mocked_controller.execute.assert_not_called()

    def test_main_runs_file_mode_if_ran_with_parameters(self):
        mocked_open = MagicMock()

        with (
            patch("builtins.open", mock_open(mocked_open, "PLACE 0,0,NORTH")),
            patch.object(sys, "argv", ["main.py", "commands.txt"]),
        ):
            main()

        mocked_open.assert_called_with("commands.txt")

    def test_main_runs_interactive_mode_if_ran_without_parameters_and_exits_gracefully_on_keyboard_interrupt(
        self,
    ):
        mocked_input = MagicMock()

        with patch("builtins.input", mocked_input), patch.object(sys, "argv", ["main.py"]):

            def _input_interrupt():
                raise KeyboardInterrupt

            mocked_input.side_effect = _input_interrupt
            main()

        mocked_input.assert_called()
