FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY src ./src

EXPOSE 9000

CMD [".venv/bin/python", "-m", "src.mcp_server.server"]

