import pytest
from flask_webtest import TestApp

from {{ cookiecutter.project_slug }} import app


@pytest.fixture
def flask_webtest(request):
    request.cls.app = TestApp(app)
