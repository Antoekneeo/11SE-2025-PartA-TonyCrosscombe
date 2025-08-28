"""
Main game module containing all game classes and logic.
"""

class StationItem:
    """
    Base class for all items in the game that can be picked up by the player.
    """
    def __init__(self, name: str, description: str):
        """
        Initialize a new station item.
        
        Args:
            name: The name of the item
            description: A description of the item
        """
        self._name = name
        self._description = description
    
    def examine(self) -> str:
        """
        Return a description of the item.
        
        Returns:
            A string describing the item
        """
        return self._description


class DiagnosticTool(StationItem):
    """
    A diagnostic tool used to repair the maintenance droid.
    """
    def __init__(self):
        """Initialize the diagnostic tool with default values."""
        super().__init__(
            name="Diagnostic Tool",
            description="A handheld device with various connectors and readouts."
        )
    
    def examine(self) -> str:
        """
        Return a hint about the tool's purpose.
        
        Returns:
            A string containing a hint about the tool
        """
        return "This diagnostic tool seems designed to interface with maintenance droids."


class EnergyCrystal(StationItem):
    """
    A volatile energy crystal that the player must collect.
    """
    def __init__(self):
        """Initialize the energy crystal with default values."""
        super().__init__(
            name="Energy Crystal",
            description="A glowing crystal that pulses with energy."
        )
    
    def examine(self) -> str:
        """
        Return a description of the crystal.
        
        Returns:
            A string describing the crystal's appearance
        """
        return "The crystal pulses with an unstable, vibrant energy."


class Location:
    """
    Represents a location in the game world that can contain items and connect to other locations.
    """
    def __init__(self, name: str, description: str):
        """
        Initialize a new location.
        
        Args:
            name: The name of the location
            description: A description of the location
        """
        self.name = name
        self.description = description
        self.exits = {}  # direction -> Location
        self.has_tool = False
        self.has_crystal = False
        self.droid_present = False
    
    def add_exit(self, direction: str, other_location: 'Location') -> None:
        """
        Add an exit to another location.
        
        Args:
            direction: The direction of the exit (e.g., 'north', 'east')
            other_location: The Location object this exit leads to
        """
        self.exits[direction.lower()] = other_location
    
    def describe(self) -> str:
        """
        Generate a description of the location and its contents.
        
        Returns:
            A formatted string describing the location
        """
        description_parts = [
            f"=== {self.name} ===",
            self.description
        ]
        
        # Add item descriptions if present
        if self.has_tool:
            description_parts.append("You see a diagnostic tool here.")
        if self.has_crystal:
            description_parts.append("You see an energy crystal here.")
        if self.droid_present:
            description_parts.append("A maintenance droid blocks the way!")
        
        # Add available exits
        if self.exits:
            exit_directions = ", ".join(self.exits.keys())
            description_parts.append(f"Exits: {exit_directions}.")
        
        return "\n".join(description_parts)
    
    def remove_tool(self) -> bool:
        """
        Remove the tool from this location if present.
        
        Returns:
            bool: True if a tool was removed, False otherwise
        """
        if self.has_tool:
            self.has_tool = False
            return True
        return False
    
    def remove_crystal(self) -> bool:
        """
        Remove the crystal from this location if present.
        
        Returns:
            bool: True if a crystal was removed, False otherwise
        """
        if self.has_crystal:
            self.has_crystal = False
            return True
        return False
    
    def set_droid_present(self, is_present: bool) -> None:
        """
        Set whether the droid is present in this location.
        
        Args:
            is_present: Whether the droid should be present
        """
        self.droid_present = is_present


class DamagedMaintenanceDroid:
    """
    Represents a damaged maintenance droid that blocks the player's path until repaired.
    """
    def __init__(self):
        """Initialize the droid in a blocking state."""
        self.blocking = True
    
    def repair(self) -> None:
        """
        Repair the droid, making it no longer block the path.
        """
        self.blocking = False
    
    def is_blocking(self) -> bool:
        """
        Check if the droid is currently blocking the path.
        
        Returns:
            bool: True if the droid is blocking, False otherwise
        """
        return self.blocking


class Player:
    """
    Represents the player in the game, tracking their state, inventory, and score.
    """
    def __init__(self, starting_location: Location):
        """
        Initialize a new player.
        
        Args:
            starting_location: The initial location of the player
        """
        self.current_location = starting_location
        self.has_tool = False
        self.has_crystal = False
        self.score = 0
        self.hazard_count = 0
    
    def move(self, direction: str) -> bool:
        """
        Attempt to move the player in the specified direction.
        
        Args:
            direction: The direction to move (e.g., 'north', 'east')
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        # Normalize the direction: trim whitespace and convert to lowercase
        direction = direction.strip().lower()
        
        # Check if the direction is valid by looking for a case-insensitive match
        matching_direction = None
        for exit_dir in self.current_location.exits:
            if exit_dir.lower() == direction:
                matching_direction = exit_dir
                break
        
        if matching_direction is None:
            print(f"There is no exit to the {direction}.")
            return False
            
        # Check if the droid is blocking the path (eastward movement only)
        if (self.current_location.droid_present and 
                matching_direction.lower() == 'east' and 
                hasattr(self.current_location, 'droid') and 
                self.current_location.droid.is_blocking()):
            self.hazard_count += 1
            print("A maintenance droid blocks your way!")
            return False
            
        # Move to the new location
        self.current_location = self.current_location.exits[matching_direction]
        print(f"You move {matching_direction} to {self.current_location.name}.")
        return True
    
    def pick_up_tool(self) -> bool:
        """
        Attempt to pick up the diagnostic tool from the current location.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_location.remove_tool():
            self.has_tool = True
            self.score += 10
            print("You pick up the diagnostic tool. (+10 points)")
            return True
        print("There is no tool here to pick up.")
        return False
    
    def use_tool_on_droid(self) -> bool:
        """
        Attempt to use the diagnostic tool on the droid.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.has_tool:
            print("You don't have a diagnostic tool to use!")
            return False
            
        if not self.current_location.droid_present:
            print("There's no droid here to repair!")
            return False
            
        # Create a temporary droid to repair
        droid = DamagedMaintenanceDroid()
        droid.repair()
        self.current_location.set_droid_present(False)
        self.score += 20
        print("You use the diagnostic tool on the droid. It powers down, no longer blocking the way. (+20 points)")
        return True
    
    def pick_up_crystal(self) -> bool:
        """
        Attempt to pick up the energy crystal from the current location.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_location.remove_crystal():
            self.has_crystal = True
            self.score += 50
            print("You pick up the energy crystal. (+50 points)")
            return True
        print("There is no crystal here to pick up.")
        return False
    
    def get_status(self) -> tuple[int, int]:
        """
        Get the player's current score and hazard count.
        
        Returns:
            tuple: A tuple containing (score, hazard_count)
        """
        return self.score, self.hazard_count


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
