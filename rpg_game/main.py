#!/usr/bin/env python3
"""
Main entry point for the Space Station RPG game.
"""
from rpg_game.game.game_controller import GameController

def main():
    """
    Initialize and start the game.
    """
    try:
        game = GameController()
        game.start_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("The game will now exit.")

if __name__ == "main":
    main()
