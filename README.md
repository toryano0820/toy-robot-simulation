# Toy Robot Simulation

This project provides a command execution system for a simulated robot. The system reads commands, interprets them, and applies them to the robot within a defined table space.


## Overview

The `Robot` class simulates a robot that can be placed on a `Table` and moved around. The `Controller` class takes commands and executes them on the `Robot`. Commands are defined in the `Command` enum and include moving the robot, turning it, and reporting its location.


## Setup

To set up the project:
1. Clone the repository and ensure you have Python 3.7+ and pip installed on your system.
2. Install the program with the following command:
    ```bash
    pip install .
    ```
    > Test run with the following commands:
    > ```bash
    > toy_robot_simulation  # terminal should pause as it is waiting for input, then you can enter below commands, Ctrl+C to exit.
    > PLACE 0,0,NORTH
    > REPORT
    > ```
    > Above commands should print "Output: 0,0,NORTH".


## Usage

The program can be run in two modes:

1. **File Input Mode**: If command-line arguments are provided, the program reads commands from the specified files.

    ```bash
    toy_robot_simulation commands.txt ...
    ```

2. **Interactive Mode**: If no arguments are provided, the program enters an interactive mode where commands can be input manually.

    ```bash
    toy_robot_simulation
    ```


## Commands

- `PLACE X,Y,F`: Places the robot on the table at position X,Y facing direction F.
- `MOVE`: Moves the robot one unit forward in the current direction.
- `LEFT`: Turns the robot left.
- `RIGHT`: Turns the robot right.
- `REPORT`: Outputs the current position and direction of the robot.


## Testing

To test the project:
1. Ensure `pytest` is installed (listed in `tests/requirements.txt`).
    ```bash
    pip install pytest  # or pip install -r tests/requirements.txt
    ```
2. Run pytest command:
    ```bash
    pytest
    ```

To check test coverage:
1. Ensure `coverage` is installed (listed in `tests/requirements.txt`).
    ```bash
    pip install coverage  # or pip install -r tests/requirements.txt
    ```
2. Run pytest with coverage:
    ```bash
    coverage run -m pytest
    ```
3. Print coverage report:
    ```bash
    coverage report
    ```


## Pre-Commit

We use pre-commit in this project to ensure that we are following Python coding standards.  
To enable pre-commit:
1. Ensure `pre-commit` is installed (listed in `requirements.txt`).
    ```bash
    pip install pre-commit  # or pip install -r requirements.txt
    ```