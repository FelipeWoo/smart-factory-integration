import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

from app.utils.logger import logger, setup_loguru


class AppConfig(BaseModel):
    name: str
    env: str
    log_level: str
    root: str


def get_root() -> str:
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / ".git").is_dir():
            return str(parent.resolve())
    raise FileNotFoundError(
        ".git directory not found in any parent directory.")


def load_config() -> AppConfig:
    load_dotenv(override=True)
    return AppConfig(
        name=os.getenv("APP_NAME", "default"),
        env=os.getenv("APP_ENV", "production"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        root=get_root(),
    )


def init_logger(log_name: str, config: AppConfig) -> None:
    log_path = Path(config.root) / "logs" / f"{log_name}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    setup_loguru(level=config.log_level, log_file=log_path)


def boot(log_name: str) -> AppConfig:
    config = load_config()
    init_logger(log_name, config=config)
    logger.info("System initialized.")
    logger.debug(f"AppConfig: {config.model_dump()}")

    return config
