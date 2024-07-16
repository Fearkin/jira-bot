from typing import Optional
from pydantic import EmailStr, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import tomllib


class Settings(BaseSettings):
    """Stores secrets and other configuration details"""

    issue_key: str
    jira_url: str
    jira_token: SecretStr
    jira_id: SecretStr
    jira_email: EmailStr
    bot_token: SecretStr
    redis: RedisDsn
    admin_chat_id: int
    projects: Optional[list[str]] = None
    problem_types: Optional[list[str]] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def read_extra_settings(self, path: str):
        with open(path, "rb") as f:
            data = tomllib.load(f)
            self.projects = data["projects"]
            self.problem_types = data["problem_types"]
        return self


config = Settings().read_extra_settings("settings.toml")
