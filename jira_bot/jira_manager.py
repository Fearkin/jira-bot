from jira import JIRA
import structlog

from jira_bot.utils import Ticket
from jira_bot.config.settings import config

log = structlog.stdlib.get_logger(__name__)


def create_ticket(data: Ticket, jira: JIRA) -> None:
    """Creates ticket via Jira"""
    log.info("creating issue")
    fields = {
        "project": config.issue_key,
        "summary": data.problem_name,
        "description": data.problem_desc,
        "issuetype": {"name": "Task"},
        "reporter": {"accountId": config.jira_id.get_secret_value()},
        "customfield_10032": data.username,
        "customfield_10033": data.problem_type,
        "customfield_10034": data.project,
    }
    issue = jira.create_issue(fields=fields)
    fields["key"] = issue.key
    return fields
