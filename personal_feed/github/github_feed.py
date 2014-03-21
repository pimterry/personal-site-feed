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
    def __init__(self, event):
        super().__init__(event)
        self.event = event

    @classmethod
    def matches_data(cls, event_data):
        return event_data["type"] == "PullRequestEvent"

    @property
    def description(self):
        return self.event["payload"]["pull_request"]["title"]

class GithubReleaseFeedItem(GithubFeedItem):
    @classmethod
    def matches_data(cls, event_data):
        return event_data["type"] == "ReleaseEvent"

    @property
    def description(self):
        return "A New Release"

class GithubCreateRepositoryFeedItem(GithubFeedItem):
    def __init__(self, event):
        super().__init__(event)
        self.repo_name = event["repository"]["name"]

    @classmethod
    def matches_data(cls, event_data):
        return (event_data["type"] == "CreateEvent" and
                event_data["payload"]["ref_type"] == "repository")

    @property
    def description(self):
        return "Created repository '%s'" % self.repo_name

class GithubWatchFeedItem(GithubFeedItem):
    def __init__(self, event):
        super().__init__(event)
        self.repo_owner = event["repository"]["owner"]
        self.repo_name = event["repository"]["name"]

    @classmethod
    def matches_data(cls, event_data):
        return (event_data["type"] == "WatchEvent" and
                event_data["payload"]["action"] == "started")

    @property
    def description(self):
        return "Starred %s/%s" % (self.repo_owner, self.repo_name)

class GithubForkFeedItem(GithubFeedItem):
    def __init__(self, event):
        super().__init__(event)
        self.repo_owner = event["repository"]["owner"]
        self.repo_name = event["repository"]["name"]

    @classmethod
    def matches_data(cls, event_data):
        return event_data["type"] == "ForkEvent"

    @property
    def description(self):
        return "Forked %s/%s" % (self.repo_owner, self.repo_name)

class GithubCommitsEvent(GithubFeedItem):
    def __init__(self, events):
        self.events = events
        self.feed_template = "github_commits_feed_item.html"
        self.timestamp = max(get_created_date(e) for e in events)

    @property
    def repositories(self):
        return set("%s/%s" % (e["repository"]["owner"], e["repository"]["name"])
                   for e in self.events)

    @property
    def commit_messages(self):
        for event in self.events:
            for commit in event["payload"]["shas"]:
                yield commit[2]

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

            EventClass = next((e for e in event_classes if e.matches_data(event)), None)

            if EventClass:
                if partial_commit_list:
                    yield GithubCommitsEvent(partial_commit_list)
                    partial_commit_list = []

                yield EventClass(event)

        if partial_commit_list:
            yield GithubCommitsEvent(partial_commit_list)

    @property
    def feed_items(self):
        return self._get_items_for_events(self._get_user_events(self.username))

event_classes = [
    GithubPullRequestFeedItem,
    GithubForkFeedItem,
    GithubCreateRepositoryFeedItem,
    GithubWatchFeedItem,
    GithubReleaseFeedItem
]