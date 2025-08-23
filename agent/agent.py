import logging

from .llm import LLMService
from .parser import ResponseParser
from .schemas import ToolPlan, ToolResult
from .tool_registry import ToolRegistry

logger = logging.getLogger(__name__)


class Agent:
    """Main agent class that orchestrates LLM calls and tool execution"""

    def __init__(self, use_fake_llm: bool = True):
        self.llm_service = LLMService(use_fake_llm=use_fake_llm)
        self.parser = ResponseParser()
        self.tool_registry = ToolRegistry()

    def answer(self, question: str) -> str:
        """Answer a question using LLM and tools"""
        try:
            llm_response = self.llm_service.call_llm(question)
            if llm_response is None:
                return "I'm sorry, I couldn't process your request."

            # Parse the response
            parsed_response = self.parser.parse_response(llm_response)

            if isinstance(parsed_response, ToolPlan):
                # Execute tool
                return self._execute_tool_plan(parsed_response)
            elif isinstance(parsed_response, str):
                return parsed_response
            else:
                return "I'm sorry, I couldn't understand the response format."

        except Exception as e:
            logger.error(f"Error processing question '{question}': {e}")
            return f"An error occurred while processing your request: {str(e)}"

    def _execute_tool_plan(self, plan: ToolPlan) -> str:
        """Execute a tool plan and return formatted result"""
        tool = self.tool_registry.get_tool(plan.tool.value)

        if tool is None:
            return f"Tool '{plan.tool.value}' is not available."

        result = tool.execute(plan.args)
        return self._format_tool_result(result)

    def _format_tool_result(self, result: ToolResult) -> str:
        """Format tool result for user display"""
        if not result.success:
            return f"Error: {result.error}"

        # Format based on tool type
        if result.tool_used == "weather":
            return f"{result.result}°C"
        elif result.tool_used == "calc":
            return str(result.result)
        elif result.tool_used == "kb":
            return str(result.result)
        elif result.tool_used == "translator":
            return str(result.result)
        else:
            return str(result.result)


# For backward compatibility
def answer(question: str) -> str:
    """Backward compatible function"""
    agent = Agent()
    return agent.answer(question)
