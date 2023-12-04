import app
import unittest


@unittest.skip("reason for skipping")
def test_handler():
    app.handler({}, None)
