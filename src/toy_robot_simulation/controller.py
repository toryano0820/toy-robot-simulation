from enum import Enum

from .robot import Robot


class Command(Enum):
    """Enumeration for robot commands."""

    LEFT = "LEFT"
    RIGHT = "RIGHT"
    MOVE = "MOVE"
    REPORT = "REPORT"
    PLACE = "PLACE"


class Controller:
    """A controller for executing commands on a robot.

    Attributes:
        robot (Robot): The robot instance that the controller will command.
    """

    def __init__(self, robot: Robot) -> None:
        """Initializes a new instance of the Controller class with a robot.

        Args:
            robot (Robot): The robot instance to control.
        """
        self.robot = robot

    def execute(self, command: Command, *args) -> None:
        """Executes the given command on the robot.

        This method dynamically calls the corresponding command method based on the Command enum.

        Args:
            command (Command): The command to execute.
            *args: Additional arguments required for the command.
        """
        func = getattr(self, f"_command_{command.value.lower()}", None)
        if callable(func):
            func(*args)

    def _command_place(self, table, location, direction) -> None:
        """Executes the PLACE command to set the robot's position and direction.

        Args:
            table: The table where the robot is to be placed.
            location: The starting location of the robot on the table.
            direction: The initial direction the robot is facing.
        """
        self.robot.place(table, location, direction)

    def _command_left(self) -> None:
        """Executes the LEFT command to turn the robot left."""
        self.robot.turn_left()

    def _command_right(self) -> None:
        """Executes the RIGHT command to turn the robot right."""
        self.robot.turn_right()

    def _command_move(self) -> None:
        """Executes the MOVE command to move the robot forward one unit."""
        self.robot.move()

    def _command_report(self) -> None:
        """Executes the REPORT command to print the robot's current position and direction."""
        self.robot.report()
