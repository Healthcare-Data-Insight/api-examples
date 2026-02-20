#!/bin/bash
set -e
# Remove the container if already exists
docker rm -f ediconvert 2>/dev/null || true
docker create --name ediconvert --restart unless-stopped -p "8443:5080" -v ./etc:/app/etc:ro -e SERVER_SSL_CERTIFICATE=./etc/ssl/certificate.crt -e SERVER_SSL_CERTIFICATEPRIVATEKEY=./etc/ssl/private.key repo.datainsight.health/ediconvert:2.14
# Now run docker start -ai ediconvert
# The container listens on 8443 port