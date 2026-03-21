import logging
from loguru import logger
import sys
from pathlib import Path

# Custom format for console and file output
LOG_FORMAT = (
    "<level>▶ {level: <8}</level> | "
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<cyan>{name}:{function}:{line}</cyan> - "
    "<level>{message}</level>"
)

def setup_loguru(level: str = "DEBUG", log_file: str = "logs/main.log") -> None:
    """
    Configures loguru with:
    - Console output
    - Rotating file output
    - Interception of standard logs (uvicorn, sqlalchemy, etc.)
    """
    # Ensure log directory exists
    log_path = Path(log_file).resolve()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Remove previous handlers
    logger.remove()

    # Console output
    logger.add(sys.stdout, level=level, colorize=True, format=LOG_FORMAT)

    # Rotating file output
    logger.add(str(log_path), rotation="1 week", retention="1 month", level=level, format=LOG_FORMAT)

    # Redirect standard logs to loguru
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                log_level = logger.level(record.levelname).name
            except ValueError:
                log_level = record.levelno

            logger.opt(depth=6, exception=record.exc_info).log(log_level, record.getMessage())

    intercept_handler = InterceptHandler()
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi", "sqlalchemy"):
        logging.getLogger(name).handlers = [intercept_handler]
        logging.getLogger(name).setLevel(logging.DEBUG)

# Make globally importable
__all__ = ["logger", "setup_loguru"]
