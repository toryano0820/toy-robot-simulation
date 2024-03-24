from unittest.mock import MagicMock, patch

import pytest

from toy_robot_simulation.controller import Command, Controller
from toy_robot_simulation.robot import Direction, Location, Robot, Table


class TestController:
    @pytest.fixture
    def mocked_robot(self):
        return MagicMock(Robot)

    @pytest.fixture
    def controller(self, mocked_robot):
        return Controller(mocked_robot)

    @pytest.mark.parametrize(
        "command, command_args, robot_func",
        [
            [Command.PLACE, (Table(1, 1), Location(0, 0), Direction.NORTH), "place"],
            [Command.LEFT, (), "turn_left"],
            [Command.RIGHT, (), "turn_right"],
            [Command.MOVE, (), "move"],
            [Command.REPORT, (), "report"],
        ],
    )
    def test_execute_calls_robot_method(
        self, controller, mocked_robot, command, command_args, robot_func
    ):
        func = getattr(mocked_robot, robot_func)

        controller.execute(command, *command_args)

        if command_args:
            func.assert_called_with(*command_args)
        else:
            func.assert_called()

    def test_execute_place_command_fails_without_arguments(self, controller):
        with pytest.raises(TypeError) as ex_ctx:
            controller.execute(Command.PLACE)

        ex_ctx.match(".+ missing 3 required positional arguments: .+")
