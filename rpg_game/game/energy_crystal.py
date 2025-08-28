"""
Module containing the EnergyCrystal class for the game.
"""

from .station_item import StationItem


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
        return f"{self._description} It looks unstable and dangerous."
