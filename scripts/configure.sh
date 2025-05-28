#!/bin/bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONF_SRC_DIR="$PROJECT_ROOT/var/conf/weightr-frontend"
CONF_DEST_DIR="$HOME/Data/var/conf/weightr-frontend"
ENV_TEMPLATE="$CONF_SRC_DIR/.env.dev.template"
ENV_FINAL="$CONF_DEST_DIR/.env.dev"
ENV_DOCKER_TEMPLATE="$CONF_SRC_DIR/.env.dev.docker.template"
ENV_DOCKER_FINAL="$CONF_DEST_DIR/.env.dev.docker"
VENV_DIR="$PROJECT_ROOT/.venv"

# Ensure CONF_DEST_DIR exists
mkdir -p "$CONF_DEST_DIR"

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

echo "Copying environment template..."
cp "$ENV_TEMPLATE" "$ENV_FINAL"
cp "$ENV_DOCKER_TEMPLATE" "$ENV_DOCKER_FINAL"
