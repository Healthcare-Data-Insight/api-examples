#!/bin/bash
set -e
export API_URL=http://localhost:4080/clinsight/api
echo -- Upload multiple files and convert to JSON
# Upload multiple files and get json back as ndjson
curl -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" ${API_URL}/edi/json/upload?splitTran=true&ndjson=false
# Or as regular JSON with array of claims
curl -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" ${API_URL}/edi/json/upload?splitTran=true

echo -- Post single file
# Post content as a single file
curl -X POST -H "Content-Type: text/plain" --data-binary @../edi_files/837/prof-encounter.dat ${API_URL}/edi/json&splitTran=true

echo -- Upload multiple files and convert to CSV
# Same for CSV conversion, upload files and get CSV back
curl -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" ${API_URL}/edi/csv/upload
