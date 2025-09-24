#!/usr/bin/env bash
set -euo pipefail
# Orchestrator local run
python orchestrator/app.py &
ORCH_PID=$!
echo "Orchestrator PID: $ORCH_PID"
# Cypress
pushd cypress >/dev/null
npm ci
npx cypress run --browser chrome || true
popd >/dev/null
# Selenium
pushd selenium >/dev/null
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q || true
deactivate
popd >/dev/null
kill $ORCH_PID || true
