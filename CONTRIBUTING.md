# Contributing

[UV](https://docs.astral.sh/uv/getting-started/installation/) is the only required development dependency, all of the python dependencies are bootstrapped using UV.

## Install Dependencies

    uv sync

## Run the Tests

    uv run pytest

## Lint

    uv run pre-commit run --all-files

## Install Pre-Commit Hooks (optional)

    uv run pre-commit install

## Build the Documentation

    cd docs/
    uv run make html

then open `docs/_build/html/index.html` in a browser
