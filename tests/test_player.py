"""
Tests for the Player class.
"""
import pytest

def test_player_initialization(player, maintenance_tunnels):
    """Test that Player initializes with correct default values."""
    assert player.current_location == maintenance_tunnels
    assert player.has_tool is False
    assert player.has_crystal is False
    assert player.score == 0
    assert player.hazard_count == 0

def test_move_successful(player, maintenance_tunnels, docking_bay):
    """Test successful movement between locations."""
    maintenance_tunnels.add_exit("east", docking_bay)
    assert player.move("east") is True
    assert player.current_location == docking_bay

def test_move_blocked_by_droid(player, maintenance_tunnels, docking_bay):
    """Test movement blocked by droid increments hazard count."""
    from rpg_game.game import DamagedMaintenanceDroid
    
    maintenance_tunnels.add_exit("east", docking_bay)
    maintenance_tunnels.droid_present = True
    maintenance_tunnels.droid = DamagedMaintenanceDroid()
    
    assert player.move("east") is False
    assert player.hazard_count == 1
    assert player.current_location == maintenance_tunnels

def test_move_invalid_direction(player):
    """Test moving in an invalid direction."""
    assert player.move("north") is False
    assert player.hazard_count == 0

def test_pick_up_tool_success(player, maintenance_tunnels):
    """Test successfully picking up the tool."""
    maintenance_tunnels.has_tool = True
    assert player.pick_up_tool() is True
    assert player.has_tool is True
    assert player.score == 10
    assert maintenance_tunnels.has_tool is False

def test_pick_up_tool_none_available(player):
    """Test attempting to pick up a tool when none is available."""
    assert player.pick_up_tool() is False
    assert player.has_tool is False
    assert player.score == 0

def test_use_tool_on_droid_success(player, maintenance_tunnels):
    """Test successfully using the tool on the droid."""
    player.has_tool = True
    maintenance_tunnels.droid_present = True
    
    assert player.use_tool_on_droid() is True
    assert maintenance_tunnels.droid_present is False
    assert player.score == 20

def test_use_tool_no_tool(player, maintenance_tunnels):
    """Test using tool on droid without having the tool."""
    maintenance_tunnels.droid_present = True
    assert player.use_tool_on_droid() is False
    assert maintenance_tunnels.droid_present is True
    assert player.score == 0

def test_use_tool_no_droid(player):
    """Test using tool when no droid is present."""
    player.has_tool = True
    assert player.use_tool_on_droid() is False
    assert player.score == 0

def test_pick_up_crystal_success(player, maintenance_tunnels):
    """Test successfully picking up the crystal."""
    maintenance_tunnels.has_crystal = True
    assert player.pick_up_crystal() is True
    assert player.has_crystal is True
    assert player.score == 50
    assert maintenance_tunnels.has_crystal is False

def test_pick_up_crystal_none_available(player):
    """Test attempting to pick up a crystal when none is available."""
    assert player.pick_up_crystal() is False
    assert player.has_crystal is False
    assert player.score == 0

def test_get_status(player):
    """Test getting the player's status."""
    player.score = 100
    player.hazard_count = 3
    score, hazards = player.get_status()
    assert score == 100
    assert hazards == 3
