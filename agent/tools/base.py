from abc import ABC, abstractmethod
from typing import Any, Dict

from ..schemas import ToolResult


class BaseTool(ABC):
    """Base class for all tools"""

    @property
    @abstractmethod
    def name(self) -> str:  # pragma: no cover
        """Tool name"""
        pass

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> ToolResult:  # pragma: no cover
        """Execute the tool with given arguments"""
        pass

    @abstractmethod
    def validate_args(self, args: Dict[str, Any]) -> bool:  # pragma: no cover
        """Validate tool arguments"""
        pass
