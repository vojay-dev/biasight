from jinja2 import Environment, PackageLoader, select_autoescape
from pydantic_core import from_json
from vertexai.generative_models import ChatSession

from biasight.gemini import GeminiClient
from biasight.model import AnalyzeResult


class BiasAnalyzer:

    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client
        self.env = Environment(
            loader=PackageLoader('biasight'),
            autoescape=select_autoescape()
        )

    def _render_template(self, text: str) -> str:
        return self.env.get_template(f'analyze.jinja').render(text=text)

    def analyze(self, text: str) -> AnalyzeResult:
        prompt = self._render_template(text)
        chat: ChatSession = self.gemini_client.start_chat()
        chat_response: str = self.gemini_client.get_chat_response(chat, prompt)

        return AnalyzeResult.model_validate(from_json(chat_response))
