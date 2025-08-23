from typing import Dict, Optional

from .tools import CalculatorTool, KnowledgeBaseTool, TranslatorTool, WeatherTool
from .tools.base import BaseTool


class ToolRegistry:
    """Registry for managing available tools"""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register default tools"""
        default_tools = [
            CalculatorTool(),
            WeatherTool(),
            KnowledgeBaseTool(),
            TranslatorTool(),
        ]

        for tool in default_tools:
            self.register_tool(tool)

    def register_tool(self, tool: BaseTool):
        """Register a new tool"""
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name"""
        return self._tools.get(name)

    def list_tools(self) -> Dict[str, BaseTool]:
        """List all registered tools"""
        return self._tools.copy()
