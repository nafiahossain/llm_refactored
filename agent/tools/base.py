from abc import ABC, abstractmethod
from typing import Any, Dict

from ..schemas import ToolResult


class BaseTool(ABC):
    """Base class for all tools"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name"""
        pass

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> ToolResult:
        """Execute the tool with given arguments"""
        pass

    @abstractmethod
    def validate_args(self, args: Dict[str, Any]) -> bool:
        """Validate tool arguments"""
        pass
