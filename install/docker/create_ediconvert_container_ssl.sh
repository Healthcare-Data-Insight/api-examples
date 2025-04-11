#!/bin/bash
set -e
docker create --name ediconvert  -p "8443:5080" -v ./etc:/app/etc -e SERVER_SSL_CERTIFICATE=./etc/ssl/certificate.crt -e SERVER_SSL_CERTIFICATEPRIVATEKEY=./etc/ssl/private.key repo.datainsight.health/ediconvert:2.11