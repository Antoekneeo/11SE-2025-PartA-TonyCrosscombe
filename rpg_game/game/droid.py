"""
Module containing the DamagedMaintenanceDroid class for the game.
"""


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
