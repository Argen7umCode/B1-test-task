import os

from utils.process import Grouper, Parser


class Config:
    DB_CONFIG = os.getenv(
        "DB_CONFIG",
        "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
            DB_USER=os.getenv("DB_USER", "postgres"),
            DB_PASSWORD=os.getenv("DB_PASSWORD", "postgres"),
            DB_HOST=os.getenv("DB_HOST", "127.0.0.1:5432"),
            DB_NAME=os.getenv("DB_NAME", "postgres"),
        ),
    )


config = Config
parser = Parser()
