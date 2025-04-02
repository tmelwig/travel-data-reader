#!/bin/bash

mkdir -p jsons

ssh -i ~/.ssh/ec2-decorator-rsa -t ec2-user@51.21.161.233 'cat /tmp/reco_pipe' | \
while read -r json; do
    search_id=$(echo "$json" | jq -r '.search_id')
    echo "$json" > "jsons/${search_id}.json"

    # ⚠️ Replace with your processing command:
    # python decorator_algorithm.py "jsons/${search_id}.json"

    if [ $? -ne 0 ]; then
        echo "Error processing $search_id" >&2
        break
    fi
done