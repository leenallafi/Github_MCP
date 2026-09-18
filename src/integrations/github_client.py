import os
from dotenv import load_dotenv
from github import Github

load_dotenv()
# Load environment variables from .env file

GITHUB_PAT = os.getenv("GITHUB_PAT")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

# Validate that the required environment variables are set

if not GITHUB_PAT or not GITHUB_USERNAME:
    raise ValueError("GITHUB_PAT and GITHUB_USERNAME must be set in the .env file.")

try:
    # Authenticate with GitHub using the provided personal access token and username
    g = Github(GITHUB_PAT)
    user = g.get_user(GITHUB_USERNAME)
except Exception as e:
    raise ValueError(f"Failed to authenticate with GitHub: {e}")

