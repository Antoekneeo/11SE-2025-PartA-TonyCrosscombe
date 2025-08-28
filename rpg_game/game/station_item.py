"""
Module containing the base StationItem class for all game items.
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
