from random import choice, randint
from twython import Twython

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

class TwitterFeedItem:
    def __init__(self, tweet):
        self.feed_template = "twitter_feed_item.html"
        self.tweet = tweet
        self.id = randint(0, 100)

    def __lt__(self, other):
        return self.id < other.id

class TweetFeedItem(TwitterFeedItem):
    @property
    def description(self):
        return "@%s tweeted: '%s'" % (self.tweet["user"]["screen_name"], self.tweet["text"])

class RetweetFeedItem(TwitterFeedItem):
    @property
    def description(self):
        return "@%s retweeted: '%s'" % (self.tweet["user"]["screen_name"], self.tweet["text"])