import logging
from functools import lru_cache

import colorlog
from cachetools import TTLCache
from fastapi import FastAPI
from fastapi import HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials

from .bias import BiasAnalyzer
from .config import Settings
from .gemini import GeminiClient
from .limit import RateLimiter
from .model import AnalyzeRequest, AnalyzeResponse, LimitResponse
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
rate_limiter: RateLimiter = RateLimiter(settings.daily_limit)

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

# cache for results to avoid analyzing the same URI again in a short amount of time
# ttl = seconds after which results will be invalidated
result_cache: TTLCache = TTLCache(maxsize=1000, ttl=3600)

@app.post('/analyze')
def analyze(analyze_request: AnalyzeRequest) -> AnalyzeResponse:
    # try to use cached result
    cached_result = result_cache.get(analyze_request.uri)

    if cached_result:
        logger.info('returning cached result for %s', analyze_request.uri)
        return AnalyzeResponse(uri=analyze_request.uri, result=cached_result)

    # if not cached, check rate limit before invoking the analyzer
    rate_limiter.increment()

    logger.info('analyzing %s', analyze_request.uri)
    text = web_parser.parse(analyze_request.uri)

    if not text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Could not parse page')

    try:
        result = bias_analyzer.analyze(text)
        result_cache[analyze_request.uri] = result

        response = AnalyzeResponse(uri=analyze_request.uri, result=result)
        return response
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Could not analyze page')

@app.get('/limit')
async def limit() -> LimitResponse:
    rate_limiter.check_and_update()
    return LimitResponse(limit=rate_limiter.limit, usage=rate_limiter.usage, last_reset=rate_limiter.last_reset_iso)
