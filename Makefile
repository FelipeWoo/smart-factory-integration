# Makefile for Python project

PYTHON := uv
ENV_FILE := .env
TEST_ENV_FILE := .env.test
SRC_DIR := src
TEST_DIR := tests
NOTEBOOK_DIR := scripts/notebooks

# Load environment variables (optional fallback if .env exists)
ifneq ("$(wildcard $(ENV_FILE))","")
	include $(ENV_FILE)
	export
endif

.PHONY: help init run test cov lint ty check clean reset

help:
	@echo "Available commands:"
	@echo "  make init         - Create virtual environment and install dependencies"
	@echo "  make run          - Run the main program"
	@echo "  make test         - Run tests"
	@echo "  make cov          - Run tests with coverage"
	@echo "  make lint         - Run code formatters and linters"
	@echo "  make ty           - Run ty (static type checker)"
	@echo "  make check        - Run lint + ty checks"
	@echo "  make clean        - Remove compiled and temporary files"
	@echo "  make reset        - Remove env, logs, __pycache__, etc."


init:
	$(PYTHON) init
	$(PYTHON) venv
	$(PYTHON) add -r requirements.txt

run:
	@cd $(SRC_DIR) && $(PYTHON) run main.py

test:
	APP_ENV=test $(PYTHON) pip install -e .
	APP_ENV=test $(PYTHON) run -m pytest $(TEST_DIR)

cov:
	APP_ENV=test $(PYTHON) run -m pytest --cov=$(SRC_DIR) --cov-report=term-missing

lint:
	$(PYTHON) run ruff check $(SRC_DIR) $(TEST_DIR)
	$(PYTHON) run black --check $(SRC_DIR) $(TEST_DIR)

ty:
	$(PYTHON) run ty check $(SRC_DIR)

check: lint ty

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .pytest_cache .coverage coverage.xml

reset: clean
	rm -rf .venv logs
