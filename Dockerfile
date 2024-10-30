FROM python:3.12.7-slim

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# change the working directory to the `app` directory
WORKDIR /app

# install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project

# copy the project into the image
ADD . /app

# sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-cache --compile-bytecode

# define healthcheck
HEALTHCHECK --interval=1s --timeout=1s --start-period=20s --retries=3 CMD curl -f http://0.0.0.0:8000/health || exit 1

# run the application
CMD ["/app/.venv/bin/gunicorn", "app:create_app()", "--bind", "0.0.0.0:8000"]
