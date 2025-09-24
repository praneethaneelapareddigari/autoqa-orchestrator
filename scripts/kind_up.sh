#!/usr/bin/env bash
set -euo pipefail
if ! command -v kind >/dev/null; then
  echo "Install kind: https://kind.sigs.k8s.io/"
  exit 1
fi
kind create cluster || true
kubectl get nodes
