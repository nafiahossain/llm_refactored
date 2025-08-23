import json
import logging
import re
from typing import Any, Dict, Optional, Union

from .schemas import ToolPlan, ToolType

logger = logging.getLogger(__name__)


class ResponseParser:
    """Parser for handling various LLM response formats"""

    @staticmethod
    def parse_response(
        response: Union[str, dict, ToolPlan],
    ) -> Optional[Union[str, ToolPlan]]:
        """Parse LLM response into either a direct answer or tool plan"""
        if isinstance(response, ToolPlan):
            return response

        if isinstance(response, dict):
            return ResponseParser._parse_dict_response(response)

        if isinstance(response, str):
            return ResponseParser._parse_string_response(response)

        return None

    @staticmethod
    def _parse_dict_response(response: Dict[str, Any]) -> Optional[ToolPlan]:
        """Parse dictionary response into ToolPlan"""
        try:
            if "tool" in response and "args" in response:
                tool_name = response["tool"]

                # Handle common typos
                if tool_name == "weaher":
                    tool_name = "weather"

                # Validate tool type
                try:
                    tool_type = ToolType(tool_name)
                except ValueError:
                    logger.warning(f"Invalid tool type: {tool_name}")
                    return None

                return ToolPlan(
                    tool=tool_type,
                    args=response["args"],
                    confidence=response.get("confidence", 1.0),
                )
        except Exception as e:
            logger.warning(f"Error parsing dict response: {e}")

        return None

    @staticmethod
    def _parse_string_response(response: str) -> Optional[Union[str, ToolPlan]]:
        """Parse string response - could be JSON, structured text, or direct answer"""
        # Parse as JSON first
        json_plan = ResponseParser._try_parse_json(response)
        if json_plan:
            return json_plan

        # Parse structured format like "TOOL:calc EXPR=..."
        structured_plan = ResponseParser._try_parse_structured(response)
        if structured_plan:
            return structured_plan

        return response.strip()

    @staticmethod
    def _try_parse_json(response: str) -> Optional[ToolPlan]:
        """Attempt to parse as JSON, with error recovery"""
        try:
            data = json.loads(response)
            return ResponseParser._parse_dict_response(data)
        except json.JSONDecodeError:
            # Fix common JSON errors
            fixed_response = ResponseParser._fix_common_json_errors(response)
            if fixed_response != response:
                try:
                    data = json.loads(fixed_response)
                    return ResponseParser._parse_dict_response(data)
                except json.JSONDecodeError:
                    pass

        return None

    @staticmethod
    def _fix_common_json_errors(response: str) -> str:
        """Fix common JSON formatting errors"""
        # Add missing closing braces
        if response.count("{") > response.count("}"):
            response = response + "}" * (response.count("{") - response.count("}"))

        # Fix missing commas between key-value pairs
        response = re.sub(r'"\s+"([^"]+)":', r'", "\1":', response)

        # Fix unquoted keys
        response = re.sub(r"(\w+):", r'"\1":', response)

        return response

    @staticmethod
    def _try_parse_structured(response: str) -> Optional[ToolPlan]:
        """Parse structured format like 'TOOL:calc EXPR="1+1"'"""
        # Match patterns like "TOOL:toolname PARAM=value"
        pattern = r'TOOL:(\w+)\s+(\w+)=(["\']?)([^"\']+)\3'
        match = re.search(pattern, response)

        if match:
            tool_name = match.group(1)
            param_name = match.group(2).lower()
            param_value = match.group(4)

            try:
                tool_type = ToolType(tool_name)
                args = {param_name: param_value}

                return ToolPlan(
                    tool=tool_type,
                    args=args,
                    confidence=0.7,  # Lower confidence for non-standard format
                )
            except ValueError:
                logger.warning(f"Invalid tool type in structured format: {tool_name}")

        return None
