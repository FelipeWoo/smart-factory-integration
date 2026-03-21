import os
from dotenv import load_dotenv
from utils.logger import setup_loguru, logger
from pydantic import BaseModel
from pathlib import Path


class AppConfig(BaseModel):
    name: str
    env: str
    log_level: str
    root: str


def get_root() -> str:
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / "Makefile").is_file():
            return str(parent.resolve())
    raise FileNotFoundError("Makefile not found in any parent directory.")


def boot(log_name: str) -> AppConfig:
    load_dotenv(override=True)

    config = AppConfig(
        name=os.getenv("APP_NAME", "default"),
        env=os.getenv("APP_ENV", "production"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        root=get_root()
    )

    log_dir = Path(config.root) / "logs" / f"{log_name}.log"

    setup_loguru(level=config.log_level, log_file=log_dir)
    logger.info("System initialized.")
    logger.debug(f"AppConfig: {config.model_dump()}")

    return config



    