import pytest
from pydantic import ValidationError

from agent.schemas import ToolPlan, ToolResult, ToolType


class TestSchemas:
    def test_valid_tool_plan(self):
        plan = ToolPlan(tool=ToolType.CALC, args={"expr": "1+1"}, confidence=0.9)
        assert plan.tool == ToolType.CALC
        assert plan.args == {"expr": "1+1"}
        assert plan.confidence == 0.9

    def test_invalid_tool_type(self):
        with pytest.raises(ValidationError):
            ToolPlan(tool="invalid_tool", args={})

    def test_confidence_bounds(self):
        # Valid confidence
        plan = ToolPlan(tool=ToolType.CALC, args={}, confidence=0.5)
        assert plan.confidence == 0.5

        # Invalid confidence (too high)
        with pytest.raises(ValidationError):
            ToolPlan(tool=ToolType.CALC, args={}, confidence=1.5)

        # Invalid confidence (negative)
        with pytest.raises(ValidationError):
            ToolPlan(tool=ToolType.CALC, args={}, confidence=-0.1)

    def test_tool_result(self):
        result = ToolResult(success=True, result="test result", tool_used="test_tool")
        assert result.success
        assert result.result == "test result"
        assert result.error is None
