import unittest

import pytest


@pytest.mark.usefixtures("flask_webtest")
class TestViews(unittest.TestCase):

    def test_root(self):
        response = self.app.get("/")

        assert response.status_int == 200
        assert "Hello, world!" in response
