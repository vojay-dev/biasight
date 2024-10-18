import logging
from functools import lru_cache

import colorlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials

from .bias import BiasAnalyzer
from .config import Settings
from .gemini import GeminiClient
from .model import AnalyzeRequest, AnalyzeResponse
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
bias_analyzer: BiasAnalyzer = BiasAnalyzer(gemini_client)
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

@app.post('/analyze')
async def analyze(analyze_request: AnalyzeRequest) -> AnalyzeResponse:
    text = web_parser.parse(analyze_request.uri)
    result = bias_analyzer.analyze(text)

    response = AnalyzeResponse(uri=analyze_request.uri, result=result)
    return response
