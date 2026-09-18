from fastmcp import FastMCP
from typing import List
from src.integrations.github_client import user
branch_management_mcp = FastMCP("branch-management")

@branch_management_mcp.tool
def create_branch(repo_name: str, new_branch_name: str, base_branch_name: str
) -> str:
    """
    Create a new branch in a GitHub repository.

    Args:
        repo_name: The name of the repository.
        new_branch_name: The name of the new branch to create.
        base_branch_name: The name of the base branch from which to create the new branch.  

    Returns:
        A message containing the name of the created branch.    
    """
    try:
        repo = user.get_repo(repo_name)
        base_branch = repo.get_branch(base_branch_name)
        repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=base_branch.commit.sha)
        return f"Branch '{new_branch_name}' created successfully in repository '{repo_name}'."
    except Exception as e:
        raise ValueError(f"Failed to create branch: {e}")


@branch_management_mcp.tool
def list_branches(repo_name: str) -> List[str]:
    """
    List all branches in a GitHub repository.

    Args:
        repo_name: The name of the repository.

    Returns:
        A list of branch names.
    """
    try:
        repo = user.get_repo(repo_name)
        branches = repo.get_branches()
        return [branch.name for branch in branches]
    except Exception as e:
        raise ValueError(f"Failed to list branches: {e}")


@branch_management_mcp.tool
def delete_branch(repo_name: str, branch_name: str) -> str:
    """
    Delete a branch in a GitHub repository.

    Args:
        repo_name: The name of the repository.
        branch_name: The name of the branch to delete.  

    Returns:
        A message confirming the deletion of the branch.
    """
    try:
        repo = user.get_repo(repo_name)
        ref = repo.get_git_ref(f"heads/{branch_name}")
        ref.delete()
        return f"Branch '{branch_name}' deleted successfully from repository '{repo_name}'."
    except Exception as e:
        raise ValueError(f"Failed to delete branch: {e}")

@branch_management_mcp.tool
def get_default_branch(repo_name: str) -> str:
    """
    Get the default branch of a GitHub repository.

    Args:
        repo_name: The name of the repository.

    Returns:
        The name of the default branch.
    """
    try:
        repo = user.get_repo(repo_name)
        return repo.default_branch
    except Exception as e:
        raise ValueError(f"Failed to get default branch: {e}")
    