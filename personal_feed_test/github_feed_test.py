from flask import json
import unittest
from unittest.mock import Mock, patch

from personal_feed.github_feed import *

@patch("personal_feed.github_feed.requests")
class GithubFeedTest(unittest.TestCase):
    def test_should_make_request_for_username(self, requests_mock):
        username = "pimterry"
        requests_mock.get.return_value = mockResponse([forkEvent()])

        list(GithubFeed(username).feed_items)

        requests_mock.get.assert_called_once_with("https://github.com/pimterry.json")

    def test_should_ignore_unrecognized_events(self, requests_mock):
        requests_mock.get.return_value = mockResponse([event("ImaginaryEvent")])

        self.assertEqual(0, len(list(GithubFeed("pimterry").feed_items)))

    def test_should_batch_push_events(self, requests_mock):
        requests_mock.get.return_value = mockResponse([
            event("PushEvent"), event("PushEvent"), event("PushEvent")
        ])

        self.assertEqual(1, len(list(GithubFeed("pimterry").feed_items)))

class mockResponse:
    def __init__(self, jsonData):
        self.jsonData = jsonData

    def json(self):
        return self.jsonData

def event(event_type, timestamp=123123123, actor="pimterry"):
    return {
        "created_at": timestamp,
        "actor": actor,
        "type": event_type
    }

def forkEvent(timestamp=123123123, actor="pimterry"):
    return {
        "created_at": timestamp,
        "actor": actor,
        "type": "ForkEvent",
        "repository": {
            "owner": "junit-team",
            "name": "junit"
        }
    }