from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

SYSTEM_PROMPT_TEMPLATE = "You are NOVA, a helpful AI assistant."


class OpenAISettings(BaseModel):
    api_key: SecretStr


class MongoDBSettings(BaseModel):
    uri: SecretStr
    database_name: str


class PromptSettings(BaseModel):
    system_prompt_template: str = SYSTEM_PROMPT_TEMPLATE


class NOVASettings(BaseSettings):
    openai: OpenAISettings
    prompt: PromptSettings = {}
    db: MongoDBSettings
    token: SecretStr

    init_path: str | None = None

    model_config = SettingsConfigDict(
        env_file=[
            ".env",
            ".env.local",
        ],
        env_nested_delimiter="__",
        extra="ignore",
    )


SHARED_SETTINGS = NOVASettings()
