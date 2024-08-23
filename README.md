# Gomoku

This project is a Python implementation of the Gomoku game, including an AI opponent. The game is developed using Pygame and supports a graphical interface where players can play against each other or test the AI.

## Prerequisites

Before you start, ensure you have the following installed:

- Python 3.10 or higher
- `pip` (Python package installer)
- `virtualenv` (for managing a virtual Python environment)
- `fontconfig` (for font handling on Linux)

### Installing System Dependencies

For Ubuntu (or other Debian-based systems), you can install the necessary system dependencies by running:

```bash
sudo apt-get update
sudo apt-get install fontconfig
```

## Setting Up the Project

Follow these steps to set up the project:

1. **Clone the repository**

2. **Create and activate a virtual environment:**

   ```bash
   cd gomoku
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**

   You can use the `Makefile` to install all necessary Python packages:

   ```bash
   make install
   ```

   This will install all the packages listed in `requirements.txt`.

## Running the Game

To start the game, simply run:

```bash
make
```

This will run the game using Pygame.

## Cleaning Up

If you need to clean up the environment or reset the project, you can use the following commands:

- **Clean the virtual environment:**

  ```bash
  make clean
  ```

- **Force clean and reinstall everything:**

  ```bash
  make fclean
  make install
  ```

## Additional Information

- **Game Controls:**
  - Use the mouse to click on intersections to place stones.
  - The game ends when one player aligns five stones in a row.

- **Exiting the Game:**
  - To exit the game, simply close the Pygame window.

## System Dependencies

Before setting up the Python environment, make sure to install the following system dependencies:

### Ubuntu (or other Debian-based systems)

```bash
sudo apt-get update
sudo apt-get install fontconfig
```

This ensures that `fc-list` is available for Pygame to load system fonts correctly.

### Summary of Makefile Commands:

- `make install`: Installs the Python dependencies.
- `make`: Runs the game.
- `make clean`: Cleans up the virtual environment.
- `make fclean`: Force cleans everything and reinstalls the dependencies.
