#!/bin/bash
set -e
cd "$(dirname "$BASH_SOURCE")/../"

docker compose run --rm --build reverse-proxy nginx -T
