from random import choice

class GithubFeed:
    @property
    def feed_items(self):
        for x in range(200):
            yield choice([GithubPullRequestFeedItem(),
                          GithubNewRepositoryFeedItem(),
                          GithubReleaseFeedItem(),
                          GithubCommitsFeedItem()])

class GithubFeedItem:
    def __init__(self):
        self.feed_template = "github_feed_item.html"

class GithubPullRequestFeedItem(GithubFeedItem):
    @property
    def description(self):
        return "A Pull Request"

class GithubNewRepositoryFeedItem(GithubFeedItem):
    @property
    def description(self):
        return "A New Repo"

class GithubReleaseFeedItem(GithubFeedItem):
    @property
    def description(self):
        return "A New Release"

class GithubCommitsFeedItem(GithubFeedItem):
    @property
    def description(self):
        return "Some commits"