#!/bin/bash
set -e
export API_URL=http://localhost:5080/api

# get the app version and the license info
curl $API_URL/about
echo
echo -- Post single file
curl -H "Content-Type: text/plain" --data-binary @../edi_files/837/837P-minimal.dat "$API_URL/edi/json"

echo $'\n-- Upload multiple files, validate and convert to JSON'
# Upload multiple files and get json back as ndjson
curl -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" "$API_URL/edi/json?ndjson=true&validate=true" > 837p.ndjson
# Or as regular JSON with array of claims
curl -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" "$API_URL/edi/json?validate=true" > 837p.json

# Post content of 835 as a single file
curl -H "Content-Type: text/plain" --data-binary @../edi_files/835/835-all-fields.dat "$API_URL/edi/json?ediFileName=835-all-fields.dat&validate=true" > 835.json

echo $'\n-- Upload multiple files and convert to CSV'
curl -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" "$API_URL/edi/csv" > 837p.csv
echo
curl -H "Content-Type: text/plain" --data-binary @../edi_files/837/prof-encounter.dat "$API_URL/edi/csv?ediFileName=prof-encounter.dat"

echo $'\n-- Convert 277'
curl -H "Content-Type: text/plain" --data-binary @../edi_files/277/277CA-all-fields.edi "$API_URL/edi/json?validate=true" > 277ca.json

echo  $'\n-- Validate EDI files without conversion'
# Validate various EDI files
curl -H "Content-Type: text/plain" --data-binary @../edi_files/835/835-validation-issues.edi "$API_URL/edi/validate"
echo
curl -H "Content-Type: text/plain" --data-binary @../edi_files/837/837P-validation-issues.edi "$API_URL/edi/validate"
echo
# Validate to EDI text
curl -H "Content-Type: text/plain" --data-binary @../edi_files/837/837P-validation-issues.edi "$API_URL/edi/validate/text"

# NCPDP
echo  $'\n-- Parse NCPDP telco b1 file'
curl -H "Content-Type: text/plain" --data-binary @../edi_files/ncpdp/b1_telco.dat "$API_URL/ncpdp/parse"