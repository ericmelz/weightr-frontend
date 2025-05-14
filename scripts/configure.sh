#!/bin/bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"

# Install uv if missing
if ! command -v uv &>/dev/null; then
  echo "uv not found.  Installing uv via pip..."
  python3 -m pip install --upgrade pip
  python3 -m pip install uv
fi

# Create virtual environment
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  uv venv
fi

# Install dependencies
echo "Installing dependencies..."
uv pip install -e ".[dev]"