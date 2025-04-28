import os
from loguru import logger

def setup_logging():
    logger.add("server.log", rotation="2 MB", retention="10 days", level="DEBUG")

def get_env_var(key, default=None):
    return os.getenv(key, default)
