#!/bin/sh

# Stop the script if an error occurs
set -e

echo "Running prestart..."

echo "Downloading JWKS..."
if [ -n "${QUARK_JWKS}" ]; then
    wget ${QUARK_JWKS} -O jwks.json
    echo "JWKS downloaded!"
else
    echo "Skipping JWKS, URL not set."
fi

# Run database migrations to upgrade the database schema
echo "Executing database migrations..."
alembic upgrade head

echo "Prestart complete!"
