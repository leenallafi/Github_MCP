from fastmcp import FastMCP
from src.integrations.github_client import user

issue_tracking_mcp = FastMCP("issue_tracking")

@issue_tracking_mcp.tool
def list_issues(repo_name: str) -> list:
    """
    List all issues in a GitHub repository.

    Args:
        repo_name: The name of the repository.
    Returns:
        A list of issue titles.
    """
    try:
        repo = user.get_repo(repo_name)
        issues = repo.get_issues(state='open')
        return [issue.title for issue in issues]
    except Exception as e:
        raise ValueError(f"Failed to list issues: {e}")

@issue_tracking_mcp.tool
def create_issue(repo_name: str, title: str, body: str) -> str:
    """
    Create a new issue in a GitHub repository.

    Args:
        repo_name: The name of the repository.
        title: The title of the issue.
        body: The body/description of the issue.
    Returns:
        A message confirming the creation of the issue.
    """
    try:
        repo = user.get_repo(repo_name)
        issue = repo.create_issue(title=title, body=body)
        return f"Issue '{issue.title}' created successfully in repository '{repo_name}'."
    except Exception as e:
        raise ValueError(f"Failed to create issue: {e}")
    

@issue_tracking_mcp.tool
def close_issue(repo_name: str, issue_number: int) -> str:
    """
    Close an issue in a GitHub repository.

    Args:
        repo_name: The name of the repository.
        issue_number: The number of the issue to close.
    Returns:
        A message confirming the closure of the issue.
    """
    try:
        repo = user.get_repo(repo_name)
        issue = repo.get_issue(number=issue_number)
        issue.edit(state='closed')
        return f"Issue '{issue.title}' closed successfully in repository '{repo_name}'."
    except Exception as e:
        raise ValueError(f"Failed to close issue: {e}")


