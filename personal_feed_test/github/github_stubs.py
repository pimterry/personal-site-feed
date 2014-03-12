from datetime import datetime, timezone

def event(event_type, timestamp=None, actor="pimterry"):
    if not timestamp:
        timestamp = datetime.now(timezone.utc)

    return {
        "created_at": timestamp.isoformat(),
        "actor": actor,
        "type": event_type,
        "repository": {
            "owner": "junit-team",
            "name": "junit"
        }
    }

def pushEvent(commit_message, timestamp=None, actor="pimterry"):
    eventData = event("PushEvent", timestamp, actor)
    eventData.update({
        "payload": {
            "shas": [
                ["hash123123", "username@example.com", commit_message]
            ]
        }
    })
    return eventData

def pullRequestEvent(pull_request_title, timestamp=None, actor="pimterry"):
    eventData = event("PullRequestEvent", timestamp, actor)
    eventData.update({
        "payload": {
            "pull_request": {
                "title": pull_request_title
            }
        }
    })
    return eventData

def forkEvent(timestamp=None, actor="pimterry"):
    return event("ForkEvent", timestamp, actor)