#!/bin/sh

# Stop the script if an error occurs
set -e

echo "Running prestart..."

# Run database migrations to upgrade the database schema
echo "Executing database migrations..."
flask db upgrade

echo "Prestart complete!"

echo "Starting server..."
exec "$@"