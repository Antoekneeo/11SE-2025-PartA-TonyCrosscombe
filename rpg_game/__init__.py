"""
RPG Game Package

This package contains the implementation of a text-based RPG game where the player
navigates through different locations, collects items, and completes objectives.

To start the game, run the main.py script in the rpg_game directory.
"""

# Import key components to make them available at the package level
from .game.game_controller import GameController
from .game.player import Player
from .game.location import Location
from .game.station_item import StationItem
from .game.diagnostic_tool import DiagnosticTool
from .game.energy_crystal import EnergyCrystal
from .game.droid import DamagedMaintenanceDroid

# Define __all__ for explicit exports
__all__ = [
    'GameController',
    'Player',
    'Location',
    'StationItem',
    'DiagnosticTool',
    'EnergyCrystal',
    'DamagedMaintenanceDroid'
]
