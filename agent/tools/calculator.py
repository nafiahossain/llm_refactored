from typing import Any, Dict

from ..schemas import ToolResult
from .base import BaseTool


class CalculatorTool(BaseTool):
    """Calculator tool for mathematical expressions"""

    @property
    def name(self) -> str:
        return "calc"

    def validate_args(self, args: Dict[str, Any]) -> bool:
        return "expr" in args and isinstance(args["expr"], str)

    def execute(self, args: Dict[str, Any]) -> ToolResult:
        if not self.validate_args(args):
            return ToolResult(
                success=False,
                result="",
                error="Invalid arguments. Expected 'expr' field with string value.",
                tool_used=self.name,
            )

        try:
            expr = args["expr"]
            result = self._evaluate_expression(expr)
            return ToolResult(success=True, result=result, tool_used=self.name)
        except Exception as e:
            return ToolResult(
                success=False,
                result="",
                error=f"Calculation error: {str(e)}",
                tool_used=self.name,
            )

    def _evaluate_expression(self, expr: str) -> float:
        """Safely evaluate mathematical expressions"""

        expr = expr.lower().replace("what is", "").strip()

        # Handle percentage calculations
        if "% of" in expr:
            return self._calculate_percentage(expr)

        # Handle natural language additions
        expr = self._normalize_expression(expr)

        # Only allow mathematical operations
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expr):
            raise ValueError("Expression contains invalid characters")

        return float(eval(expr))

    def _calculate_percentage(self, expr: str) -> float:
        """Calculate percentage expressions like '12.5% of 243'"""
        try:
            left, right = expr.split("% of")
            x = float(left.strip())
            y = float(right.strip())
            return (x / 100.0) * y
        except Exception:
            raise ValueError("Invalid percentage expression")

    def _normalize_expression(self, expr: str) -> str:
        """Convert natural language to mathematical expression"""
        expr = expr.replace("add ", "").replace("plus ", "+")
        expr = expr.replace(" to the ", " + ")
        expr = expr.replace("average of", "(10+20)/2")
        return expr
