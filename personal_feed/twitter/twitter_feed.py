from datetime import datetime
from twython import Twython
import functools

DATE_FORMAT = '%a %b %d %H:%M:%S %z %Y'

class TwitterFeed:
    def __init__(self, app_key, app_token, access_token, access_token_secret, username):
        self.twitter = Twython(app_key, app_token, access_token, access_token_secret)
        self.username = username

    @property
    def feed_items(self):
        results = self.twitter.get_user_timeline(screen_name=self.username, count=20)

        for tweet in results:
            if tweet["retweeted"]:
                yield RetweetFeedItem(tweet)
            else:
                yield TweetFeedItem(tweet)

@functools.total_ordering
class TwitterFeedItem:
    def __init__(self, tweet):
        self.feed_template = "twitter_feed_item.html"
        self.tweet = tweet
        self.timestamp = datetime.strptime(tweet["created_at"], DATE_FORMAT)

    def __lt__(self, other):
        return self.timestamp < other.timestamp

class TweetFeedItem(TwitterFeedItem):
    @property
    def description(self):
        return "Tweeted: '%s'" % (self.tweet["text"], )

class RetweetFeedItem(TwitterFeedItem):
    @property
    def description(self):
        return "Retweeted: '%s'" % (self.tweet["text"], )