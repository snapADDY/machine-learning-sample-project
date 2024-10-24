FROM python:3.12.7-slim as base
WORKDIR /opt/application

RUN useradd --system wsgi \
  && apt-get update \
  && apt-get --yes install --no-install-recommends curl libgomp1 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists \
  && pip install poetry

# create virtual environment (to keep things clean with poetry etc.)
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# copy appilcation file for gunicorn
COPY application.py ./

# copy pyproject.toml and lockfile
COPY pyproject.toml poetry.lock ./

# copy package
COPY package ./package

# install only prod dependencies
RUN poetry install --no-dev

USER wsgi

# expose port 8000 for external use
EXPOSE 8000

# define healthcheck
HEALTHCHECK --interval=1s --timeout=1s --start-period=20s --retries=3 CMD curl -f localhost:8000/health || exit 1

# run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "application"]
