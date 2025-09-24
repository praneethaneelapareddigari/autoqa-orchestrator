#!/usr/bin/env bash
set -euo pipefail
kubectl apply -f infra/k8s/namespace.yaml
kubectl apply -f infra/k8s/selenium-grid.yaml
kubectl apply -f infra/k8s/orchestrator-deploy.yaml
kubectl apply -f infra/k8s/orchestrator-svc.yaml
kubectl apply -f infra/k8s/grafana-deploy.yaml
kubectl apply -f infra/k8s/jenkins-deploy.yaml
kubectl -n autoqa get pods -o wide
