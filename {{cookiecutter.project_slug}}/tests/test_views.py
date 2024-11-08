import unittest

import pytest


@pytest.mark.usefixtures("client_class")
class TestViews(unittest.TestCase):
    def test_root(self):
        response = self.client.get("/")

        assert response.status_code == 200
        assert "Hello, world!" in response.get_data(as_text=True)
