"""
Main game module containing the GameController class.
"""

from typing import Tuple
from .location import Location
from .player import Player
from .droid import DamagedMaintenanceDroid
from .diagnostic_tool import DiagnosticTool
from .energy_crystal import EnergyCrystal


class GameController:
    """
    Controls the main game loop and manages game state.
    """
    def __init__(self):
        """Initialize the game world and player."""
        self.maintenance_tunnels = None
        self.docking_bay = None
        self.droid = None
        self.player = None
        self.diagnostic_tool = None
        self.energy_crystal = None
        self.last_command_was_win = False
        self.setup_world()
    
    def setup_world(self) -> None:
        """Set up the game world with locations, items, and the player."""
        # Create locations
        self.maintenance_tunnels = Location(
            "Maintenance Tunnels",
            "You are in the dimly lit maintenance tunnels. Various pipes and conduits line the walls."
        )
        self.docking_bay = Location(
            "Docking Bay",
            "You've entered the spacious docking bay. Ships of various sizes are docked here."
        )
        
        # Set up exits
        self.maintenance_tunnels.add_exit("east", self.docking_bay)
        self.docking_bay.add_exit("west", self.maintenance_tunnels)
        
        # Set up items and droid
        self.maintenance_tunnels.has_tool = True
        self.docking_bay.has_crystal = True
        
        # Create game objects
        self.droid = DamagedMaintenanceDroid()
        self.diagnostic_tool = DiagnosticTool()
        self.energy_crystal = EnergyCrystal()
        
        # Place droid in the maintenance tunnels
        self.maintenance_tunnels.set_droid_present(True)
        
        # Create player
        self.player = Player(self.maintenance_tunnels)
    
    def start_game(self) -> None:
        """Start the main game loop."""
        print("=== Space Station RPG ===")
        print("Your mission: Collect the energy crystal and escape!")
        print("Type 'help' for a list of commands.\n")
        
        while True:
            # Print current location description
            print("\n" + self.player.current_location.describe())
            
            # Get player input
            command = input("\n> ").strip().lower()
            
            # Process the command
            self.process_input(command)
            
            # Check win condition
            if self.check_win_condition():
                break
    
    def process_input(self, command: str) -> None:
        """
        Process a player's command.
        
        Args:
            command: The command entered by the player
        """
        self.last_command_was_win = (command == "win")
        
        if command == "help":
            self.show_help()
        elif command.startswith("move "):
            direction = command[5:].strip()
            if direction:
                self.player.move(direction)
            else:
                print("Please specify a direction to move.")
        elif command == "pick up tool":
            self.player.pick_up_tool()
        elif command == "use tool":
            self.player.use_tool_on_droid()
        elif command == "pick up crystal":
            self.player.pick_up_crystal()
        elif command == "status":
            score, hazards = self.player.get_status()
            print(f"Score: {score} | Hazards: {hazards}")
        elif command == "win":
            pass  # Handled in check_win_condition()
        else:
            print("Invalid command. Type 'help' for a list of commands.")
    
    def check_win_condition(self) -> bool:
        """
        Check if the player has won the game.
        
        Returns:
            bool: True if the player has won, False otherwise
        """
        if (self.player.current_location == self.docking_bay and 
                self.player.has_crystal and 
                self.last_command_was_win):
            self.player.score += 30  # Add win bonus
            print("\n=== Congratulations! You've won! ===")
            score, hazards = self.player.get_status()
            print(f"Final Score: {score} | Hazards: {hazards}")  # Now shows 110
            if hazards == 0:
                print("Perfect! You completed the mission with no hazards!")
            return True
        elif self.last_command_was_win:
            print("You can't win yet! Make sure you're in the Docking Bay with the crystal.")
            # Show current score for feedback
            score, hazards = self.player.get_status()
            print(f"Current Score: {score} | Hazards: {hazards}")
        return False
    
    @staticmethod
    def show_help() -> None:
        """Display the help message with available commands."""
        print("\nAvailable commands:")
        print("  move <direction>  - Move in the specified direction (e.g., 'move east')")
        print("  pick up tool      - Pick up the diagnostic tool")
        print("  use tool          - Use the diagnostic tool on the droid")
        print("  pick up crystal   - Pick up the energy crystal")
        print("  status            - Show your current score and hazard count")
        print("  win               - Attempt to complete the mission")
        print("  help              - Show this help message")
        print("  quit              - Quit the game")
        print("\nObjective: Collect the energy crystal and return to the Docking Bay to win!")
