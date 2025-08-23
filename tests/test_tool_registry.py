from agent.tool_registry import ToolRegistry
from agent.tools.calculator import CalculatorTool


class TestToolRegistry:
    def setup_method(self):
        self.registry = ToolRegistry()

    def test_default_tools_registered(self):
        tools = self.registry.list_tools()
        assert "calc" in tools
        assert "weather" in tools
        assert "kb" in tools
        assert "translator" in tools

    def test_get_existing_tool(self):
        tool = self.registry.get_tool("calc")
        assert tool is not None
        assert isinstance(tool, CalculatorTool)

    def test_get_nonexistent_tool(self):
        tool = self.registry.get_tool("nonexistent")
        assert tool is None

    def test_register_new_tool(self):
        # Create a mock tool
        class MockTool:
            @property
            def name(self):
                return "mock"

        mock_tool = MockTool()
        self.registry.register_tool(mock_tool)

        retrieved_tool = self.registry.get_tool("mock")
        assert retrieved_tool is mock_tool
