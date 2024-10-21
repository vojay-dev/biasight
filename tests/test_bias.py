import unittest
from unittest.mock import Mock

from biasight.bias import BiasAnalyzer
from biasight.gemini import GeminiClient
from biasight.model import AnalyzeResult


class TestBiasAnalyzer(unittest.TestCase):

    def test_analyze(self):
        gemini_client: GeminiClient = Mock()
        bias_analyzer: BiasAnalyzer = BiasAnalyzer(gemini_client)

        # Ensure to NOT include overall_score in the Gemini mock data, as this is calculated by the BiasAnalyzer
        gemini_client.get_chat_response.return_value = """
            {
                "summary": "The webpage shows a strong commitment to gender equality through its focus on a hackathon addressing UN SDG 5.  However, while the language used is largely inclusive, the high number of mentions related to women and girls compared to men could be perceived as unbalanced.  Further improvements could enhance the overall inclusivity.",
                "stereotyping_feedback": "The webpage avoids reinforcing traditional gender stereotypes. The focus is on addressing gender inequality, not perpetuating it.",
                "stereotyping_score": 95,
                "stereotyping_example": "The hackathon's theme directly challenges gender inequality by focusing on UN SDG 5.",
                "representation_feedback": "While the hackathon aims for inclusivity, the overwhelming focus on women and girls in the description might inadvertently overshadow the participation of other genders.",
                "representation_score": 75,
                "representation_example": "The repeated emphasis on 'women and girls' in the description and prize categories.",
                "language_feedback": "The language used is largely gender-neutral and inclusive, using terms like 'participants' instead of gendered terms. However, the frequent mention of 'women and girls' could be balanced.",
                "language_score": 85,
                "language_example": "The use of 'participants' instead of gender-specific terms like 'participants' and the explicit statement that the hackathon is open to all genders.",
                "framing_feedback": "The framing of the hackathon positively promotes gender equality and empowerment.  There is no victim-blaming or minimization of women's experiences.",
                "framing_score": 90,
                "framing_example": "The hackathon's focus on UN SDG 5 and its emphasis on addressing real-world challenges faced by women and girls.",
                "positive_aspects": "The webpage's clear commitment to gender equality through its focus on a hackathon addressing UN SDG 5 is commendable. The use of inclusive language and the explicit statement welcoming participants of all genders are positive steps.",
                "improvement_suggestions": "1. Balance the focus on women and girls with more inclusive language that acknowledges the participation and contributions of all genders. 2.  Highlight success stories and contributions from participants of all genders in promotional materials. 3.  Ensure that judging criteria are equally applicable and unbiased towards all participants regardless of gender.",
                "male_to_female_mention_ratio": 0.1,
                "gender_neutral_language_percentage": 80
            }
        """

        analyze_result: AnalyzeResult = bias_analyzer.analyze('https://womentechmakers.devpost.com/')

        self.assertEqual(96, analyze_result.overall_score)

    def test_lowest_score(self):
        gemini_client: GeminiClient = Mock()
        bias_analyzer: BiasAnalyzer = BiasAnalyzer(gemini_client)

        # Ensure the lowest rating is 1
        gemini_client.get_chat_response.return_value = self._get_gemini_reply(
            0,
            0,
            0,
            0,
            0,
            0
        )

        analyze_result: AnalyzeResult = bias_analyzer.analyze('https://example.com/')
        self.assertEqual(1, analyze_result.overall_score)

    def test_highest_score(self):
        gemini_client: GeminiClient = Mock()
        bias_analyzer: BiasAnalyzer = BiasAnalyzer(gemini_client)

        # Ensure the highest rating is 100
        gemini_client.get_chat_response.return_value = self._get_gemini_reply(
            100,
            100,
            100,
            100,
            1,
            100
        )

        analyze_result: AnalyzeResult = bias_analyzer.analyze('https://example.com/')
        self.assertEqual(100, analyze_result.overall_score)

    def test_basic_score(self):
        gemini_client: GeminiClient = Mock()
        bias_analyzer: BiasAnalyzer = BiasAnalyzer(gemini_client)

        # Ensure that overall score is average if m-to-f ratio and neutral percentage are 0
        gemini_client.get_chat_response.return_value = self._get_gemini_reply(
            10,
            10,
            10,
            10,
            0,
            0
        )

        analyze_result: AnalyzeResult = bias_analyzer.analyze('https://example.com/')
        self.assertEqual(10, analyze_result.overall_score)

    def test_ratio_score_boost(self):
        gemini_client: GeminiClient = Mock()
        bias_analyzer: BiasAnalyzer = BiasAnalyzer(gemini_client)

        # Ensure that best m-to-f ratio increases score by 30%
        gemini_client.get_chat_response.return_value = self._get_gemini_reply(
            10,
            10,
            10,
            10,
            1,
            0
        )

        analyze_result: AnalyzeResult = bias_analyzer.analyze('https://example.com/')
        self.assertEqual(13, analyze_result.overall_score)

    def test_neutral_percentage_boost(self):
        gemini_client: GeminiClient = Mock()
        bias_analyzer: BiasAnalyzer = BiasAnalyzer(gemini_client)

        # Ensure that best neutral percentage increases score by 10%
        gemini_client.get_chat_response.return_value = self._get_gemini_reply(
            10,
            10,
            10,
            10,
            0,
            100
        )

        analyze_result: AnalyzeResult = bias_analyzer.analyze('https://example.com/')
        self.assertEqual(11, analyze_result.overall_score)

    @staticmethod
    def _get_gemini_reply(
            stereotyping_score: int,
            representation_score: int,
            language_score: int,
            framing_score: int,
            male_to_female_mention_ratio: float,
            gender_neutral_language_percentage: int
    ) -> str:
        return f"""
            {{
                "summary": "x",
                "stereotyping_feedback": "x",
                "stereotyping_score": {stereotyping_score},
                "stereotyping_example": "x",
                "representation_feedback": "x",
                "representation_score": {representation_score},
                "representation_example": "x",
                "language_feedback": "x",
                "language_score": {language_score},
                "language_example": "x",
                "framing_feedback": "x",
                "framing_score": {framing_score},
                "framing_example": "x",
                "positive_aspects": "x",
                "improvement_suggestions": "x",
                "male_to_female_mention_ratio": {male_to_female_mention_ratio},
                "gender_neutral_language_percentage": {gender_neutral_language_percentage}
            }}
        """
