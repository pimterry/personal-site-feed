from datetime import datetime
import unittest
from unittest.mock import patch
from collections import defaultdict

from personal_feed.main import build_app
from .github.github_stubs import *

def mockTweet(text, timestamp=None, retweeted=False, username="pimterry"):
    if not timestamp:
        timestamp = datetime.now()

    return {
        "retweeted": retweeted,
        "created_at": timestamp.strftime('%a %b %d %H:%M:%S +0000 %Y'),
        "text": text,
        "user": { "screen_name": username }
    }

class IntegrationTests(unittest.TestCase):
    def test_root_page_pulls_tweets(self):
        client = self.buildClient()
        self.twitterMock.get_user_timeline.return_value = [
            mockTweet("a tweet"), mockTweet("another tweet", retweeted=True)
        ]

        result = str(client.get('/').data)

        self.assertIn("a tweet", result)
        self.assertIn("another tweet", result)

    def test_root_page_pulls_github_events(self):
        client = self.buildClient()

        self.requestsMock.get.return_value.json.return_value = [
            pushEvent("my-first-commit"),
            forkEvent("forked-repo"),
            createdBranch("a branch"),
            pullRequestEvent("a-pull-request"),
            starEvent("starred-repo"),
            createdRepo("new repo"),
        ]
        result = str(client.get('/').data)

        self.assertIn("my-first-commit", result)
        self.assertIn("forked-repo", result)
        self.assertIn("a-pull-request", result)
        self.assertIn("starred-repo", result)
        self.assertIn("new repo", result)
        self.assertNotIn("a branch", result)

    def test_blog_route_redirects_to_real_blog(self):
        client = self.buildClient()
        result = client.get('/blog/2011/12/26/Third_Time_Lucky',
                            follow_redirects=False)

        self.assertEqual(301, result.status_code)
        self.assertEqual("http://blog.tim-perry.co.uk/third-time-lucky",
                         result.headers["location"])

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
        twitterPatch = patch("personal_feed.twitter.twitter_feed.Twython")
        self.twitterMock = twitterPatch.start().return_value
        self.addCleanup(twitterPatch.stop)

        requestsPatch = patch("personal_feed.github.github_feed.requests")
        self.requestsMock = requestsPatch.start()
        self.addCleanup(requestsPatch.stop)
