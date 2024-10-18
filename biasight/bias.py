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
        return self.env.get_template('analyze.jinja').render(text=text)

    @staticmethod
    def _calculate_score(analyze_result: AnalyzeResult) -> int:
        stereotyping_score = analyze_result.stereotyping_score
        representation_score = analyze_result.representation_score
        language_score = analyze_result.language_score
        framing_score = analyze_result.framing_score

        base_score = (stereotyping_score + representation_score + language_score + framing_score) / 4

        male_to_female_mention_ratio = analyze_result.male_to_female_mention_ratio
        gender_neutral_language_percentage = analyze_result.gender_neutral_language_percentage

        # calculate ratio boost
        ratio_boost = 0
        if male_to_female_mention_ratio > 0:  # Avoid division by zero
            ratio_difference = abs(1 - male_to_female_mention_ratio)
            ratio_boost = max(0, 30 * (1 - ratio_difference))  # Max boost of 30% when ratio is 1

        # calculate neutral language boost
        neutral_language_boost = (gender_neutral_language_percentage / 100) * 10  # Max boost of 10% when 100% neutral

        # apply boosts
        boosted_score = base_score * (1 + ratio_boost / 100 + neutral_language_boost / 100)

        # ensure the final score is between 1 and 100
        final_score = int(round(max(1, min(100, boosted_score))))
        return final_score

    def analyze(self, text: str) -> AnalyzeResult:
        prompt = self._render_template(text)
        chat: ChatSession = self.gemini_client.start_chat()
        chat_response: str = self.gemini_client.get_chat_response(chat, prompt)

        analyze_result = AnalyzeResult.model_validate(from_json(chat_response))

        # overall score is calculated via Python instead of using the LLM to ensure deterministic results
        analyze_result.overall_score = self._calculate_score(analyze_result)

        return analyze_result
