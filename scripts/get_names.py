import os
import re
import json
import pandas as pd

# Updated regex pattern to find names starting with 't*' or '†*'
name_pattern = re.compile(r'\b(?:t\*|†\*)[\w\s]+\b', re.IGNORECASE)

def find_names_in_json(json_data):
    """Extracts a list of names that start with 't*' or '†*' from a list of JSON objects"""
    names = []
    
    for entry in json_data:
        text = entry.get("text", "")
        names.extend(name_pattern.findall(text))
    
    return names

def extract_year_from_filename(filename):
    """Extracts the year from the filename assuming the format: YEAR_Month_XXX.json"""
    year_pattern = re.compile(r'(\d{4})')
    match = year_pattern.search(filename)
    if match:
        return match.group(1)
    return None

def process_json_files_in_directory(directory):
    """Processes all .json files in the given directory and returns a list of (year, name) tuples"""
    data = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                
                # Extract the year from the filename
                year = extract_year_from_filename(file)
                
                # Read the JSON data from the file
                try:
                    with open(file_path, 'r') as json_file:
                        json_data = json.load(json_file)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {file}: {e}")
                    continue
                
                # Find names that match the pattern
                names = find_names_in_json(json_data)
                
                # Append names and year to the data list
                for name in names:
                    data.append((year, name))
                
    return data

def save_to_csv(data, output_file):
    """Saves the collected data to a CSV file"""
    df = pd.DataFrame(data, columns=['Year', 'Name'])
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

def main():
    input_directory = '../pdf_ingest/output'  # Path to the directory containing JSON files
    output_file = '../output/names_by_year.csv'  # Output CSV file path
    
    # Process the JSON files and get the data
    data = process_json_files_in_directory(input_directory)
    
    # Save the data to a CSV file
    save_to_csv(data, output_file)

if __name__ == "__main__":
    main()
