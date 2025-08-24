import logging
import random
from typing import Optional, Union

from .schemas import ToolPlan, ToolType

logger = logging.getLogger(__name__)


class LLMService:
    """Service for handling LLM interactions"""

    def __init__(self, use_fake_llm: bool = True):
        self.use_fake_llm = use_fake_llm

    def call_llm(self, prompt: str) -> Optional[Union[str, ToolPlan]]:
        """Call LLM and return either a direct response or a tool plan"""
        if self.use_fake_llm:
            return self._fake_llm_call(prompt)

    def _fake_llm_call(self, prompt: str) -> Optional[Union[str, ToolPlan]]:
        """Fake LLM that simulates real-world behavior including errors"""
        p = prompt.lower()
        roll = random.random()

        # 35% chance of returning a proper tool plan
        if roll < 0.35:
            try:
                return self._generate_tool_plan(p, prompt)
            except Exception as e:  # pragma: no cover
                logger.warning(f"Error generating tool plan: {e}")
                return None

        # 25% chance of malformed JSON (simulate real LLM flakiness)
        if roll < 0.60:
            try:
                return self._generate_malformed_response()
            except Exception as e:  # pragma: no cover
                logger.warning(f"Error generating malformed response: {e}")
                return None

        # 20% chance of completely wrong format
        if roll < 0.80:
            try:
                return 'TOOL:calc EXPR="12.5% of 243"'
            except Exception as e:  # pragma: no cover
                logger.warning(f"Error generating structured response: {e}")
                return None

        # 20% chance of direct answer
        try:
            return self._generate_direct_answer(p, prompt)
        except Exception as e:  # pragma: no cover
            logger.warning(f"Error generating direct answer: {e}")
        return None

    def _generate_tool_plan(self, p: str, prompt: str) -> Optional[ToolPlan]:
        """Generate a proper tool plan"""
        try:
            if "translate" in p or "spanish" in p or "french" in p or "german" in p:
                # Extract text and language
                text = "hello"
                lang = "spanish"
                if "french" in p:
                    lang = "french"
                elif "german" in p:
                    lang = "german"

                return ToolPlan(
                    tool=ToolType.TRANSLATOR,
                    args={"text": text, "target_language": lang},
                )

            if "weather" in p or "temperature" in p:
                city = "paris"
                if "london" in p:
                    city = "london"
                elif "dhaka" in p:
                    city = "dhaka"

                return ToolPlan(tool=ToolType.WEATHER, args={"city": city})

            if "%" in p or "add" in p or any(op in p for op in ["+", "-", "*", "/"]):
                return ToolPlan(tool=ToolType.CALC, args={"expr": prompt})

            if "ada lovelace" in p or "who is" in p or "knowledge" in p:
                if "who is" in p:
                    name = prompt.lower().split("who is", 1)[1].strip().rstrip("?")
                    query = name
                else:
                    query = prompt
                return ToolPlan(tool=ToolType.KB, args={"q": query})

            # Default fallback
            return ToolPlan(tool=ToolType.WEATHER, args={"city": "paris"})
        except Exception as e:
            logger.warning(f"Error generating tool plan: {e}")
            return None

    def _generate_malformed_response(self) -> str:
        """Generate malformed JSON to simulate real LLM errors"""
        malformed_responses = [
            '{"tool": "weather", "args": {"city": "Pa ris" }',  # Missing closing brace
            '{"tool": "calc", "args": {"expr": "1+1"}',  # Missing closing brace
            '{"tool": "weather" "args": {"city": "london"}}',  # Missing comma
            'tool: "calc", args: {expr: "2+2"}',  # Invalid JSON format
        ]
        return random.choice(malformed_responses)

    def _generate_direct_answer(self, p: str, prompt: str) -> str:
        """Generate direct answers for some queries"""
        if "ada lovelace" in p:
            return "Ada Lovelace was a 19th-century mathematician and early computing pioneer."
        return f"I think you are asking about: {prompt[:60]}"
