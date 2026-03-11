#!/bin/bash

# Change directory to the script's directory
cd "$(dirname "$0")"

# Build and start the container
docker-compose up -d --build

# Attach to the sandbox
docker exec -it dcai_sandbox /bin/bash
