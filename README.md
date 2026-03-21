# Template Python Project

## Overview

This is a general-purpose Python project template designed for rapid development and clean structure.  
It uses `uv` for dependency management and includes support for logging, environment configuration, testing, linting, static type checking, and Jupyter notebooks.

## Features

- Structured source code in `src/`
- Logging system with loguru
- Environment configuration with dotenv
- Test suite with pytest
- Code formatting with black and ruff
- Static type analysis with ty
- Jupyter notebook support for exploration
- Makefile with common automation tasks

## Requirements

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (package manager)
- Unix-like system or WSL (recommended)

## Installation

Clone the repository and run:

```bash
make init
````

This will create the virtual environment and install all required dependencies.

## Running the Project

```bash
make run
```

## Environment Configuration

Create a `.env` file based on the provided `.env.example` and customize values as needed.

```dotenv
APP_NAME=template_python
APP_ENV=development
LOG_LEVEL=DEBUG
```

## Testing

```bash
make test
make cov
```

## Linting and Formatting

```bash
make lint
make ty
make check
```

## Jupyter Notebooks

To launch a Jupyter environment:

```bash
make jupyter
```

Notebooks are located in `scripts/notebooks/`.

## Project Structure

```
project/
├── src/                # Main source code
├── tests/              # Unit tests
├── scripts/            # Jupyter notebooks and helper scripts
├── data/               # Input or reference data
├── logs/               # Application logs
├── docs/               # Documentation
├── Makefile            # Command shortcuts
├── .env                # Environment variables
├── requirements.txt    # Dependencies
├── pyproject.toml      # Configuration for tooling
└── README.md           # Project information
```

## License

This project is licensed under the terms of the LICENSE file.

