import pytest
from sphinx.testing.path import path

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir() -> path:
    return path(__file__).parent.abspath() / "roots"
