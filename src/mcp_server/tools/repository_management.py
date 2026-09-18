from fastmcp import FastMCP
from src.integrations.github_client import user
from typing import List


repository_management_mcp = FastMCP("repository-management")


@repository_management_mcp.tool

def create_repository(
    repo_name: str,
    description: str = "",
    private: bool = True,
) -> str:
    """
    Create a new GitHub repository.

    Args:
        repo_name: The name of the repository to create.
        description: A short description of the repository.
        private: Whether the repository should be private.

    Returns:
        A message containing the full name of the created repository.
    """
    try:
        repo = user.create_repo(
            name=repo_name,
            description=description,
            private=private,
        )
        return f"Repository created successfully: {repo.full_name}"
    except Exception as e:
        raise ValueError(f"Failed to create repository: {e}")

@repository_management_mcp.tool
def list_repositories() -> List[str]:
    """
    List all repositories for the authenticated user.

    Returns:
        A list of repository names.
    """
    try:
        repos = user.get_repos()
        return [repo.full_name for repo in repos]
    except Exception as e:
        raise ValueError(f"Failed to list repositories: {e}")


@repository_management_mcp.tool
def delete_repository(repo_name: str) -> str:
    """
    Delete a GitHub repository.

    Args:
        repo_name: The name of the repository to delete.

    Returns:
        A message indicating the result of the deletion.
    """
    try:
        repo = user.get_repo(repo_name)
        repo.delete()
        return f"Repository deleted successfully: {repo_name}"
    except Exception as e:
        raise ValueError(f"Failed to delete repository: {e}")



@repository_management_mcp.tool
def get_repository_info(repo_name: str) -> dict:
    """
    Get information about a specific GitHub repository.

    Args:
        repo_name: The name of the repository.

    Returns:
        A dictionary containing repository information.
    """
    try:
        repo = user.get_repo(repo_name)
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "private": repo.private,
            "url": repo.html_url,
            "created_at": str(repo.created_at),
            "updated_at": str(repo.updated_at),
            "pushed_at": str(repo.pushed_at),
            "stargazers_count": repo.stargazers_count,
            "watchers_count": repo.watchers_count,
            "forks_count": repo.forks_count,
        }
    except Exception as e:
        raise ValueError(f"Failed to get repository info: {e}")
    
