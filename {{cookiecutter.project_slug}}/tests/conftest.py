import pytest
from flask_webtest import TestApp

from project import app


@pytest.fixture
def flask_webtest(request):
    request.cls.app = TestApp(app)
