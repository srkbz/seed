#!/usr/bin/env bash
set -euo pipefail

docker compose up -d --build
docker compose exec -it secrets bash
