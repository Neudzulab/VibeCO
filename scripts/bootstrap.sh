#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

log() {
  printf '\n[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$1"
}

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
else
  PYTHON=python
fi

if [ ! -d .venv ]; then
  log "Creating Python virtual environment (.venv)"
  "$PYTHON" -m venv .venv
else
  log "Using existing Python virtual environment (.venv)"
fi

# shellcheck disable=SC1091
source .venv/bin/activate

log "Upgrading pip"
pip install --upgrade pip >/dev/null

if [ -f requirements.txt ]; then
  log "Installing project dependencies"
  pip install -r requirements.txt >/dev/null
else
  log "No requirements.txt found; skipping dependency installation"
fi

if [ ! -f project.yaml ] && [ -f project.yaml.example ]; then
  log "Seeding project.yaml from project.yaml.example"
  cp project.yaml.example project.yaml
fi

if command -v make >/dev/null 2>&1 && [ -f Makefile ] && grep -q '^render:' Makefile; then
  log "Rendering PROJECT_SUMMARY.md via make render"
  make render >/dev/null
else
  log "Skipping make render (target missing or make unavailable)"
fi

log "Environment ready. Activate it anytime with: source .venv/bin/activate"
