from typing import Optional

from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    uri: str

class AnalyzeResult(BaseModel):
    summary: str
    overall_score: int
    stereotyping_feedback: str
    stereotyping_score: int
    stereotyping_example: str
    representation_feedback: str
    representation_score: int
    representation_example: str
    language_feedback: str
    language_score: int
    language_example: str
    framing_feedback: str
    framing_score: int
    framing_example: str
    positive_aspects: str
    improvement_suggestions: str
    male_to_female_mention_ratio: float
    gender_neutral_language_percentage: float

class AnalyzeResponse(BaseModel):
    uri: str
    result: AnalyzeResult
