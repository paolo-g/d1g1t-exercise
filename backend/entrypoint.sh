#!/bin/sh
set -e

# Wait for the DB to be up
until python entrypoint.py $POSTGRES_HOST $POSTGRES_NAME $POSTGRES_USER $POSTGRES_PASSWORD; do
  >&2 echo "DB container $POSTGRES_HOST named $POSTGRES_NAME is unavailable; sleeping for now."
  sleep 5
done

>&2 echo "DB is up; starting up API."

exec "$@"
