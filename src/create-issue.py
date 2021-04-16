from commentjson import loads

from jira import JIRA
from pydantic import AnyHttpUrl, BaseSettings, SecretStr


class Settings(BaseSettings):
    class Config:
        env_prefix = "INPUT_"

    JIRA_USERNAME: str
    JIRA_PASSWORD: SecretStr
    JIRA_BASE_URL: AnyHttpUrl

    PROJECT: str

    ISSUE_TITLE: str
    ISSUE_ASSIGNEE: str
    ISSUE_TITLE: str
    ISSUE_BODY: str
    ISSUE_TYPE: str = "Task"
    ISSUE_FIELDS: str = "{}"


settings = Settings()

jira = JIRA(
    settings.JIRA_BASE_URL,
    auth=(settings.JIRA_USERNAME, settings.JIRA_PASSWORD.get_secret_value()),
)

required_fields = {
    "project": settings.PROJECT,
    "summary": settings.ISSUE_TITLE,
    "description": settings.ISSUE_BODY,
    "issuetype": {"name": settings.ISSUE_TYPE},
}
optional_fields = loads(settings.ISSUE_FIELDS)

issue_fields = optional_fields | required_fields
issue = jira.create_issue(fields=issue_fields)

print(f"JIRA issue {issue.key} created successfully")

print(f"::set-output name=jira-issue-key::{issue.key}")
print(f"::set-output name=jira-issue-url::{issue.permalink()}")
