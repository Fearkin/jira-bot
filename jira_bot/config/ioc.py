from dishka import Provider, Scope, make_async_container
from jira import JIRA
from jira_bot.config.settings import config


def get_jira_conn() -> JIRA:
    """Returns connection to cloud Jira instance"""
    return JIRA(
        server=config.jira_url,
        basic_auth=(config.jira_email, config.jira_token.get_secret_value()),
    )


provider = Provider()
provider.provide(get_jira_conn, scope=Scope.APP)
container = make_async_container(provider)
