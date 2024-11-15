import os
import re
import pandas as pd

# Define a pattern to match names starting with 't*' followed by the rest of the name
name_pattern = re.compile(r'\bt\*[\w\s]+\b')

def find_names_in_txt(file_path):
    """Reads a .txt file and returns a list of names that start with 't*'"""
    with open(file_path, 'r') as file:
        text = file.read()
    
    # Find all occurrences of names starting with t*
    names = name_pattern.findall(text)
    return names

def extract_year_from_filename(filename):
    """Extracts the year from the filename assuming the format: YEAR_Month_XXX.txt"""
    year_pattern = re.compile(r'(\d{4})')  # Matches the first 4 digits (the year)
    match = year_pattern.search(filename)
    if match:
        return match.group(1)  # Returns the year as a string
    return None

def process_files_in_directory(directory):
    """Processes all .txt files in the given directory and returns a list of (year, name) tuples"""
    data = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                
                # Extract year from filename
                year = extract_year_from_filename(file)
                
                # Extract names from the file
                names = find_names_in_txt(file_path)
                
                # Add each (year, name) pair to the data list
                for name in names:
                    data.append((year, name))
                
    return data

def save_to_csv(data, output_file):
    """Saves the collected data to a CSV file"""
    df = pd.DataFrame(data, columns=['Year', 'Name'])
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

def main():
    input_directory = '../pdf_ingest/output'  # Adjust this if the path changes
    output_file = '../data/names_by_year.csv'  # Output CSV file path
    
    # Process files and collect data
    data = process_files_in_directory(input_directory)
    
    # Save data to CSV
    save_to_csv(data, output_file)

if __name__ == "__main__":
    main()