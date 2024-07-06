#!/bin/bash

echo "Alembic upgrades migrations..."
alembic upgrade head

echo "Starting Fastapi server..."
fastapi dev app/main.py --port 5000
