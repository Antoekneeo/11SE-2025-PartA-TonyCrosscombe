"""
Module containing the DiagnosticTool class for the game.
"""

from .station_item import StationItem


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
        return f"{self._description} It might be useful for repairing maintenance droids."
