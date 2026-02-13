from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379"
    mongo_uri: str = "mongodb://localhost:27017/price_comparison"
    log_level: str = "INFO"
    queue_name: str = "scrape:jobs"
    queue_poll_interval: int = 1  # seconds between BRPOP calls

    class Config:
        env_prefix = "SCRAPER_"
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
