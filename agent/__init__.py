from .agent import Agent, answer
from .schemas import ToolPlan, ToolResult, ToolType
from .tool_registry import ToolRegistry

__version__ = "1.0.0"
__all__ = [
    "Agent",
    "answer",  # Backward compatibility
    "ToolPlan",
    "ToolResult",
    "ToolType",
    "ToolRegistry",
]
