import json
from typing import Any, Dict

from ..schemas import ToolResult
from .base import BaseTool


class KnowledgeBaseTool(BaseTool):
    """Knowledge base lookup tool"""

    def __init__(self, kb_path: str = "data/kb.json"):
        self.kb_path = kb_path

    @property
    def name(self) -> str:
        return "kb"

    def validate_args(self, args: Dict[str, Any]) -> bool:
        return "q" in args and isinstance(args["q"], str)

    def execute(self, args: Dict[str, Any]) -> ToolResult:
        if not self.validate_args(args):
            return ToolResult(
                success=False,
                result="",
                error="Invalid arguments. Expected 'q' field with string value.",
                tool_used=self.name,
            )

        try:
            query = args["q"].lower().strip()
            result = self._lookup(query)
            return ToolResult(success=True, result=result, tool_used=self.name)
        except Exception as e:
            return ToolResult(
                success=False,
                result="",
                error=f"Knowledge base error: {str(e)}",
                tool_used=self.name,
            )

    def _lookup(self, query: str) -> str:
        """Look up information in the knowledge base"""
        try:
            with open(self.kb_path, "r") as f:
                data = json.load(f)

            for item in data.get("entries", []):
                if query in item.get("name", "").lower():
                    return item.get("summary", "")

            return "No entry found."
        except FileNotFoundError:
            return "Knowledge base not found."
        except json.JSONDecodeError:
            return "Knowledge base format error."
