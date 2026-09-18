from fastmcp import FastMCP
from src.integrations.github_client import user
from typing import List

commits_mcp = FastMCP("commits")

@commits_mcp.tool
def list_commits(repo_name: str, branch_name: str) -> List[str]:
    """
    List all commits in a specific branch of a GitHub repository.

    Args:
        repo_name: The name of the repository.
        branch_name: The name of the branch.

    Returns:

        A list of commit messages.
    """
    try:
        repo = user.get_repo(repo_name)
        commits = repo.get_commits(sha=branch_name)
        return [commit.commit.message for commit in commits]
    except Exception as e:
        raise ValueError(f"Failed to list commits: {e}")


@commits_mcp.tool
def get_commit_details(repo_name: str, commit_sha: str) -> dict:
    """
    Get details of a specific commit in a GitHub repository.

    Args:
        repo_name: The name of the repository.
        commit_sha: The SHA of the commit.

    Returns:
        A dictionary containing commit details such as author, date, and message.
    """

    try:
        repo = user.get_repo(repo_name)
        commit = repo.get_commit(commit_sha)
        return {
            "author": commit.commit.author.name,
            "date": commit.commit.author.date.isoformat(),
            "message": commit.commit.message,
            "sha": commit.sha,
        }
    except Exception as e:
        raise ValueError(f"Failed to get commit details: {e}")


@commits_mcp.tool
def compare_commits(repo_name: str, base_commit_sha: str, head_commit_sha:
    str) -> dict:
        """
        Compare two commits in a GitHub repository.
    
        Args:
            repo_name: The name of the repository.
            base_commit_sha: The SHA of the base commit.
            head_commit_sha: The SHA of the head commit.

        Returns:
            A dictionary containing the comparison details, including the list of files changed and the number of additions and deletions.
        """
        
        try:
            repo = user.get_repo(repo_name)
            comparison = repo.compare(base_commit_sha, head_commit_sha)
            return {
                "base_commit": base_commit_sha,
                "head_commit": head_commit_sha,
                "files_changed": [file.filename for file in comparison.files],
                "additions": comparison.additions,
                "deletions": comparison.deletions,
                "total_changes": comparison.total_changes,
            }
        except Exception as e:
            raise ValueError(f"Failed to compare commits: {e}")
        
