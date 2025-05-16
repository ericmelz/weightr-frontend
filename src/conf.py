from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    login_url: str
    weight_url: str
