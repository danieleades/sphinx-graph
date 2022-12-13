# Contributing

[Poetry](https://python-poetry.org/) is the only required development dependency, all of the python dependencies are bootstrapped using Poetry.

[Pre-commit](https://pre-commit.com/) is an optional local development dependency, and is used for linting the project in CI

## Install Dependencies

    poetry install

## Run the Tests

    poetry run pytest

## Lint

    pre-commit run --all-files

## Install Pre-Commit Hooks (optional)

    pre-commit install

## Build the Documentation

    cd docs/
    poetry run make html

then open `docs/_build/html/index.html` in a browser
