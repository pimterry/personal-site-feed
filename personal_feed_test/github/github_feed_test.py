from datetime import datetime, timedelta, timezone
import unittest
from unittest.mock import patch

from .github_stubs import *
from personal_feed.github.github_feed import *

def n_consecutive_days(n):
    now = datetime.now(timezone.utc)
    oneDay = timedelta(1)

    return [now + i*oneDay for i in range(n)]

@patch("personal_feed.github.github_feed.requests")
class GithubFeedTest(unittest.TestCase):
    def test_should_make_request_for_username(self, requests_mock):
        username = "pimterry"
        requests_mock.get.return_value = mockResponse([githubEvent("MiscEvent")])

        list(GithubFeed(username).feed_items)

        requests_mock.get.assert_called_once_with("https://github.com/pimterry.json")

    def test_should_ignore_unrecognized_events(self, requests_mock):
        requests_mock.get.return_value = mockResponse([githubEvent("MiscEvent")])

        self.assertEqual(0, len(list(GithubFeed("pimterry").feed_items)))

    def test_should_track_timestamps_on_items(self, requests_mock):
        datetimes = n_consecutive_days(3)
        requests_mock.get.return_value = mockResponse([
            forkEvent("repo", timestamp=datetimes[0]),
            forkEvent("repo2", timestamp=datetimes[1]),
            forkEvent("repo3", timestamp=datetimes[2])
        ])

        feed_items = list(GithubFeed("pimterry").feed_items)

        self.assertListEqual([d.date() for d in datetimes],
                             [i.timestamp.date() for i in feed_items])

    def test_should_build_new_repo_events(self, requests_mock):
        requests_mock.get.return_value = mockResponse([
            createdRepo("RepoName")
        ])

        items = list(GithubFeed("pimterry").feed_items)
        self.assertEqual(1, len(items))
        self.assertEqual("Created repository 'RepoName'", items[0].description)

    def test_should_not_build_new_branch_events(self, requests_mock):
        requests_mock.get.return_value = mockResponse([
            createdBranch("BranchName")
        ])

        items = list(GithubFeed("pimterry").feed_items)
        self.assertEqual(0, len(items))


    def test_should_batch_push_events(self, requests_mock):
        requests_mock.get.return_value = mockResponse([
            githubEvent("PushEvent"), githubEvent("PushEvent"), githubEvent("PushEvent")
        ])

        self.assertEqual(1, len(list(GithubFeed("pimterry").feed_items)))

class mockResponse:
    def __init__(self, jsonData):
        self.jsonData = jsonData

    def json(self):
        return self.jsonData

