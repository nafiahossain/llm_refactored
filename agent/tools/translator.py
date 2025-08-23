from typing import Any, Dict

from ..schemas import ToolResult
from .base import BaseTool


class TranslatorTool(BaseTool):
    """Mock implementation of translation tool"""

    # Mock translation data
    _TRANSLATIONS = {
        ("hello", "spanish"): "hola",
        ("hello", "french"): "bonjour",
        ("hello", "german"): "hallo",
        ("goodbye", "spanish"): "adiós",
        ("goodbye", "french"): "au revoir",
        ("goodbye", "german"): "auf wiedersehen",
        ("thank you", "spanish"): "gracias",
        ("thank you", "french"): "merci",
        ("thank you", "german"): "danke",
        ("yes", "spanish"): "sí",
        ("yes", "french"): "oui",
        ("yes", "german"): "ja",
        ("no", "spanish"): "no",
        ("no", "french"): "non",
        ("no", "german"): "nein",
    }

    @property
    def name(self) -> str:
        return "translator"

    def validate_args(self, args: Dict[str, Any]) -> bool:
        return (
            "text" in args
            and isinstance(args["text"], str)
            and "target_language" in args
            and isinstance(args["target_language"], str)
        )

    def execute(self, args: Dict[str, Any]) -> ToolResult:
        if not self.validate_args(args):
            return ToolResult(
                success=False,
                result="",
                error="Invalid arguments. Expected 'text' and 'target_language' fields.",
                tool_used=self.name,
            )

        try:
            text = args["text"].lower().strip()
            target_lang = args["target_language"].lower().strip()

            translation = self._translate(text, target_lang)
            return ToolResult(success=True, result=translation, tool_used=self.name)
        except Exception as e:
            return ToolResult(
                success=False,
                result="",
                error=f"Translation error: {str(e)}",
                tool_used=self.name,
            )

    def _translate(self, text: str, target_language: str) -> str:
        """Translate text to target language"""
        key = (text, target_language)
        if key in self._TRANSLATIONS:
            return self._TRANSLATIONS[key]
        else:
            return f"Translation not available for '{text}' to {target_language}"
