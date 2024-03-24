import sys
from unittest.mock import MagicMock, mock_open, patch

import pytest

from toy_robot_simulation.main import main


class TestFileInputMode:
    @pytest.mark.parametrize(
        "commands, expected_output",
        [
            [["PLACE 0,0,NORTH", "REPORT"], "Output: 0,0,NORTH"],
            [["PLACE 0,0,NORTH", "MOVE", "REPORT"], "Output: 0,1,NORTH"],
            [["PLACE 0,0,NORTH", "LEFT", "REPORT"], "Output: 0,0,WEST"],
            [["PLACE 1,2,EAST", "MOVE", "MOVE", "LEFT", "MOVE", "REPORT"], "Output: 3,3,NORTH"],
            [["PLACE 0,0,SOUTH", "MOVE", "REPORT"], "Output: 0,0,SOUTH"],
            [["PLACE 0,0,WEST", "MOVE", "REPORT"], "Output: 0,0,WEST"],
            [["LEFT", "MOVE", "REPORT"], ""],
        ],
    )
    def test_file_input_mode(self, commands, expected_output):
        mocked_print = MagicMock()
        mocked_open = MagicMock()

        with (
            patch("builtins.print", mocked_print),
            patch("builtins.open", mock_open(mocked_open, "\n".join(commands))),
            patch.object(sys, "argv", ["main.py", "commands.txt"]),
        ):
            main()

        if expected_output:
            mocked_print.assert_called_with(expected_output)
        else:
            mocked_print.assert_not_called()
