#!/bin/bash
set -e
export API_URL=https://datainsight.health/clinsight/api

# * code search
# Simple search
curl $API_URL/code/search?query=0LBQ4
# By words in the description
curl -G $API_URL/code/search?type=procedure --data-urlencode 'query=endo right knee'
# Multiple codes
curl -G $API_URL/code/search?type=procedure --data-urlencode 'query=0LBQ4, 0Y3F4ZZ'
# Initial code letter + description
curl -G $API_URL/code/search?type=procedure --data-urlencode 'query=code:j adrenalin'

# * CSV export
# All procedures
curl -G $API_URL/code/csv?type=procedure
# Procedures for the search query
curl -G $API_URL/code/csv?type=procedure --data-urlencode 'query=0LBQ4, 0Y3F4ZZ'
