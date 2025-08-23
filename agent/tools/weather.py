from typing import Any, Dict

from ..schemas import ToolResult
from .base import BaseTool


class WeatherTool(BaseTool):
    """Weather tool for temperature queries"""

    # Mock temperature data
    _TEMPS = {
        "paris": 18.0,
        "london": 17.0,
        "dhaka": 31.0,
        "amsterdam": 19.5,
        "new york": 15.0,
        "tokyo": 22.0,
    }

    @property
    def name(self) -> str:
        return "weather"

    def validate_args(self, args: Dict[str, Any]) -> bool:
        return "city" in args and isinstance(args["city"], str)

    def execute(self, args: Dict[str, Any]) -> ToolResult:
        if not self.validate_args(args):
            return ToolResult(
                success=False,
                result="",
                error="Invalid arguments. Expected 'city' field with string value.",
                tool_used=self.name,
            )

        try:
            city = args["city"].lower().strip()
            temp = self._get_temperature(city)
            return ToolResult(success=True, result=temp, tool_used=self.name)
        except Exception as e:
            return ToolResult(
                success=False,
                result="",
                error=f"Weather lookup error: {str(e)}",
                tool_used=self.name,
            )

    def _get_temperature(self, city: str) -> float:
        """Get temperature for a city"""
        temp = self._TEMPS.get(city, 20.0)  # Default
        return float(temp)
