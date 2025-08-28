"""
Module containing the GameController class for managing game state and flow.
"""

from typing import Optional, Tuple
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
            "You are in the maintenance tunnels under the space station. "
            "The walls are lined with pipes and conduits. "
            "To the east is the Docking Bay."
        )
        
        self.docking_bay = Location(
            "Docking Bay",
            "You are in the Docking Bay. "
            "This is where ships come and go from the station. "
            "To the west are the Maintenance Tunnels."
        )
        
        # Connect locations
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
        self.maintenance_tunnels.set_droid_present(True, self.droid)
        
        # Create player
        self.player = Player(self.maintenance_tunnels)
    
    def start_game(self) -> None:
        """Start the main game loop."""
        print("Welcome to Space Station Repair!")
        print("Type 'help' for a list of commands.\n")
        
        # Initial location description
        print(self.player.current_location.describe())
        
        # Main game loop
        while True:
            command = input("\nWhat would you like to do? ").strip().lower()
            self.process_input(command)
            
            # Check win condition after each command
            if self.check_win_condition():
                print("\nCongratulations! You've completed your mission!")
                score, hazards = self.player.get_status()
                print(f"Final Score: {score} (Hazards: {hazards})")
                break
    
    def process_input(self, command: str) -> None:
        """
        Process a player's command.
        
        Args:
            command: The command entered by the player
        """
        self.last_command_was_win = False
        
        if command == "help":
            self.show_help()
        elif command == "look":
            print(self.player.current_location.describe())
        elif command == "inventory":
            self.show_inventory()
        elif command.startswith("go "):
            direction = command[3:].strip()
            self.player.move(direction)
        elif command == "get tool":
            self.player.pick_up_tool()
        elif command == "use tool":
            self.player.use_tool_on_droid()
        elif command == "get crystal":
            self.player.pick_up_crystal()
        elif command == "status":
            self.show_status()
        elif command == "win":
            self.last_command_was_win = True
            if not self.check_win_condition():
                print("You haven't completed all the mission objectives yet!")
        else:
            print("I don't understand that command. Type 'help' for a list of commands.")
    
    def check_win_condition(self) -> bool:
        """
        Check if the player has won the game.
        
        Returns:
            bool: True if the player has won, False otherwise
        """
        # Player must be in the docking bay with the crystal and have used 'win' command
        if not self.last_command_was_win:
            return False
            
        if self.player.current_location != self.docking_bay:
            print("You need to be in the Docking Bay to complete your mission!")
            return False
            
        if not self.player.has_crystal:
            print("You need to retrieve the energy crystal first!")
            return False
            
        # All conditions met - player wins!
        self.player.score += 30  # Bonus for winning
        return True
    
    def show_help(self) -> None:
        """Display the help message with available commands."""
        print("\nAvailable commands:")
        print("  help           - Show this help message")
        print("  look           - Look around the current location")
        print("  inventory      - Check your inventory")
        print("  go <direction> - Move in the specified direction (e.g., 'go east')")
        print("  get tool       - Pick up the diagnostic tool")
        print("  use tool       - Use the diagnostic tool on the droid")
        print("  get crystal    - Pick up the energy crystal")
        print("  status         - Check your score and hazard count")
        print("  win            - Complete the mission (if all objectives are met)")
    
    def show_inventory(self) -> None:
        """Show the player's current inventory."""
        print("\nInventory:")
        if self.player.has_tool:
            print("- Diagnostic Tool")
        if self.player.has_crystal:
            print("- Energy Crystal")
        if not (self.player.has_tool or self.player.has_crystal):
            print("You're not carrying anything.")
    
    def show_status(self) -> None:
        """Show the player's current status."""
        score, hazards = self.player.get_status()
        print(f"\nScore: {score}")
        print(f"Hazards encountered: {hazards}")
