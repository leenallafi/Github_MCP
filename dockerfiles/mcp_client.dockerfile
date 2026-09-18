FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY src ./src

EXPOSE 8000

CMD [".venv/bin/uvicorn", "src.mcp_client.client:app", "--host", "0.0.0.0", "--port", "8000"]