#!/bin/sh

# Stop the script if an error occurs
set -e

echo "Running prestart..."

# Run database migrations to upgrade the database schema
echo "Executing database migrations..."
alembic upgrade head

echo "Prestart complete!"
