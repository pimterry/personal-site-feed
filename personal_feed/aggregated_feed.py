class AggregatedFeed:
    def __init__(self, feeds):
        self.feeds = feeds

    @property
    def feed_items(self):
        return sorted([item for feed in self.feeds
                            for item in feed.feed_items],
                      reverse=True)