from fastmcp import FastMCP
from src.mcp_server.tools.repository_management import repository_management_mcp
from src.mcp_server.tools.commits import commits_mcp
from src.mcp_server.tools.pull_requests import pull_requests_mcp
from src.mcp_server.tools.issue_tracking import issue_tracking_mcp
from src.mcp_server.tools.branch_management import branch_management_mcp

# creating mcp server instance
mcp_server = FastMCP("Github MCP Server",
instructions="This is a server that provides tools to interact with GitHub repositories. " \
"It allows you to manage repositories, commits, pull requests, issues, and branches."
                     )

mcp_server.mount(repository_management_mcp)
mcp_server.mount(commits_mcp)
mcp_server.mount(pull_requests_mcp)
mcp_server.mount(issue_tracking_mcp)
mcp_server.mount(branch_management_mcp)

if __name__ == "__main__":
    # Start the MCP server
    mcp_server.run(transport="http", host="0.0.0.0", port=8000)
