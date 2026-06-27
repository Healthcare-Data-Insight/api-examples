#!/bin/bash
set -e
export API_URL=http://localhost:5080/api

echo -- EDI for a minimalilstic 837P claim
curl  -H "Content-Type: application/json" --data-binary @../edi_gen/request/837p-minimal.json $API_URL/edi/gen/claim

echo -- Validate our request to make sure the resulting EDI is valid
curl  -H "Content-Type: application/json" --data-binary @../edi_gen/request/837p-minimal.json $API_URL/edi/gen/claim/validate

# Issues