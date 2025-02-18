import os
import re
import pandas as pd

# Regex patterns for the three groups with Unicode for dagger and plus
plus_pattern = re.compile(r'\u002B[\*]{0,3}[\w\s]+\b', re.UNICODE)  # \u002B is the Unicode for the plus sign
dagger_pattern = re.compile(r'\u2020[\*]{0,3}[\w\s]+\b', re.UNICODE)  # \u2020 is the Unicode for dagger
t_pattern = re.compile(r'\bt\*{1,3}[\w\s]+\b', re.IGNORECASE)

def find_names_in_text(text):
    """Extracts a list of names from the text file using three different regex patterns"""
    plus_matches = plus_pattern.findall(text)
    dagger_matches = dagger_pattern.findall(text)
    t_matches = t_pattern.findall(text)
    
    # Combine all matches from the three groups
    all_matches = plus_matches + dagger_matches + t_matches
    print(f"Found {len(all_matches)} matches")  # Debugging output
    return all_matches

def extract_year_from_filename(filename):
    """Extracts the year from the filename assuming the format: YEAR_Month_XXX.txt"""
    year_pattern = re.compile(r'(\d{4})')
    match = year_pattern.search(filename)
    if match:
        print(f"Extracted year {match.group(1)} from {filename}")  # Debugging output
        return match.group(1)
    print(f"Warning: Could not extract year from {filename}")  # Debugging output
    return None

def process_text_files_in_directory(directory):
    """Processes all .txt files in the given directory and returns a list of (year, name) tuples"""
    data = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                print(f"\nProcessing file: {file_path}")  # Debugging output
                
                # Extract the year from the filename
                year = extract_year_from_filename(file)
                
                if not year:
                    print(f"Skipping {file_path} due to missing year")  # Debugging output
                    continue

                # Read the text data from the file
                try:
                    with open(file_path, 'r', encoding='utf-8') as text_file:
                        text_data = text_file.read()
                except Exception as e:
                    print(f"Error reading file {file}: {e}")
                    continue
                
                # Find names that match the patterns
                names = find_names_in_text(text_data)

                if not names:
                    print(f"No matches found in {file_path}")  # Debugging output
                
                # Append names and year to the data list
                for name in names:
                    data.append((year, name))
                
    return data

def save_to_csv(data, output_file):
    """Saves the collected data to a CSV file"""
    if not data:
        print("Warning: No data to save!")  # Debugging output
    df = pd.DataFrame(data, columns=['Year', 'Name'])
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

def main():
    input_directory = '../pdf_ingest/output'  # Path to the directory containing text files
    output_file = '../output/names_by_year.csv'  # Output CSV file path
    
    # Process the text files and get the data
    data = process_text_files_in_directory(input_directory)
    
    # Save the data to a CSV file
    save_to_csv(data, output_file)

if __name__ == "__main__":
    main()