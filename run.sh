#!/usr/bin/env bash
query=$1
echo "query:$query"
curl -G http://127.0.0.1:80 --data-urlencode=$query
