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

    def test_parse_response_invalid_type(self):
        result = ResponseParser.parse_response(12345)
        assert result is None

    def test_parse_dict_response_invalid_tool(self, caplog):
        response = {"tool": "invalid_tool", "args": {"x": 1}}
        with caplog.at_level("WARNING"):
            result = ResponseParser.parse_response(response)
        assert result is None
        assert "Invalid tool type" in caplog.text

    def test_parse_dict_response_exception(self, caplog):
        response = {"tool": "calc", "args": None}
        with caplog.at_level("WARNING"):
            result = ResponseParser.parse_response(response)
        assert result is None
        assert "Error parsing dict response" in caplog.text

    def test_parse_structured_invalid_tool(self, caplog):
        response = "TOOL:invalidtool PARAM=123"
        with caplog.at_level("WARNING"):
            result = ResponseParser._try_parse_structured(response)
            assert result is None
            assert any(
                "Invalid tool type in structured format: invalidtool" in m
                for m in caplog.messages
            )
