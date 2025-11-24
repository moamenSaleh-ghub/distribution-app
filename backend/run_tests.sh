#!/bin/bash
# Script to run backend tests

set -e

cd "$(dirname "$0")"

echo "Installing test dependencies..."
pip install -r requirements.txt

echo ""
echo "Running tests..."
pytest -v --cov=src --cov-report=term-missing

echo ""
echo "✅ Tests completed!"

