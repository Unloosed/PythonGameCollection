# Game Menu

This project is a simple game menu built using Python's Tkinter library. It allows users to select and start different games from a graphical interface.

## GitHub Page
The link to this project's GitHub Pages documentation can be found [here](https://unloosed.github.io/PythonGameCollection/)

## Features

- **House Escape**: A thrilling escape game.
- **Snake**: The classic snake game.
- **Pollen Collector**: Play as a bee braving the storm to collect pollen for the hive!

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Unloosed/PythonGameCollection.git
    cd PythonGameCollection
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the main script to start the game menu:
```bash
python main.py
```

## Project Structure

- `main.py`: The main script that launches the game menu in an interactable **GUI**.
- `games/`: Directory containing all game-specific files.
    - Each `.py` file contains a unique game that gets loaded into `main.py`.
- `requirements.txt`: Lists the dependencies required for the project.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE.txt](https://unloosed.github.io/PythonGameCollection/LICENSE.txt) file for details.

## Acknowledgements

Thanks to the developers of the Tkinter library for making GUI development in Python straightforward.
