from dataclasses import dataclass
from enum import Enum
from typing import Union


@dataclass(frozen=True)
class Offset:
    """Represents the offset from a location.

    Attributes:
        x (int): The horizontal offset.
        y (int): The vertical offset.
    """

    x: int = 0
    y: int = 0


@dataclass(frozen=True)
class Location:
    """Represents a location in a two-dimensional space.

    Attributes:
        x (int): The horizontal coordinate.
        y (int): The vertical coordinate.
    """

    x: int = 0
    y: int = 0

    def __add__(self, other: Union[Offset, "Location"]) -> "Location":
        """Adds an Offset or another Location to this Location.

        Args:
            other (Union[Offset, "Location"]): The other Offset or Location to add.

        Returns:
            Location: The resulting Location after addition.

        Raises:
            TypeError: If 'other' is not of type Offset or Location.
        """
        if not isinstance(other, (Offset, self.__class__)):
            raise TypeError(f"Cannot add type {other.__class__.__name__} to a Location.")
        return Location(self.x + other.x, self.y + other.y)


@dataclass(frozen=True)
class Table:
    """Represents the dimensions of a table.

    Attributes:
        width (int): The width of the table.
        height (int): The height of the table.
    """

    width: int = 5
    height: int = 5


class Direction(Enum):
    """Enumeration for cardinal directions."""

    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


# Constants for turn sequences and movement offsets
TURN_LEFT_SEQUENCE = (Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST)
TURN_RIGHT_SEQUENCE = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
MOVEMENT_OFFSET_MAP = {
    Direction.NORTH: Offset(0, 1),
    Direction.EAST: Offset(1, 0),
    Direction.SOUTH: Offset(0, -1),
    Direction.WEST: Offset(-1, 0),
}


class Robot:
    """A robot that can be placed on a table and moved around.

    Attributes:
        table (Table | None): The table on which the robot is placed.
        location (Location | None): The current location of the robot.
        direction (Direction | None): The current direction the robot is facing.
    """

    def __init__(self) -> None:
        """Initializes a new instance of the Robot class."""
        self.table: Table | None = None
        self.location: Location | None = None
        self.direction: Direction | None = None

    def _check_placed(self) -> bool:
        """Checks if the robot has been placed on the table.

        Returns:
            bool: True if the robot is placed, False otherwise.
        """
        return self.table is not None and self.location is not None and self.direction is not None

    def _check_bounds(self, table: Table | None = None, location: Location | None = None) -> bool:
        """Checks if the given location is within the bounds of the given table.

        Args:
            table (Table | None): The table to check against. Defaults to the robot's table.
            location (Location | None): The location to check. Defaults to the robot's location.

        Returns:
            bool: True if the location is within the table's bounds, False otherwise.
        """
        table = table or self.table
        location = location or self.location
        return 0 <= location.x < table.width and 0 <= location.y < table.height

    def place(self, table: Table, location: Location, direction: Direction) -> None:
        """Places the robot on the table at the specified location and direction.

        Args:
            table (Table): The table to place the robot on.
            location (Location): The location to place the robot at.
            direction (Direction): The direction the robot will face.
        """
        if self._check_bounds(table, location):
            self.table = table
            self.location = location
            self.direction = direction

    def turn_left(self) -> None:
        """Turns the robot to the left if placed."""
        if self._check_placed():
            self.direction = TURN_LEFT_SEQUENCE[(TURN_LEFT_SEQUENCE.index(self.direction) + 1) % 4]

    def turn_right(self) -> None:
        """Turns the robot to the right if placed."""
        if self._check_placed():
            self.direction = TURN_RIGHT_SEQUENCE[
                (TURN_RIGHT_SEQUENCE.index(self.direction) + 1) % 4
            ]

    def move(self) -> None:
        """Moves the robot one unit forward in the direction it is currently facing.

        Checks if the robot is placed and if the new location is within the bounds of the table.
        If both checks pass, the robot's location is updated to the new location.
        """
        if self._check_placed():
            offset = MOVEMENT_OFFSET_MAP[self.direction]
            new_location = self.location + offset
            if self._check_bounds(location=new_location):
                self.location = new_location

    def report(self) -> None:
        """Prints the current location and direction of the robot.

        If the robot is placed, it outputs the current X and Y coordinates along with the direction.
        The output format is: 'Output: X,Y,DIRECTION'.
        """
        if self._check_placed():
            print(f"Output: {self.location.x},{self.location.y},{self.direction.value}")
