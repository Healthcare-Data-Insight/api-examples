#!/bin/bash
set -e
export API_URL=http://localhost:5080/api

echo -- Generate 837P EDI
curl  -H "Content-Type: application/json" --data-binary @../edi_gen/request/837p-minimal.json $API_URL/edi/gen/837

echo $'\n-- Generate 835 EDI'
curl  -H "Content-Type: application/json" --data-binary @../edi_gen/request/835-minimal.json $API_URL/edi/gen/835

echo $'\n-- Validate our request to make sure the resulting EDI will be valid'
curl  -H "Content-Type: application/json" --data-binary @../edi_gen/request/837p-minimal.json $API_URL/edi/gen/837/validate