import os
import json

def update_special_regimes(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {file_path}")  # Debug statement
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # Check if 'visas' exists
                if 'visas' in data:
                    for visa in data['visas']:
                        # Check if 'special_regimes' exists and is not empty
                        if 'special_regimes' in visa:
                            if visa['special_regimes']:
                                print(f"Found special regimes in {filename}")  # Debug statement
                                for special_regime in visa['special_regimes']:
                                    # Add the new fields if not already present
                                    if 'special_regime_auto_trigger' not in special_regime:
                                        special_regime['special_regime_auto_trigger'] = True  # Default value
                                        print(f"Added special_regime_auto_trigger to {filename}")  # Debug statement
                                    if 'special_regime_application_trigger' not in special_regime:
                                        special_regime['special_regime_application_trigger'] = False  # Default value
                                        print(f"Added special_regime_application_trigger to {filename}")  # Debug statement
                            else:
                                print(f"No special regimes in {filename}")  # Debug statement
                        else:
                            print(f"'special_regimes' field not found in {filename}")  # Debug statement
                else:
                    print(f"'visas' field not found in {filename}")  # Debug statement

                # Save the updated data back to the file
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                print(f"Finished processing file: {file_path}")  # Debug statement

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {file_path}: {e}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# Set the directory containing the JSON files
directory = '/Users/erickufta/Projects/admin-wealthy-wanderers/countries/07:31:2024'
update_special_regimes(directory)
