from fastmcp import FastMCP
from src.integrations.github_client import user

pull_requests_mcp = FastMCP("pull_requests")

@pull_requests_mcp.tool
def list_pull_requests(repo_name: str) -> list:
    """
    List all pull requests in a GitHub repository.

    Args:
        repo_name: The name of the repository.

    Returns:
        A list of pull request titles.
    """
    try:
        repo = user.get_repo(repo_name)
        pull_requests = repo.get_pulls(state='open')
        return [pr.title for pr in pull_requests]
    except Exception as e:
        raise ValueError(f"Failed to list pull requests: {e}")

@pull_requests_mcp.tool
def create_pull_request(repo_name: str, title: str, body: str, head: str, base: str) -> str:
    """
    Create a new pull request in a GitHub repository.

    Args:
        repo_name: The name of the repository.
        title: The title of the pull request.
        body: The body/description of the pull request.
        head: The name of the branch where your changes are implemented.
        base: The name of the branch you want the changes pulled into.

    Returns:

        A message confirming the creation of the pull request.
    """
    try:
        repo = user.get_repo(repo_name)
        pr = repo.create_pull(title=title, body=body, head=head, base=base)
        return f"Pull request '{pr.title}' created successfully in repository '{repo_name}'."
    except Exception as e:
        raise ValueError(f"Failed to create pull request: {e}")

@pull_requests_mcp.tool
def merge_pull_request(repo_name: str, pull_number: int) -> str:
    """
    Merge a pull request in a GitHub repository.

    Args:
        repo_name: The name of the repository.
        pull_number: The number of the pull request to merge.

    Returns:
        A message confirming the merge of the pull request.
    """
    try:
        repo = user.get_repo(repo_name)
        pr = repo.get_pull(pull_number)
        pr.merge()
        return f"Pull request #{pull_number} merged successfully in repository '{repo_name}'."
    except Exception as e:
        raise ValueError(f"Failed to merge pull request: {e}")


@pull_requests_mcp.tool
def close_pull_request(repo_name: str, pull_number: int) -> str:
    """
    Close a pull request in a GitHub repository.

    Args:
        repo_name: The name of the repository.
        pull_number: The number of the pull request to close.

    Returns:
        A message confirming the closure of the pull request.
    """
    try:
        repo = user.get_repo(repo_name)
        pr = repo.get_pull(pull_number)
        pr.edit(state='closed')
        return f"Pull request #{pull_number} closed successfully in repository '{repo_name}'."
    except Exception as e:
        raise ValueError(f"Failed to close pull request: {e}")


@pull_requests_mcp.tool
def summarize_pull_request(repo_name: str, pull_number: int) -> str:
    """
    Summarize a pull request in a GitHub repository.

    Args:
        repo_name: The name of the repository.
        pull_number: The number of the pull request to summarize.

    Returns:
        A summary of the pull request, including title, body, and state.
    """
    try:
        repo = user.get_repo(repo_name)
        pr = repo.get_pull(pull_number)
        summary = f"Title: {pr.title}\nBody: {pr.body}\nState: {pr.state}"
        return summary
    except Exception as e:
        raise ValueError(f"Failed to summarize pull request: {e}")


