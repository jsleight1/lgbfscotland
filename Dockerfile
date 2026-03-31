ARG PYVERSION
FROM python:$PYVERSION

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . .
RUN uv sync --locked --all-extras --dev

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 9003

CMD ["shiny", "run", "app.py", "--host", "0.0.0.0", "--port", "9003"]