"""
Tests for the Location class.
"""
import pytest

def test_location_initialization(maintenance_tunnels):
    """Test that Location initializes with correct attributes."""
    assert maintenance_tunnels.name == "Maintenance Tunnels"
    assert "dimly lit" in maintenance_tunnels.description.lower()
    assert maintenance_tunnels.exits == {}
    assert maintenance_tunnels.has_tool is False
    assert maintenance_tunnels.has_crystal is False
    assert maintenance_tunnels.droid_present is False

def test_add_exit(maintenance_tunnels, docking_bay):
    """Test adding an exit to a location."""
    maintenance_tunnels.add_exit("east", docking_bay)
    assert "east" in maintenance_tunnels.exits
    assert maintenance_tunnels.exits["east"] == docking_bay

def test_describe_empty_location(maintenance_tunnels):
    """Test describe() on an empty location."""
    description = maintenance_tunnels.describe()
    assert "Maintenance Tunnels" in description
    assert "dimly lit" in description
    assert "Exits:" not in description
    assert "tool" not in description.lower()
    assert "crystal" not in description.lower()
    assert "droid" not in description.lower()

def test_describe_with_items_and_exits(maintenance_tunnels, docking_bay):
    """Test describe() with items and exits."""
    maintenance_tunnels.add_exit("east", docking_bay)
    maintenance_tunnels.has_tool = True
    maintenance_tunnels.has_crystal = True
    maintenance_tunnels.droid_present = True
    
    description = maintenance_tunnels.describe()
    assert "Exits: east" in description
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

def test_set_droid_present(maintenance_tunnels):
    """Test setting droid presence."""
    maintenance_tunnels.set_droid_present(True)
    assert maintenance_tunnels.droid_present is True
    maintenance_tunnels.set_droid_present(False)
    assert maintenance_tunnels.droid_present is False
