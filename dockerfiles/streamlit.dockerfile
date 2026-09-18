FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY src ./src

EXPOSE 8501

CMD [".venv/bin/streamlit", "run", "src/chat_ui/streamlit_app.py"]
