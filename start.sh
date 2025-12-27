#!/bin/bash
# Start the orchid detection service

export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "Starting Orchid Detection Service..."
python -m app.main
