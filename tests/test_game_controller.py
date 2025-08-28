"""Tests for the GameController class."""

import pytest
from unittest.mock import patch, MagicMock
from rpg_game.game.game_controller import GameController


def test_game_controller_initialization(game_controller):
    """
    Test that GameController initializes with correct attributes.

    Args:
        game_controller (GameController): A GameController instance for testing.

    Asserts:
        game_controller.maintenance_tunnels is not None
        game_controller.docking_bay is not None
        game_controller.player is not None
        game_controller.droid is not None
    """
    assert game_controller.maintenance_tunnels is not None
    assert game_controller.docking_bay is not None
    assert game_controller.player is not None
    assert game_controller.droid is not None


def test_setup_world(game_controller):
    """
    Test that the game world is set up correctly.

    Args:
        game_controller (GameController): A GameController instance for testing.

    Asserts:
        Maintenance Tunnels and Docking Bay are properly initialized
        Connections between locations are correctly set up
        Initial items are in their correct locations
    """
    # Check locations
    assert game_controller.maintenance_tunnels.name == "Maintenance Tunnels"
    assert game_controller.docking_bay.name == "Docking Bay"
    
    # Check connections
    assert "east" in game_controller.maintenance_tunnels.exits
    assert "west" in game_controller.docking_bay.exits
    
    # Check initial items
    assert game_controller.maintenance_tunnels.has_tool is True
    assert game_controller.docking_bay.has_crystal is True
    assert game_controller.maintenance_tunnels.droid_present is True


def test_process_input_move(game_controller):
    """
    Test processing a move command.

    Args:
        game_controller: A GameController instance for testing

    Asserts:
        The player's move method is called with the correct direction
    """
    # Setup
    game_controller.player.move = MagicMock(return_value=True)
    
    # Test valid move
    game_controller.process_input("go east")
    game_controller.player.move.assert_called_once_with("east")


def test_check_win_condition_not_met(game_controller):
    """
    Test win condition when not met.

    Args:
        game_controller: A GameController instance for testing

    Asserts:
        check_win_condition returns False when win conditions are not met
    """
    assert game_controller.check_win_condition() is False


def test_check_win_condition_met(game_controller):
    """
    Test win condition when met.

    Args:
        game_controller: A GameController instance for testing

    Asserts:
        check_win_condition returns True when all win conditions are met
    """
    # Setup win condition
    game_controller.player.current_location = game_controller.docking_bay
    game_controller.player.has_crystal = True
    game_controller.last_command_was_win = True
    
    assert game_controller.check_win_condition() is True


@patch('builtins.print')
def test_show_help(mock_print, game_controller):
    """
    Test that the help text is displayed correctly.

    Args:
        mock_print: Mock for the print function
        game_controller: A GameController instance for testing

    Asserts:
        All expected command help text is included in the output
    """
    game_controller.show_help()

    # Verify help text was printed
    help_output = str(mock_print.call_args_list).lower()
    expected_commands = [
        "available commands",
        "help",
        "look",
        "status",
        "win"
    ]

    for cmd in expected_commands:
        assert cmd in help_output
