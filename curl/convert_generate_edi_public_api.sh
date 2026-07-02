#!/bin/bash
set -e
export API_URL=https://datainsight.health/clinsight/api
# Your license key is the API key, request your license key at https://datainsight.health/products/edi-license/
export API_KEY="Ic5OXgAAABoAAAACAAAACwAAAANlbnRpdGxlbWVudEVESQAAABoAAAALAAAACmV4cGlyYXRpb24AAAGfY+52AAAAAJwAAAABAAAAEAAAAIBsaWNlbnNlU2lnbmF0dXJlOsneSdogzSNep090TKIoVq2WqvdnaIZOoO3z21OJ3k28F+YoLVYy8xBzyUe7LU6zjqnJCc1DLhsB+RGkyJxUwhLkt9JCYvxZcIWKJ1QPxck643NB4b4zJm9NPlflkczqrb2kEGgoZ9NdXCsKgeb5S0tOdquTEIkJsvFQhdiXMeIAAAAiAAAAAgAAAA8AAAAHc2lnbmF0dXJlRGlnZXN0U0hBLTUxMg=="


echo -- Convert an EDI file
# Simple post
curl -H "Content-Type: text/plain" -H "X-Api-Key: $API_KEY" --data-binary @../edi_files/837/837P-minimal.dat "$API_URL/edi/json"
curl -H "Content-Type: text/plain" -H "X-Api-Key: $API_KEY" --data-binary @../edi_files/835/835-minimal.dat "$API_URL/edi/json"

# Multipart request with multiple files; convert to NDJSON
curl -H "X-Api-Key: $API_KEY" -F files=@"../edi_files/837/837P-minimal.dat" -F files=@"../edi_files/835/835-minimal.dat" "$API_URL/edi/json?ndjson=true"

echo $'\n-- Validate EDI files'
curl -H "Content-Type: text/plain" -H "X-Api-Key: $API_KEY" --data-binary @../edi_files/837/837P-validation-issues.edi "$API_URL/edi/validate"
curl -H "Content-Type: text/plain" -H "X-Api-Key: $API_KEY" --data-binary @../edi_files/837/837P-validation-issues.edi "$API_URL/edi/validate/text"

echo $'\n-- Generate 837P EDI'
curl  -H "Content-Type: application/json" -H "X-Api-Key: $API_KEY" --data-binary @../edi_gen/request/837p-minimal.json $API_URL/edi/gen/837

echo $'\n-- Generate 835 EDI'
curl  -H "Content-Type: application/json" -H "X-Api-Key: $API_KEY" --data-binary @../edi_gen/request/835-minimal.json $API_URL/edi/gen/835