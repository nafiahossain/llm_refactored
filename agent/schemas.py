from enum import Enum
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field


class ToolType(str, Enum):
    CALC = "calc"
    WEATHER = "weather"
    KB = "kb"
    TRANSLATOR = "translator"


class ToolPlan(BaseModel):
    """Schema for tool execution plans"""

    tool: ToolType
    args: Dict[str, Any]
    confidence: Optional[float] = Field(default=1.0, ge=0.0, le=1.0)


class ToolResult(BaseModel):
    """Schema for tool execution results"""

    success: bool
    result: Union[str, float, Dict[str, Any]]
    error: Optional[str] = None
    tool_used: str
