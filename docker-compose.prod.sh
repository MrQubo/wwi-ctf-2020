#!/usr/bin/env bash

declare -r SOURCE_DIR="$(dirname -- "$BASH_SOURCE")"


cd -- "$SOURCE_DIR"

exec docker-compose -f docker-compose.yml -f docker-compose.prod.yml "$@"
