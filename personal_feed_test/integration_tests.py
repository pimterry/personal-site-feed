import unittest
from unittest.mock import patch

from personal_feed.main import build_app

class IntegrationTests(unittest.TestCase):
    def test_root_page_throws_no_exceptions(self):
        client = self.buildClient()
        client.get('/')

    def buildClient(self, envSettings={}):
        defaultEnv = {}
        defaultEnv.update(envSettings)
        self.patchEnvWithMock(defaultEnv)

        app = build_app()
        app.testing = True

        return app.test_client()

    def patchEnvWithMock(self, envMock):
        envPatcher = patch("os.environ", new=envMock)
        self.envMock = envPatcher.start();
        self.addCleanup(envPatcher.stop)