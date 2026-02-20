#!/bin/bash
set -e
# Remove the container if already exists
docker rm -f ediconvert 2>/dev/null || true
docker create --name ediconvert  --restart unless-stopped -p "5080:5080" -v ./etc:/app/etc:ro repo.datainsight.health/ediconvert:2.14
# Now run docker start -ai ediconvert