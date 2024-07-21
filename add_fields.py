import os
import json

def add_fields_to_json(directory_path, fields_to_add):
    # Loop through each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            
            # Open and load the JSON data
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Navigate to the visas.taxes.special_regimes object and add the new fields
            if 'visas' in data:
                for visa in data['visas']:
                    if 'taxes' in visa and 'special_regimes' in visa['taxes']:
                        for regime in visa['taxes']['special_regimes']:
                            regime.update(fields_to_add)
            
            # Save the updated JSON data back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

# Directory containing the JSON files
directory_path = '/Users/erickufta/Projects/admin-wealthy-wanderers/countries/07:20:2024'

# Fields to be added
fields_to_add = {
    "apply_standard_rate_after_trigger": True,
    "apply_special_rate_after_trigger": False
}

# Call the function to add fields to JSON files
add_fields_to_json(directory_path, fields_to_add)
