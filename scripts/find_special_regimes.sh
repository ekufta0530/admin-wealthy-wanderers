#!/bin/bash

# Directory containing the JSON files
directory="/Users/erickufta/Projects/admin-wealthy-wanderers/countries/07:31:2024"

# Loop through all JSON files in the directory
for file in "$directory"/*.json; do
    # Check if the file has special regimes defined and is not empty
    has_special_regime=$(jq -r '.visas[]? | select(.special_regimes and .special_regimes != []) | length' "$file")
    if [ "$has_special_regime" -gt 0 ]; then
        # Extract and print the country name
        country_name=$(jq -r '.country_name' "$file")
        echo "Country with special regime: $country_name"
    fi
done
