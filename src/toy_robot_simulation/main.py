import sys

from .controller import Command, Controller
from .robot import Direction, Location, Robot, Table

TABLE = Table(5, 5)


def execute_command(controller: Controller, command: str) -> None:
    """Parses and executes a command string on the robot through the controller.

    This function takes a command string, parses it to extract the command and its arguments,
    and then executes it on the robot. If the command is 'PLACE', it also parses the location
    and direction arguments.

    Args:
        controller (Controller): The controller that sends commands to the robot.
        command (str): The command string to be executed.
    """
    command, *args = (command.strip() or "-").split()
    try:
        if command == "PLACE":
            x, y, f = "".join(args).split(",")
            controller.execute(Command.PLACE, TABLE, Location(int(x), int(y)), Direction(f))
        else:
            controller.execute(Command(command))
    except (ValueError, TypeError):
        pass


def main():
    """The main entry point of the script.

    If command-line arguments are provided, it reads commands from the files specified.
    Otherwise, it enters an interactive mode where commands can be input manually.
    """
    robot = Robot()
    controller = Controller(robot)

    if len(sys.argv) > 1:
        # Read commands from files
        for file in sys.argv[1:]:
            with open(file) as f:
                for line in f.readlines():
                    execute_command(controller, line)
    else:
        # Interactive mode
        try:
            while True:
                execute_command(controller, input())
        except KeyboardInterrupt:
            # Exit on Ctrl+C
            pass
