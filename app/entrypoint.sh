#!/bin/bash
set -e

echo "Waiting for Postgres..."
while ! pg_isready -h db -p 5432 -U devuser > /dev/null 2>&1; do
  sleep 1
done
echo "Postgres is ready!"

# รัน migrations
echo "Running migrations..."
alembic upgrade head

# รัน seeder
echo "Running seeder..."
python app/seeders/run_seed.py

# รัน uvicorn
echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
