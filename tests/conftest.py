"""
Pytest configuration and fixtures for the RPG Game tests.
"""
import pytest
from rpg_game.game.station_item import StationItem
from rpg_game.game.diagnostic_tool import DiagnosticTool
from rpg_game.game.energy_crystal import EnergyCrystal
from rpg_game.game.location import Location
from rpg_game.game.droid import DamagedMaintenanceDroid
from rpg_game.game.player import Player
from rpg_game.game.game_controller import GameController

@pytest.fixture
def sample_item():
    """Return a sample StationItem for testing."""
    return StationItem("Test Item", "A test item for unit testing.")

@pytest.fixture
def diagnostic_tool():
    """Return a DiagnosticTool instance for testing."""
    return DiagnosticTool()

@pytest.fixture
def energy_crystal():
    """Return an EnergyCrystal instance for testing."""
    return EnergyCrystal()

@pytest.fixture
def maintenance_tunnels():
    """Return a Location instance for Maintenance Tunnels with a droid."""
    loc = Location("Maintenance Tunnels", "A dimly lit maintenance area.")
    loc.droid = DamagedMaintenanceDroid()
    loc.droid_present = True
    return loc

@pytest.fixture
def docking_bay():
    """Return a Location instance for Docking Bay."""
    return Location("Docking Bay", "A large area with spaceships.")

@pytest.fixture
def damaged_droid():
    """Return a DamagedMaintenanceDroid instance for testing."""
    return DamagedMaintenanceDroid()

@pytest.fixture
def player(maintenance_tunnels):
    """Return a Player instance for testing."""
    return Player(maintenance_tunnels)

@pytest.fixture
def game_controller():
    """Return a GameController instance for testing."""
    return GameController()
