#!/bin/bash
set -e
export API_URL=http://localhost:5080/api

# get the app version and the license info
curl $API_URL/about

echo -- Upload multiple files and convert to JSON
# Upload multiple files and get json back as ndjson
curl -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" "$API_URL/edi/json?splitTran=true&ndjson=true"
# Or as regular JSON with array of claims
curl -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" "$API_URL/edi/json?splitTran=true"

echo -- Post single file
# Post content of 837 as a single file
curl -H "Content-Type: text/plain" --data-binary @../edi_files/837/prof-encounter.dat "$API_URL/edi/json?splitTran=true&ediFileName=prof-encounter.dat"

# Post content of 835 as a single file
curl -H "Content-Type: text/plain" --data-binary @../edi_files/835/negotiated_discount.dat "$API_URL/edi/json?splitTran=true&ediFileName=negotiated_discount.dat"

echo -- Upload multiple files and convert to CSV
# Same for CSV conversion, upload files and get CSV back. splitTran=true is the default for CSV, no need to provide it
curl -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" "$API_URL/edi/csv"
curl -H "Content-Type: text/plain" --data-binary @../edi_files/837/prof-encounter.dat "$API_URL/edi/csv?ediFileName=prof-encounter.dat"

# Convert 277
curl -H "Content-Type: text/plain" --data-binary @../edi_files/277/277CA-all-fields.edi "$API_URL/edi/json"

# NCPDP
echo -- Parse NCPDP telco b1 file
curl -H "Content-Type: text/plain" --data-binary @../edi_files/ncpdp/b1_telco.dat "$API_URL/ncpdp/parse"

