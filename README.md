# Space Station RPG

A text-based adventure game where you explore a space station, solve puzzles, and complete your mission.

## Game Overview

You are an engineer aboard a space station that's been damaged by a solar flare. Your mission is to repair the maintenance droid, retrieve the energy crystal, and reach the docking bay to save the station.

## Features

- Explore different areas of the space station
- Collect and use items to solve puzzles
- Interact with the environment and repair damaged systems
- Score points based on your actions
- Simple text-based interface

## Installation

1. Ensure you have Python 3.8+ installed
2. Clone this repository:
   ```bash
   git clone https://github.com/Antoekneeo/Software_RPG_Task.git
   cd Software_RPG_Task
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```bash
   python -m rpg_game.main
   ```
2. Follow the on-screen instructions
3. Type commands to interact with the game world

### Available Commands

- `go [direction]` - Move in the specified direction (north, south, east, west)
- `get tool` - Pick up the diagnostic tool
- `use tool` - Use the diagnostic tool on the droid
- `get crystal` - Pick up the energy crystal
- `win` - Complete the mission (must be in docking bay with crystal)
- `look` - View current location description
- `inventory` - Check your inventory
- `score` - Check your current score
- `help` - Show available commands

## Project Structure

```
Software_RPG_Task/
├── rpg_game/
│   ├── game/
│   │   ├── __init__.py
│   │   ├── diagnostic_tool.py
│   │   ├── droid.py
│   │   ├── energy_crystal.py
│   │   ├── game_controller.py
│   │   ├── location.py
│   │   ├── player.py
│   │   └── station_item.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_game_controller.py
│   ├── test_game_controller_edge_cases.py
│   ├── test_items.py
│   ├── test_location.py
│   ├── test_player.py
│   └── test_player_movement.py
├── .gitignore
├── CHANGELOG.md
├── PROJECT_ROADMAP.md
├── README.md
├── RULES.md
├── requirements-dev.txt
└── setup.py
```

## Testing

To run the test suite:

```bash
pip install -r requirements-dev.txt
pytest
```

## Contributing

Contributions are welcome! Please read our [contribution guidelines](CONTRIBUTING.md) before submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Created as part of a software engineering exercise
- Inspired by classic text adventure games