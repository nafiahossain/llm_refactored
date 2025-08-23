from agent.agent import Agent, answer
from agent.schemas import ToolPlan, ToolResult, ToolType
from agent.tool_registry import ToolRegistry


class TestAgent:
    def setup_method(self):
        self.agent = Agent(use_fake_llm=True)

    def test_calculator_query(self):
        """Test multiple times due to randomness in fake LLM"""
        results = []
        for _ in range(10):
            result = self.agent.answer("What is 2 + 3?")
            results.append(result)

        assert any("5" in str(result) for result in results)

    def test_weather_query(self):
        results = []
        for _ in range(10):
            result = self.agent.answer("What is the temperature in Paris?")
            results.append(result)
        assert any("°C" in str(result) or "18" in str(result) for result in results)

    def test_knowledge_base_query(self):
        results = []
        for _ in range(10):
            result = self.agent.answer("Who is Ada Lovelace?")
            results.append(result)

        assert any(
            "mathematician" in str(result).lower() or "computing" in str(result).lower()
            for result in results
        )

    def test_translation_query(self):
        results = []
        for _ in range(10):
            result = self.agent.answer("Translate hello to Spanish")
            results.append(result)

        assert any(len(str(result)) > 0 for result in results)

    def test_error_handling(self):
        """Test that agent doesn't crash on malformed input"""
        result = self.agent.answer("")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_backward_compatibility(self):
        """Test the backward compatible function"""
        result = answer("What is 1 + 1?")
        assert isinstance(result, str)

    def test_unrecognized_response_format(self, monkeypatch):
        """Test the else branch when response format is unrecognized"""
        monkeypatch.setattr(
            self.agent.llm_service, "call_llm", lambda q: {"weird": "data"}
        )
        result = self.agent.answer("Trigger unknown format")
        assert result == "I'm sorry, I couldn't understand the response format."

    def test_exception_handling(self, monkeypatch):
        """Test that exceptions are caught and handled"""

        def raise_exception(_):
            raise ValueError("Fake error")

        monkeypatch.setattr(self.agent.llm_service, "call_llm", raise_exception)
        result = self.agent.answer("Cause exception")
        assert "An error occurred while processing your request" in result

    def test_tool_not_available(self, monkeypatch):
        """Test case where requested tool is not registered"""

        # Use a valid enum value
        fake_plan = ToolPlan(tool=ToolType.CALC, args={})

        # Patch ToolRegistry.get_tool to return None
        monkeypatch.setattr(
            self.agent.tool_registry, "get_tool", lambda tool_name: None
        )

        result = self.agent._execute_tool_plan(fake_plan)
        assert "Tool 'calc' is not available." in result

    def test_kb_tool_result(self):
        """Test formatting when tool_used is 'kb'"""
        result = self.agent._format_tool_result(
            ToolResult(success=True, tool_used="kb", result="Knowledge Base Entry")
        )
        assert result == "Knowledge Base Entry"

    def test_default_tool_result(self):
        """Test formatting for an unrecognized tool type"""
        result = self.agent._format_tool_result(
            ToolResult(success=True, tool_used="other_tool", result="Some output")
        )
        assert result == "Some output"
