"""
Edge case tests for the GameController class.
"""
import pytest
from unittest.mock import patch, MagicMock
from rpg_game.game.game_controller import GameController

def test_process_input_unknown_command(game_controller, capsys):
    """Test that unknown commands are handled gracefully."""
    game_controller.process_input("invalid command")
    captured = capsys.readouterr()
    assert "don't understand that command" in captured.out.lower()

def test_win_condition_not_in_docking_bay(game_controller, capsys):
    """Test win condition when not in docking bay."""
    game_controller.player.has_crystal = True
    game_controller.last_command_was_win = True
    
    # Should not win when not in docking bay
    assert game_controller.check_win_condition() is False
    captured = capsys.readouterr()
    assert "You need to be in the Docking Bay to complete your mission!" in captured.out

def test_win_condition_no_crystal(game_controller, capsys):
    """Test win condition without crystal."""
    # Move player to docking bay
    game_controller.player.current_location = game_controller.docking_bay
    game_controller.last_command_was_win = True
    
    # Should not win without crystal
    assert game_controller.check_win_condition() is False
    captured = capsys.readouterr()
    assert "You need to retrieve the energy crystal first!" in captured.out

def test_invalid_move_direction(game_controller, capsys):
    """Test handling of invalid move directions."""
    # Call the method that processes input
    game_controller.process_input("go north")
    
    # Verify invalid move message was printed
    captured = capsys.readouterr()
    assert "no exit" in captured.out.lower() or "can't go" in captured.out.lower()

def test_pick_up_tool_twice(game_controller, capsys):
    """Test examining the tool multiple times."""
    # Set up the test: ensure the current location has the tool
    game_controller.player.current_location.has_tool = True

    # First look should show the tool
    game_controller.process_input("look")
    first_output = capsys.readouterr().out
    assert "diagnostic tool" in first_output.lower()
    
    # Second look should still show the tool
    game_controller.process_input("look")
    second_output = capsys.readouterr().out
    assert "diagnostic tool" in second_output.lower()

def test_use_tool_without_picking_up(game_controller, capsys):
    """Test using tool without having picked it up."""
    # Ensure the player doesn't have the tool
    game_controller.player.has_tool = False
    
    # Try to use the tool without having it
    game_controller.process_input("use tool")
    captured = capsys.readouterr()
    assert "you don't have a diagnostic tool" in captured.out.lower()

def test_win_sequence(game_controller, capsys):
    """Test the win condition check."""
    # Set up win conditions
    game_controller.player.current_location = game_controller.docking_bay
    game_controller.player.has_crystal = True
    game_controller.last_command_was_win = True
    
    # Check win condition directly
    assert game_controller.check_win_condition() is True
    
    # Verify the score was updated (30 points for winning)
    assert game_controller.player.score == 30  # Just the win bonus
