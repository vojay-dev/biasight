import logging
from functools import lru_cache

import colorlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from vertexai.generative_models import ChatSession

from .config import Settings
from .gemini import GeminiClient
from .parse import WebParser

# setup logging
log_format = '%(log_color)s%(asctime)s [%(levelname)s] %(reset)s%(purple)s[%(name)s] %(reset)s%(blue)s%(message)s'
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(log_format))
logging.basicConfig(level=logging.INFO, handlers=[handler])

logger: logging.Logger = logging.getLogger(__name__)

@lru_cache
def _get_settings() -> Settings:
    return Settings()

settings: Settings = _get_settings()

credentials: Credentials = service_account.Credentials.from_service_account_file(settings.gcp_service_account_file)

gemini_client: GeminiClient = GeminiClient(
    settings.gcp_project_id,
    settings.gcp_location,
    credentials,
    settings.gcp_gemini_model
)
web_parser: WebParser = WebParser(settings.parse_max_content_length, settings.parse_chunk_size)

app: FastAPI = FastAPI()

# for local development
origins = [
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:5173',
]

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
async def get_asdf():
    uri = 'https://www.tagesschau.de/ausland/amerika/scholz-biden-treffen-berlin-100.html'
    text = web_parser.parse(uri)
    prompt = f"""
    You are a world-class expert on identifying and explaining gender bias in written content. Analyze the following text for gender bias, considering the following categories:

    1. **Stereotyping:**  Identify and analyze instances where gender stereotypes are reinforced or challenged. For example, are traditional gender roles being perpetuated? Are specific traits or behaviors attributed to one gender over another? 
    2. **Representation:** Assess the representation of genders in the text. Are men and women equally represented? Are diverse perspectives and experiences included?  
    3. **Language:** Analyze the language used for potentially biased or discriminatory wording.  Consider:
        - **Gendered Language:** (e.g., "policeman" vs. "police officer," "mankind" vs. "humanity")
        - **Loaded Language:** Words with strong connotations that could reinforce stereotypes (e.g., "bossy" vs. "assertive," "emotional" vs. "passionate"). 
    4. **Framing:** Evaluate how the text frames gender-related issues or events. Does the framing reinforce existing power structures or biases? Are there any instances of victim-blaming or minimizing the experiences of women?

    For each category:
    - Provide a concise summary of your analysis.
    - Give a score from 1 to 5, where 1 is highly biased and 5 is free of bias.

    Finally, compute an overall "Gender Bias Score" from 1 to 5 based on the category scores.

    Return your analysis in JSON format: 

    {{"stereotyping_feedback": str, "stereotyping_score": int, "representation_feedback": str, "representation_score": int, "language_feedback": str, "language_score": int, "framing_feedback": str, "framing_score": int, "overall_score": int}}

    Text to analyze:

    {text}
    """
    logger.info(prompt)
    chat: ChatSession = gemini_client.start_chat()
    return gemini_client.get_chat_response(chat, prompt)
