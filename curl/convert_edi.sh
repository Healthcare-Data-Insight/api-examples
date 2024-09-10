#!/bin/bash
set -e
export API_URL=http://localhost:5080/clinsight/api

# Upload multiple files and get json back as ndjson
curl -X POST -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" ${API_URL}/edi/json/upload?splitTran=true&ndjson=false
# Or as regular JSON with array of claims
curl -X POST -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" ${API_URL}/edi/json/upload?splitTran=true

# Upload multiple files and get CSV back
curl -X POST -F files=@"../edi_files/837/prof-encounter.dat" -F files=@"../edi_files/837/anesthesia.dat" ${API_URL}/edi/csv/upload
