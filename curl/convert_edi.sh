#!/bin/bash
set -e
export API_URL=http://localhost:5080/api

# get the app version and the license info
curl $API_URL/about
echo
echo -- Upload multiple files, validate and convert to JSON
# Upload multiple files and get json back as ndjson
curl -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" "$API_URL/edi/json?ndjson=true&validate=true" > 837p.ndjson
# Or as regular JSON with array of claims
curl -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" "$API_URL/edi/json?validate=true" > 837p.json

echo -- Post single file
# Post content of 837 as a single file
curl -H "Content-Type: text/plain" --data-binary @../edi_files/837/prof-encounter.dat "$API_URL/edi/json?ediFileName=prof-encounter.dat&validate=true"

# Post content of 835 as a single file
curl -H "Content-Type: text/plain" --data-binary @../edi_files/835/835-all-fields.dat "$API_URL/edi/json?ediFileName=835-all-fields.dat&validate=true" > 835.json

echo -- Upload multiple files and convert to CSV
# Same for CSV conversion, upload files and get CSV back
curl -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" "$API_URL/edi/csv" > 837p.csv
curl -H "Content-Type: text/plain" --data-binary @../edi_files/837/prof-encounter.dat "$API_URL/edi/csv?ediFileName=prof-encounter.dat"

# Convert 277
curl -H "Content-Type: text/plain" --data-binary @../edi_files/277/277CA-all-fields.edi "$API_URL/edi/json?validate=true" > 277ca.json

echo -- Validate EDI files
# Validate various EDI files
curl -H "Content-Type: text/plain" --data-binary @../edi_files/835/835-validation-issues.edi "$API_URL/edi/validate"
curl -H "Content-Type: text/plain" --data-binary @../edi_files/837/837P-validation-issues.edi "$API_URL/edi/validate"
# Validate to EDI text
curl -H "Content-Type: text/plain" --data-binary @../edi_files/837/837P-validation-issues.edi "$API_URL/edi/validate/text"

# NCPDP
echo -- Parse NCPDP telco b1 file
curl -H "Content-Type: text/plain" --data-binary @../edi_files/ncpdp/b1_telco.dat "$API_URL/ncpdp/parse"

# Validate using public API
echo $'\n-- Validate EDI files using public API'
# Your license key can be used as the API key, request your license key at https://datainsight.health/products/edi-license/
export API_KEY="Ic5OXgAAABoAAAACAAAACwAAAANlbnRpdGxlbWVudEVESQAAABoAAAALAAAACmV4cGlyYXRpb24AAAGdIyY2AAAAAJwAAAABAAAAEAAAAIBsaWNlbnNlU2lnbmF0dXJlNNiFGndeVeM9X4kxO9SFf7U0Gq7K9LLKEKPEhW5TTqZvFEB2QyKb1A7/8BjddgIZUAnNxRSykCMj6u34YlBeibVwkHqyg2p31qHRwYGtVO4O6YTEsveZ15gH5yOS1vZI6ztxI7MWsOXn7bupiezerY4/0MLMHuWqC6V1+kQVVLQAAAAiAAAAAgAAAA8AAAAHc2lnbmF0dXJlRGlnZXN0U0hBLTUxMg=="
curl -H "Content-Type: text/plain" -H "X-Api-Key: $API_KEY" --data-binary @../edi_files/837/837P-validation-issues.edi "https://datainsight.health/clinsight/api/edi/validate"