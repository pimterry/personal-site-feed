import functools
import requests
import dateutil.parser

def get_created_date(event):
    return dateutil.parser.parse(event["created_at"])

@functools.total_ordering
class GithubFeedItem:
    def __init__(self, event):
        self.feed_template = "github_feed_item.html"
        self.timestamp = get_created_date(event)

    def __lt__(self, other):
        return self.timestamp < other.timestamp

class GithubPullRequestFeedItem(GithubFeedItem):
    @property
    def description(self):
        return "A Pull Request"

class GithubReleaseFeedItem(GithubFeedItem):
    @property
    def description(self):
        return "A New Release"

class GithubCreateRepositoryFeedItem(GithubFeedItem):
    @property
    def description(self):
        return "Created repository"

class GithubWatchFeedItem(GithubFeedItem):
    @property
    def description(self):
        return "Watched something"

class GithubForkFeedItem(GithubFeedItem):
    @property
    def description(self):
        return "Fork something"

class GithubCommitsEvent(GithubFeedItem):
    def __init__(self, events):
        print(events)
        super().__init__(max(events, key=lambda e: get_created_date(e)))

    @property
    def description(self):
        return "Some commits"

class GithubFeed:
    def __init__(self, username):
        self.username = username

    def _get_user_events(self, username):
        response = requests.get("https://github.com/%s.json" % username)
        return response.json()

    def _get_items_for_events(self, events):
        partial_commit_list = []

        for event in events:
            if event["type"] == "PushEvent":
                partial_commit_list.append(event)
            elif event["type"] in event_type_map:
                if partial_commit_list:
                    yield GithubCommitsEvent(partial_commit_list)
                    partial_commit_list = []

                yield event_type_map[event["type"]](event)
            else:
                continue

        if partial_commit_list:
            yield GithubCommitsEvent(partial_commit_list)

    @property
    def feed_items(self):
        return self._get_items_for_events(self._get_user_events(self.username))

event_type_map = {
    "PullRequestEvent": GithubPullRequestFeedItem,
    "ForkEvent": GithubForkFeedItem,
    "CreateEvent": GithubCreateRepositoryFeedItem,
    "WatchEvent": GithubWatchFeedItem,
    "ReleaseEvent": GithubReleaseFeedItem
}