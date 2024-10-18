from typing import Optional

from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    uri: str

class AnalyzeResult(BaseModel):
    stereotyping_feedback: str
    stereotyping_score: int
    representation_feedback: str
    representation_score: int
    language_feedback: str
    language_score: int
    framing_feedback: str
    framing_score: int
    overall_score: int

class AnalyzeResponse(BaseModel):
    uri: str
    result: AnalyzeResult
