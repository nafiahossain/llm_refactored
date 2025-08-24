from agent.llm import LLMService
from agent.schemas import ToolPlan, ToolType


class TestLLMService:
    def setup_method(self):
        self.llm = LLMService(use_fake_llm=True)

    def test_generate_tool_plan_german(self):
        """Ensure German translation branch is hit"""
        plan = self.llm._generate_tool_plan(
            "translate to german", "Translate hello to German"
        )
        assert plan.tool == ToolType.TRANSLATOR
        assert plan.args["target_language"] == "german"

    def test_generate_tool_plan_dhaka(self):
        """Ensure Dhaka weather branch is hit"""
        plan = self.llm._generate_tool_plan(
            "temperature in dhaka", "What is the temperature in Dhaka?"
        )
        assert plan.tool == ToolType.WEATHER
        assert plan.args["city"] == "dhaka"

    def test_generate_tool_plan_default_weather(self):
        """Ensure default fallback goes to Paris weather"""
        plan = self.llm._generate_tool_plan("some random input", "Blah blah blah")
        assert plan.tool == ToolType.WEATHER
        assert plan.args["city"] == "paris"

    def test_call_llm_returns_tool_plan(self, monkeypatch):
        # Force random roll to return a tool plan
        monkeypatch.setattr("random.random", lambda: 0.1)
        result = self.llm.call_llm("What is the weather in London?")
        assert isinstance(result, ToolPlan)
        assert result.tool in [
            ToolType.WEATHER,
            ToolType.CALC,
            ToolType.TRANSLATOR,
            ToolType.KB,
        ]

    def test_call_llm_returns_malformed_json(self, monkeypatch):
        monkeypatch.setattr("random.random", lambda: 0.4)
        result = self.llm.call_llm("What is 2+2?")
        assert isinstance(result, str)
        assert "tool" in result

    def test_call_llm_returns_structured_format(self, monkeypatch):
        monkeypatch.setattr("random.random", lambda: 0.7)
        result = self.llm.call_llm("Add 12.5% of 243")
        assert isinstance(result, str)
        assert result.startswith("TOOL:calc")

    def test_call_llm_returns_direct_answer(self, monkeypatch):
        monkeypatch.setattr("random.random", lambda: 0.85)
        result = self.llm.call_llm("Who is Ada Lovelace?")
        assert isinstance(result, str)
        assert "Ada Lovelace" in result or result.startswith(
            "I think you are asking about:"
        )

    def test_generate_tool_plan_handles_exception(self, monkeypatch, caplog):
        # Simulate an exception in _generate_tool_plan
        def bad_generate_tool_plan(p, prompt):
            raise RuntimeError("Simulated error")

        self.llm._generate_tool_plan = bad_generate_tool_plan
        monkeypatch.setattr(
            "random.random", lambda: 0.1
        )  # Always triggers tool plan path

        with caplog.at_level("WARNING"):
            result = self.llm.call_llm("weather")
            assert result is None
            assert "Error generating tool plan" in caplog.text
