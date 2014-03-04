import unittest
from unittest.mock import patch
from collections import defaultdict

from personal_feed.main import build_app

class IntegrationTests(unittest.TestCase):
    def test_root_page_throws_no_exceptions(self):
        client = self.buildClient()
        client.get('/')

    def buildClient(self, envSettings={}):
        defaultEnv = defaultdict(lambda: None)
        defaultEnv.update(envSettings)
        self.patchEnvWithMock(defaultEnv)
        self.patchFeeds()

        app = build_app()
        app.testing = True

        return app.test_client()

    def patchEnvWithMock(self, envMock):
        envPatcher = patch("os.environ", new=envMock)
        self.envMock = envPatcher.start()
        self.addCleanup(envPatcher.stop)

    def patchFeeds(self):
        twitterPatch = patch("personal_feed.twitter_feed.Twython")
        self.twitterMock = twitterPatch.start()
        self.addCleanup(twitterPatch.stop)

        requestsPatch = patch("personal_feed.github_feed.requests")
        self.requestsMock = requestsPatch.start()
        self.addCleanup(requestsPatch.stop)