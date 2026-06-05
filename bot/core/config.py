import os

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "flyrum")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "flyrum")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "flyrum")

settings = Settings()
