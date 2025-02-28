#!/bin/bash
set -e
export API_URL=https://datainsight.health/clinsight/api
export API_KEY="12345"
# * code search
# Simple search
curl -H "X-Api-Key: $API_KEY" $API_URL/code/search?query=0LBQ4
# By words in the description
curl -H "X-Api-Key: $API_KEY" -G $API_URL/code/search?type=procedure --data-urlencode 'query=endo right knee'
# Multiple codes
curl -H "X-Api-Key: $API_KEY" -G $API_URL/code/search?type=procedure --data-urlencode 'query=0LBQ4, 0Y3F4ZZ'
# Initial code letter + description
curl -H "X-Api-Key: $API_KEY" -G $API_URL/code/search?type=procedure --data-urlencode 'query=code:j adrenalin'

# * CSV export
# All procedures
curl -H "X-Api-Key: $API_KEY" -G $API_URL/code/csv?type=procedure
# Procedures for the search query
curl -H "X-Api-Key: $API_KEY" -G $API_URL/code/csv?type=procedure --data-urlencode 'query=0LBQ4, 0Y3F4ZZ'
