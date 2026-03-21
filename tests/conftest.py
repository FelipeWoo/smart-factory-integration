import os
import pytest
from src.utils.boot import boot
from src.utils.logger import logger


def test_boot_config():
    os.environ["APP_NAME"] = "test_app"
    os.environ["APP_ENV"] = "testing"
    os.environ["LOG_LEVEL"] = "DEBUG"

    config = boot("test_config")

    assert config.name == "test_app"
    assert config.env == "testing"
    assert config.log_level.upper() == "DEBUG"
    assert config.root is not None
    assert "Makefile" in os.listdir(config.root)


def test_logger_outputs(caplog):
    os.environ["APP_NAME"] = "log_test"
    os.environ["LOG_LEVEL"] = "DEBUG"

    config = boot("log_test")
    with caplog.at_level("DEBUG"):
        logger.debug("Testing debug output")
        logger.info("Testing info output")

    assert "Testing debug output" in caplog.text
    assert "Testing info output" in caplog.text

