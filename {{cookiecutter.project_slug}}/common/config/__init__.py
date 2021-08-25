from enum import Enum
from pydantic import BaseSettings, Field

from shared.config.cors import CORSSettings


class ApplicationEnvironment(str, Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"
    TEST = "test"


class ApplicationSettings(BaseSettings):
    env: ApplicationEnvironment = Field(default=ApplicationEnvironment.LOCAL, env="APP_ENV")
    cors: CORSSettings = CORSSettings()
