"""MongoDB connection manager."""

from pymongo import MongoClient
from pymongo.database import Database
from loguru import logger

from src.config.settings import settings

_client: MongoClient | None = None
_db: Database | None = None


def get_db() -> Database:
    """Return the MongoDB database instance, connecting lazily."""
    global _client, _db
    if _db is not None:
        return _db

    _client = MongoClient(settings.mongo_uri)
    _db = _client.get_default_database()
    logger.info(f"[mongo] connected to {settings.mongo_uri}")
    return _db


def close_db() -> None:
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        logger.info("[mongo] connection closed")
