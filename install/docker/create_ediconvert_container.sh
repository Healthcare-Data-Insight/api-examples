#!/bin/bash
set -e
docker create --name ediconvert  -p "5080:5080" -v ./etc:/app/etc repo.datainsight.health/ediconvert:2.14