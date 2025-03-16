from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    gcp_project_id: str
    gcp_location: str
    gcp_service_account_file: str
    gcp_gemini_model: str = 'gemini-2.0-flash'
    parse_max_content_length: int = 1048576
    parse_chunk_size: int = 8192
    daily_limit: int = 20
    cache_size: int = 1000
    cache_ttl: int = 3600
    telegram_enabled: bool = False
    telegram_token: str = ''
    telegram_chat_id: int = 0
