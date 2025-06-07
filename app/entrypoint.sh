#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

if [ "$FLASK_ENV" = "development" ]; then
  echo "Running in development mode"
  # Apply migrations
  flask db upgrade
  # Run the application in development mode
  flask run --host=0.0.0.0 --port=8000
else
  echo "Running in production mode"
  # Apply migrations
  flask db upgrade
  # Run with gunicorn for production
  gunicorn --bind 0.0.0.0:8000 "run:app" --workers 4 --timeout 120
fi