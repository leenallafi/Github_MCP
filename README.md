# GitHub MCP Assistant

An AI-powered GitHub assistant built with **Model Context Protocol (MCP)**, **FastMCP**, **Google Gemini**, **FastAPI** and **Streamlit**.

The assistant allows users to interact with GitHub using natural-language requests. Gemini selects the appropriate MCP tool, which executes the requested GitHub operation through the GitHub API.

## Overview

```text
┌──────────────────────┐
│      Streamlit       │
│       Chat UI        │
└──────────┬───────────┘
           │ HTTP
           ▼
┌──────────────────────┐
│      FastAPI         │
│     MCP Client       │
│  Gemini Integration  │
└──────────┬───────────┘
           │ MCP / HTTP
           ▼
┌──────────────────────┐
│      FastMCP         │
│     MCP Server       │
│                      │
│     GitHub Tools     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      GitHub API      │
└──────────────────────┘
```

### Request Flow

1. User sends a request through Streamlit.
2. FastAPI forwards the request to Gemini with the available MCP tools.
3. Gemini selects the appropriate tool.
4. The MCP client communicates with the FastMCP server.
5. The selected tool performs the GitHub operation through PyGithub.
6. The result is returned to Gemini and displayed to the user.

## Features

* Repository management
* Commit operations
* Pull requests
* Issue tracking
* Branch management
* Natural-language GitHub interaction
* Dockerized client, server, and UI

Example requests:

```text
List my GitHub repositories.

Show the branches in my repository.

Create an issue in my repository.

Show the pull requests for this repository.

List recent commits.
```

## Project Structure

```text
my-mcp-project/
│
├── dockerfiles/
│   ├── mcp_server.dockerfile
│   ├── mcp_client.dockerfile
│   └── streamlit.dockerfile
│
├── src/
│   ├── integrations/
│   │   └── github_client.py
│   │
│   ├── mcp_server/
│   │   ├── server.py
│   │   └── tools/
│   │       ├── repository_management.py
│   │       ├── commits.py
│   │       ├── pull_requests.py
│   │       ├── issue_tracking.py
│   │       └── branch_management.py
│   │
│   ├── mcp_client/
│   │   └── client.py
│   │
│   └── chat_ui/
│       └── streamlit_app.py
│
├── .env.example
├── .dockerignore
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

## Tech Stack

* **Python 3.11**
* **Model Context Protocol (MCP)**
* **FastMCP**
* **Google Gemini API**
* **FastAPI**
* **Streamlit**
* **Docker & Docker Compose**
* **uv**
* **python-dotenv**

## Environment Variables

Create a `.env` file in the project root:

```env
GITHUB_PAT=your_github_personal_access_token
GITHUB_USERNAME=your_github_username
GOOGLE_API_KEY=your_google_gemini_api_key
```


> **Never commit `.env` or expose your API keys and GitHub token.**

## Running with Docker

### 1. Clone the repository

### 2. Configure environment variables

### 3. Build and run

```bash
docker compose up --build
```

The application starts:

| Service        |   Port |
| -------------- | -----: |
| MCP Server     | `7000` |
| FastAPI Client | `8000` |
| Streamlit UI   | `8501` |

Open the assistant at:

```text
http://localhost:8501
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

### Service Communication

Inside Docker:

```text
Streamlit
    ↓
mcp-client:8000
    ↓
mcp-server:8000/mcp/
    ↓
GitHub API
```

## Example

### User

```text
List all branches in username/repository-name.
```

### Assistant

```text
main
```

The request is interpreted by Gemini, routed through MCP, and executed by the corresponding GitHub tool.

## Configuration

The Gemini model is configured in the MCP client:

```python
model="gemini-3.6-flash"
```

Docker Compose manages the application services and networking.

## Security

* Credentials are loaded through environment variables.
* `.env` is excluded from version control.
* Secrets are not hard-coded.
* GitHub token permissions should follow the principle of least privilege.

## Future Improvements

* Streaming responses
* Retry and backoff handling
* Additional GitHub MCP tools
* Health checks
* Improved logging and observability
* Enhanced error handling

## License

This project is intended as a personal learning and portfolio project.
