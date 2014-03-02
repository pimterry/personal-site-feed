from functools import total_ordering
import unittest
from unittest.mock import Mock

from personal_feed.aggregated_feed import AggregatedFeed

class AggregatedFeedTest(unittest.TestCase):
    def test_should_combine_given_feeds(self):
        feed1 = feedMock(MockItem(1), MockItem(3), MockItem(5))
        feed2 = feedMock(MockItem(2), MockItem(5))

        aggregated_feed = AggregatedFeed([feed1, feed2])

        self.assertEquals([1,2,3,5,5], [x.id for x in aggregated_feed.feed_items])

@total_ordering
class MockItem:
    def __init__(self, id):
        self.id = id

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self is other


def feedMock(*items):
    return Mock(**{"feed_items": items})