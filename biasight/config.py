from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    gcp_project_id: str
    gcp_location: str
    gcp_service_account_file: str
    gcp_gemini_model: str = 'gemini-1.5-pro-001'
