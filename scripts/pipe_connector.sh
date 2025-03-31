#!/bin/bash

mkdir -p jsons  # Create output dir

# Read FIFO, extract each JSON safely
ssh -i ~/.ssh/ec2-tmelwig-rsa -t ec2-user@51.21.161.233 'cat /tmp/reco_pipe' | \
while read -r json; do
    # Parse search_id and save JSON
    search_id=$(echo "$json" | jq -r '.search_id')
    echo "$json" > "jsons/${search_id}.json"

    # Run computation (replace with your command)
    # python process.py "jsons/${search_id}.json"

    # Exit on error (optional)
    if [ $? -ne 0 ]; then
        echo "Error processing $search_id" >&2
        break
    fi
done

