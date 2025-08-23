from agent.parser import ResponseParser
from agent.schemas import ToolPlan, ToolType


class TestResponseParser:
    def test_parse_valid_dict(self):
        response = {"tool": "calc", "args": {"expr": "1+1"}}
        result = ResponseParser.parse_response(response)
        assert isinstance(result, ToolPlan)
        assert result.tool == ToolType.CALC

    def test_parse_valid_json_string(self):
        response = '{"tool": "weather", "args": {"city": "paris"}}'
        result = ResponseParser.parse_response(response)
        assert isinstance(result, ToolPlan)
        assert result.tool == ToolType.WEATHER

    def test_parse_malformed_json(self):
        response = '{"tool": "weather", "args": {"city": "paris"}'
        result = ResponseParser.parse_response(response)
        assert isinstance(result, ToolPlan)
        assert result.tool == ToolType.WEATHER

    def test_parse_structured_format(self):
        response = 'TOOL:calc EXPR="1+1"'
        result = ResponseParser.parse_response(response)
        assert isinstance(result, ToolPlan)
        assert result.tool == ToolType.CALC

    def test_parse_direct_answer(self):
        response = "This is a direct answer"
        result = ResponseParser.parse_response(response)
        assert isinstance(result, str)
        assert result == "This is a direct answer"

    def test_parse_typo_correction(self):
        response = {
            "tool": "weaher",  # Intentional typo
            "args": {"city": "paris"},
        }
        result = ResponseParser.parse_response(response)
        assert isinstance(result, ToolPlan)
        assert result.tool == ToolType.WEATHER
