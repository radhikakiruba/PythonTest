import os
from dataclasses import dataclass

@dataclass
class AppConfig:
    base_url: str
    api_url: str
    db_string: str
    auth_token: str

    @classmethod
    def load(cls):
        return cls(
            base_url=os.getenv("BASE_URL"),
            api_url=os.getenv("API_URL"),
            db_string=os.getenv("DB_CONNECTION"),
            auth_token=os.getenv("AUTH_TOKEN")
        )