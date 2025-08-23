from agent.tools.calculator import CalculatorTool
from agent.tools.knowledge_base import KnowledgeBaseTool
from agent.tools.translator import TranslatorTool
from agent.tools.weather import WeatherTool


class TestCalculatorTool:
    def setup_method(self):
        self.tool = CalculatorTool()

    def test_basic_arithmetic(self):
        result = self.tool.execute({"expr": "2 + 3"})
        assert result.success
        assert result.result == 5.0

    def test_percentage_calculation(self):
        result = self.tool.execute({"expr": "12.5% of 243"})
        assert result.success
        assert abs(result.result - 30.375) < 0.001

    def test_invalid_expression(self):
        result = self.tool.execute({"expr": "invalid_expr"})
        assert not result.success
        assert "error" in result.error.lower()

    def test_missing_args(self):
        result = self.tool.execute({})
        assert not result.success
        assert "invalid arguments" in result.error.lower()

    def test_unsafe_expression(self):
        result = self.tool.execute({"expr": "__import__('os').system('ls')"})
        assert not result.success


class TestWeatherTool:
    def setup_method(self):
        self.tool = WeatherTool()

    def test_known_city(self):
        result = self.tool.execute({"city": "Paris"})
        assert result.success
        assert result.result == 18.0

    def test_case_insensitive(self):
        result = self.tool.execute({"city": "LONDON"})
        assert result.success
        assert result.result == 17.0

    def test_unknown_city(self):
        result = self.tool.execute({"city": "UnknownCity"})
        assert result.success
        assert result.result == 20.0

    def test_missing_args(self):
        result = self.tool.execute({})
        assert not result.success


class TestKnowledgeBaseTool:
    def setup_method(self):
        self.tool = KnowledgeBaseTool()

    def test_known_entry(self):
        result = self.tool.execute({"q": "Ada Lovelace"})
        assert result.success
        if "No entry found" not in result.result:
            assert "mathematician" in result.result.lower()

    def test_case_insensitive_search(self):
        result = self.tool.execute({"q": "ada lovelace"})
        assert result.success

    def test_unknown_entry(self):
        result = self.tool.execute({"q": "Unknown Person"})
        assert result.success

    def test_missing_args(self):
        result = self.tool.execute({})
        assert not result.success


class TestTranslatorTool:
    def setup_method(self):
        self.tool = TranslatorTool()

    def test_basic_translation(self):
        result = self.tool.execute({"text": "hello", "target_language": "spanish"})
        assert result.success
        assert result.result == "hola"

    def test_case_insensitive(self):
        result = self.tool.execute({"text": "HELLO", "target_language": "FRENCH"})
        assert result.success
        assert result.result == "bonjour"

    def test_unknown_translation(self):
        result = self.tool.execute(
            {"text": "unknown_word", "target_language": "spanish"}
        )
        assert result.success
        assert "translation not available" in result.result.lower()

    def test_missing_args(self):
        result = self.tool.execute({"text": "hello"})
        assert not result.success

    def test_invalid_args(self):
        result = self.tool.execute({"text": 123, "target_language": "spanish"})
        assert not result.success
