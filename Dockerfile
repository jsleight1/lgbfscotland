ARG PYVERSION
FROM python:$PYVERSION

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . .
RUN uv sync --locked --all-extras --dev

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["shiny", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]