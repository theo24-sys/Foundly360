#!/bin/sh
set -eu

python manage.py migrate

if [ -n "${FOUNDRY_ADMIN_USERNAME:-}" ] || [ -n "${FOUNDRY_ADMIN_EMAIL:-}" ] || [ -n "${FOUNDRY_ADMIN_PASSWORD:-}" ]; then
  if [ -z "${FOUNDRY_ADMIN_USERNAME:-}" ] || [ -z "${FOUNDRY_ADMIN_EMAIL:-}" ] || [ -z "${FOUNDRY_ADMIN_PASSWORD:-}" ]; then
    echo "Admin bootstrap requires FOUNDRY_ADMIN_USERNAME, FOUNDRY_ADMIN_EMAIL, and FOUNDRY_ADMIN_PASSWORD."
    exit 1
  fi
  python manage.py create_platform_admin
fi

exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8000}" --workers "${WEB_CONCURRENCY:-2}" --access-logfile -
