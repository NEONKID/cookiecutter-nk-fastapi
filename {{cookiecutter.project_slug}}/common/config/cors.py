from pydantic import BaseSettings, Field
from typing import List


class CORSSettings(BaseSettings):
    origin: List[str] = Field(default=["*"])
    methods: List[str] = Field(default=["*"])
    headers: List[str] = Field(default=["*"])
