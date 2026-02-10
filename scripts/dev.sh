#!/usr/bin/env bash
set -e

echo "Starting database..."
docker compose up -d

echo "Starting backend..."
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload &
BACKEND_PID=$!

echo "Starting frontend..."
cd ../frontend
npm run dev

kill $BACKEND_PID
