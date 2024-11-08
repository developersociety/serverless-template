import pytest

import project


@pytest.fixture
def app():
    return project.app
