from random import choice, randint

class TwitterFeed:
    @property
    def feed_items(self):
        for x in range(200):
            yield choice([TweetFeedItem(),
                          RetweetFeedItem()])

class TwitterFeedItem:
    def __init__(self):
        self.feed_template = "twitter_feed_item.html"
        self.id = randint(0, 100)

    def __lt__(self, other):
        return self.id < other.id

class TweetFeedItem(TwitterFeedItem):
    @property
    def description(self):
        return "@pimterry tweeted: 'Tweets!'"

class RetweetFeedItem(TwitterFeedItem):
    @property
    def description(self):
        return "@pimterry retweeted something!"