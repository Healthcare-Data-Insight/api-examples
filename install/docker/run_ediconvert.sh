#!/bin/bash
set -e
# Remove the container if already exists
docker rm -f ediconvert 2>/dev/null || true
# Run the container, attach to it and remove after the shutdown
docker run -it --rm --name ediconvert  -p "5080:5080" -v ./etc:/app/etc:ro repo.datainsight.health/ediconvert:2.15