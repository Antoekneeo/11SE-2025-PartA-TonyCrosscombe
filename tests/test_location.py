"""
Tests for the Location class.
"""
import pytest
from rpg_game.game.location import Location

def test_location_initialization(maintenance_tunnels):
    """Test that Location initializes with correct attributes."""
    assert maintenance_tunnels.name == "Maintenance Tunnels"
    assert "dimly lit" in maintenance_tunnels.description.lower()
    assert maintenance_tunnels.exits == {}
    assert maintenance_tunnels.has_tool is False
    assert maintenance_tunnels.has_crystal is False
    # Maintenance Tunnels should have a droid by default
    assert maintenance_tunnels.droid_present is True
    assert maintenance_tunnels.droid is not None

def test_add_exit(maintenance_tunnels, docking_bay):
    """Test adding an exit to a location."""
    maintenance_tunnels.add_exit("east", docking_bay)
    assert "east" in maintenance_tunnels.exits
    assert maintenance_tunnels.exits["east"] == docking_bay

def test_describe_empty_location():
    """Test describe() on a location with no items or exits."""
    # Create a location without any items or droid
    test_location = Location("Test Location", "A test location.")
    description = test_location.describe()
    assert "Test Location" in description
    assert "test location" in description.lower()
    assert "Exits:" not in description
    assert "tool" not in description.lower()
    assert "crystal" not in description.lower()
    assert "droid" not in description.lower()

def test_describe_with_items_and_exits():
    """Test describe() with items and exits."""
    # Create a test location with items and exits
    test_location = Location("Test Location", "A test location.")
    other_location = Location("Other Location", "Another location for testing.")
    
    # Add items and exits
    test_location.add_exit("north", other_location)
    test_location.has_tool = True
    test_location.has_crystal = True
    
    # Add a droid to the test location
    from rpg_game.game.droid import DamagedMaintenanceDroid
    test_location.droid = DamagedMaintenanceDroid()
    test_location.droid_present = True
    
    description = test_location.describe()
    assert "Test Location" in description
    assert "test location" in description
    assert "Exits: north" in description
    assert "diagnostic tool" in description.lower()
    assert "energy crystal" in description.lower()
    assert "maintenance droid" in description.lower()

def test_remove_tool(maintenance_tunnels):
    """Test removing the tool from a location."""
    maintenance_tunnels.has_tool = True
    assert maintenance_tunnels.remove_tool() is True
    assert maintenance_tunnels.has_tool is False
    assert maintenance_tunnels.remove_tool() is False

def test_remove_crystal(maintenance_tunnels):
    """Test removing the crystal from a location."""
    maintenance_tunnels.has_crystal = True
    assert maintenance_tunnels.remove_crystal() is True
    assert maintenance_tunnels.has_crystal is False
    assert maintenance_tunnels.remove_crystal() is False

def test_set_droid_present():
    """Test setting droid presence."""
    from rpg_game.game.droid import DamagedMaintenanceDroid
    
    # Create a test location
    test_location = Location("Test Location", "A test location.")
    
    # Initially no droid
    assert test_location.droid_present is False
    assert test_location.droid is None
    
    # Add a droid
    test_location.droid = DamagedMaintenanceDroid()
    test_location.droid_present = True
    assert test_location.droid_present is True
    assert test_location.droid is not None
    
    # Remove the droid
    test_location.droid_present = False
    assert test_location.droid_present is False
