"""Tests for item-related classes (StationItem, DiagnosticTool, EnergyCrystal)."""

import pytest
from rpg_game.game import StationItem, DiagnosticTool, EnergyCrystal


def test_station_item_initialization(sample_item):
    """
    Test that StationItem initializes with correct attributes.

    Args:
        sample_item (StationItem): A sample item for testing.

    Asserts:
        sample_item._name == "Test Item"
        sample_item._description == "A test item for unit testing."
    """
    assert sample_item._name == "Test Item"
    assert sample_item._description == "A test item for unit testing."


def test_station_item_examine(sample_item):
    """
    Test that examine() returns the item's description.

    Args:
        sample_item (StationItem): A sample item for testing.

    Asserts:
        sample_item.examine() == "A test item for unit testing."
    """
    assert sample_item.examine() == "A test item for unit testing."


def test_diagnostic_tool_initialization(diagnostic_tool):
    """
    Test that DiagnosticTool initializes with correct default values.

    Args:
        diagnostic_tool (DiagnosticTool): A diagnostic tool for testing.

    Asserts:
        diagnostic_tool._name == "Diagnostic Tool"
        "handheld device" in diagnostic_tool._description.lower()
    """
    assert diagnostic_tool._name == "Diagnostic Tool"
    assert "handheld device" in diagnostic_tool._description.lower()


def test_diagnostic_tool_examine(diagnostic_tool):
    """
    Test that DiagnosticTool's examine() provides a hint about its use.

    Args:
        diagnostic_tool (DiagnosticTool): A diagnostic tool for testing.

    Asserts:
        "maintenance droids" in diagnostic_tool.examine().lower()
    """
    assert "maintenance droids" in diagnostic_tool.examine().lower()


def test_energy_crystal_initialization(energy_crystal):
    """
    Test that EnergyCrystal initializes with correct default values.

    Args:
        energy_crystal (EnergyCrystal): An energy crystal for testing.

    Asserts:
        energy_crystal._name == "Energy Crystal"
        "glowing crystal" in energy_crystal._description.lower()
    """
    assert energy_crystal._name == "Energy Crystal"
    assert "glowing crystal" in energy_crystal._description.lower()


def test_energy_crystal_examine(energy_crystal):
    """
    Test that EnergyCrystal's examine() describes its appearance.

    Args:
        energy_crystal (EnergyCrystal): An energy crystal for testing.

    Asserts:
        "pulses" in energy_crystal.examine().lower()
        "unstable" in energy_crystal.examine().lower()
    """
    assert "pulses" in energy_crystal.examine().lower()
    assert "unstable" in energy_crystal.examine().lower()


def test_item_inheritance():
    """
    Test that tool and crystal are instances of StationItem.

    Asserts:
        isinstance(tool, StationItem)
        isinstance(crystal, StationItem)
    """
    tool = DiagnosticTool()
    crystal = EnergyCrystal()
    assert isinstance(tool, StationItem)
    assert isinstance(crystal, StationItem)
