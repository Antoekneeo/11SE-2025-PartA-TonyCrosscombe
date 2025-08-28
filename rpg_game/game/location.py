"""
Module containing the Location class for game locations.
"""

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
        self._name = name
        self._description = description
        self._exits = {}  # direction -> Location
        self._has_tool = False
        self._has_crystal = False
        self._droid_present = False
        self._droid = None
        
    @property
    def name(self) -> str:
        return self._name
        
    @property
    def description(self) -> str:
        return self._description
        
    @property
    def exits(self) -> dict:
        return self._exits
        
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
    def droid_present(self) -> bool:
        return self._droid_present
        
    @droid_present.setter
    def droid_present(self, value: bool) -> None:
        self._droid_present = value
        
    @property
    def droid(self):
        return self._droid
        
    @droid.setter
    def droid(self, value):
        self._droid = value
    
    def add_exit(self, direction: str, other_location: 'Location') -> None:
        """
        Add an exit to another location.
        
        Args:
            direction: The direction of the exit (e.g., 'north', 'east')
            other_location: The Location object this exit leads to
        """
        self._exits[direction] = other_location
    
    def describe(self) -> str:
        """
        Generate a description of the location and its contents.
        
        Returns:
            A formatted string describing the location
        """
        description = f"{self.name}\n{'-' * len(self.name)}\n{self.description}"
        
        # Add information about items in the location
        if self._has_tool:
            description += "\n\nYou see a diagnostic tool on the ground."
        if self._has_crystal:
            description += "\n\nA glowing energy crystal is placed on a pedestal."
        if self._droid_present and self._droid and self._droid.is_blocking():
            description += "\n\nA damaged maintenance droid is blocking the east exit."
        
        # List available exits
        if self._exits:
            exits = ", ".join(self._exits.keys())
            description += f"\n\nExits: {exits}"
        
        return description
    
    def remove_tool(self) -> bool:
        """
        Remove the tool from this location if present.
        
        Returns:
            bool: True if a tool was removed, False otherwise
        """
        if self._has_tool:
            self._has_tool = False
            return True
        return False
    
    def remove_crystal(self) -> bool:
        """
        Remove the crystal from this location if present.
        
        Returns:
            bool: True if a crystal was removed, False otherwise
        """
        if self._has_crystal:
            self._has_crystal = False
            return True
        return False
    
    def set_droid_present(self, is_present: bool, droid=None) -> None:
        """
        Set whether the droid is present in this location.
        
        Args:
            is_present: Whether the droid should be present
            droid: The droid object (if any)
        """
        self._droid_present = is_present
        if is_present and droid:
            self._droid = droid
