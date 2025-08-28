"""
Edge case tests for the Player class.
"""
import pytest
from rpg_game.game import DamagedMaintenanceDroid

def test_move_case_insensitive(player, maintenance_tunnels, docking_bay):
    """Test that movement works with case-insensitive directions."""
    # Add exits in both directions
    maintenance_tunnels.add_exit("east", docking_bay)
    docking_bay.add_exit("west", maintenance_tunnels)
    
    # Test moving east with different cases
    assert player.move("EAST") is True
    assert player.current_location == docking_bay
    
    # Test moving back west with different case
    assert player.move("WEST") is True
    assert player.current_location == maintenance_tunnels

def test_move_whitespace_handling(player, maintenance_tunnels, docking_bay):
    """Test that movement works with extra whitespace in direction."""
    maintenance_tunnels.add_exit("east", docking_bay)
    assert player.move("  east  ") is True
    assert player.current_location == docking_bay

def test_pick_up_tool_multiple_attempts(player, maintenance_tunnels):
    """Test that tool can only be picked up once from a location."""
    maintenance_tunnels.has_tool = True
    
    # First attempt should succeed
    assert player.pick_up_tool() is True
    assert player.has_tool is True
    assert maintenance_tunnels.has_tool is False
    
    # Second attempt should fail
    assert player.pick_up_tool() is False
    assert player.score == 10  # Should only get points once

def test_pick_up_crystal_multiple_attempts(player, docking_bay):
    """Test that crystal can only be picked up once from a location."""
    player.current_location = docking_bay
    docking_bay.has_crystal = True
    
    # First attempt should succeed
    assert player.pick_up_crystal() is True
    assert player.has_crystal is True
    assert docking_bay.has_crystal is False
    
    # Second attempt should fail
    assert player.pick_up_crystal() is False
    assert player.score == 50  # Should only get points once

def test_use_tool_on_droid_multiple_attempts(player, maintenance_tunnels):
    """Test that tool can only be used once on droid."""
    maintenance_tunnels.droid_present = True
    player.has_tool = True
    
    # First attempt should succeed
    assert player.use_tool_on_droid() is True
    assert player.score == 20  # Points for using tool
    
    # Second attempt should fail (droid already repaired)
    assert player.use_tool_on_droid() is False
    assert player.score == 20  # No additional points

def test_move_after_droid_repaired(player, maintenance_tunnels, docking_bay):
    """Test that player can move past droid after it's been repaired."""
    # Set up exits and droid
    maintenance_tunnels.add_exit("east", docking_bay)
    docking_bay.add_exit("west", maintenance_tunnels)
    maintenance_tunnels.droid_present = True
    maintenance_tunnels.droid = DamagedMaintenanceDroid()
    player.has_tool = True
    
    # First attempt should be blocked by droid
    assert player.move("east") is False
    assert player.hazard_count == 1
    assert player.current_location == maintenance_tunnels
    
    # Repair the droid
    maintenance_tunnels.droid.repair()
    assert maintenance_tunnels.droid.is_blocking() is False
    
    # Now should be able to move east
    assert player.move("east") is True
    assert player.current_location == docking_bay
    assert player.hazard_count == 1  # No increment after repair
