"""
Module containing the Player class for the game's player character.
"""

from typing import Tuple
from .location import Location
from .droid import DamagedMaintenanceDroid

class Player:
    """
    Represents the player in the game, tracking their state, inventory, and score.
    """
    def __init__(self, starting_location: 'Location'):
        """
        Initialize a new player.
        
        Args:
            starting_location: The initial location of the player
        """
        self._current_location = starting_location
        self._has_tool = False
        self._has_crystal = False
        self._score = 0
        self._hazard_count = 0
        
    @property
    def current_location(self) -> 'Location':
        return self._current_location
        
    @current_location.setter
    def current_location(self, value: 'Location') -> None:
        self._current_location = value
        
    @property
    def has_tool(self) -> bool:
        return self._has_tool
        
    @has_tool.setter
    def has_tool(self, value: bool) -> None:
        self._has_tool = value
        
    @property
    def has_crystal(self) -> bool:
        return self._has_crystal
        
    @has_crystal.setter
    def has_crystal(self, value: bool) -> None:
        self._has_crystal = value
        
    @property
    def score(self) -> int:
        return self._score
        
    @score.setter
    def score(self, value: int) -> None:
        self._score = value
        
    @property
    def hazard_count(self) -> int:
        return self._hazard_count
        
    @hazard_count.setter
    def hazard_count(self, value: int) -> None:
        self._hazard_count = value
    
    def move(self, direction: str) -> bool:
        """
        Attempt to move the player in the specified direction.
        
        Args:
            direction: The direction to move (e.g., 'north', 'east')
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        # Normalize the direction: trim whitespace and convert to lowercase
        normalized_direction = direction.strip().lower()
        
        # Check if the direction is valid by looking for a case-insensitive match
        matching_direction = None
        for exit_dir in self.current_location.exits:
            if exit_dir.lower() == normalized_direction:
                matching_direction = exit_dir
                break
        
        if matching_direction is None:
            print(f"There is no exit to the {direction}.")
            return False
            
        # Check if the droid is blocking the path (eastward movement only)
        if (hasattr(self.current_location, 'droid_present') and 
            self.current_location.droid_present and 
            hasattr(self.current_location, 'droid') and 
            self.current_location.droid and 
            self.current_location.droid.is_blocking() and 
            normalized_direction == 'east'):
            print("A maintenance droid blocks your way!")
            self.hazard_count += 1
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
        if self.current_location.has_tool and not self.has_tool:
            self.current_location.has_tool = False
            self.has_tool = True
            self.score += 10
            print("You pick up the diagnostic tool.")
            return True
        elif self.has_tool:
            print("You already have the diagnostic tool.")
        else:
            print("There is no diagnostic tool here.")
        return False
    
    def use_tool_on_droid(self) -> bool:
        """
        Attempt to use the diagnostic tool on the droid.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.has_tool:
            print("You don't have a diagnostic tool.")
            return False
            
        if not (hasattr(self.current_location, 'droid_present') and self.current_location.droid_present):
            print("There's no droid here to use the tool on.")
            return False
            
        if not hasattr(self.current_location, 'droid') or self.current_location.droid is None:
            print("There's no droid here to use the tool on.")
            return False
            
        if not self.current_location.droid.is_blocking():
            print("The droid is already repaired.")
            return False
            
        self.current_location.droid.repair()
        self.current_location.droid_present = False  # Droid moves away after repair
        self.score += 20
        print("You use the diagnostic tool on the droid. It beeps and powers up!")
        print("The droid thanks you and moves out of the way.")
        return True
    
    def pick_up_crystal(self) -> bool:
        """
        Attempt to pick up the energy crystal from the current location.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_location.has_crystal and not self.has_crystal:
            self.current_location.has_crystal = False
            self.has_crystal = True
            self.score += 50
            print("You pick up the energy crystal.")
            return True
        elif self.has_crystal:
            print("You already have the energy crystal.")
        else:
            print("There is no energy crystal here.")
        return False
    
    def get_status(self) -> Tuple[int, int]:
        """
        Get the player's current score and hazard count.
        
        Returns:
            tuple: A tuple containing (score, hazard_count)
        """
        return (self.score, self.hazard_count)
