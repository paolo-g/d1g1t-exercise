# syntax=docker/dockerfile:1

# Build python/django backend container
FROM python:3-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG ENV_NAME

# Get bash to run the entrypoint script, which tries to talk to postgres
RUN set -ex; \
    apk update; \
    apk add bash gcc musl-dev postgresql-dev

# Setup python dependencies
WORKDIR /backend
COPY . /backend
RUN pip install -r requirements.${ENV_NAME}.txt
COPY . /backend

# Static code analysis
RUN pylint --load-plugins pylint_django --django-settings-module=backend.settings /backend/api

# Entrypoint to wait for DB
RUN chmod +x /backend/entrypoint.sh
# Wrap the entrypoint script in exec
ENTRYPOINT ["/backend/entrypoint.sh"]
