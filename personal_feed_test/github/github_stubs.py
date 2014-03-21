from datetime import datetime, timezone

def githubEvent(event_type, timestamp=None, actor="pimterry"):
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
    eventData = githubEvent("PushEvent", timestamp, actor)
    eventData.update({
        "payload": {
            "shas": [
                ["hash123123", "username@example.com", commit_message]
            ]
        }
    })
    return eventData

def pullRequestEvent(pull_request_title, timestamp=None, actor="pimterry"):
    eventData = githubEvent("PullRequestEvent", timestamp, actor)
    eventData.update({
        "payload": {
            "pull_request": {
                "title": pull_request_title
            }
        }
    })
    return eventData

def starEvent(repo_name, owner="knockout", timestamp=None, actor="pimterry"):
    eventData = githubEvent("WatchEvent", timestamp, actor)
    eventData.update({
        "payload": {
            "action": "started"
        },
        "repository": {
            "name": repo_name,
            "owner": owner
        }
    })
    return eventData

def forkEvent(repo_name, owner="junit-team", timestamp=None, actor="pimterry"):
    eventData = githubEvent("ForkEvent", timestamp, actor)
    eventData.update({
        "repository": {
            "name": repo_name,
            "owner": owner
        }
    })
    return eventData

def createdRepo(repoName, timestamp=None, actor="pimterry"):
    eventData = githubEvent("CreateEvent", timestamp, actor)
    eventData.update({
        "payload": {
            "ref_type": "repository"
        },
        "repository": {
            "name": repoName,
            "owner": actor
        }
    })
    return eventData

def createdBranch(branchName, timestamp=None, actor="pimterry"):
    eventData = githubEvent("CreateEvent", timestamp, actor)
    eventData.update({
        "payload": {
            "ref_type": "branch",
            "ref": branchName
        },
        "repository": {
            "name": "repo-name-for-branch"
        }
    })
    return eventData