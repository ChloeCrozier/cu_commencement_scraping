import pandas as pd
import re

def clean_names(input_file, output_file):
    # Read CSV file
    df = pd.read_csv(input_file, delimiter=',', dtype=str)  # Read everything as a string

    if df.empty:
        print("Error: The CSV file appears to be empty or incorrectly formatted.")
        return

    # Normalize column names
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['Year', 'Name'])  # Drop rows with missing values

    cleaned_data = []
    
    # Unicode-based regex patterns for removal
    plus_pattern = re.compile(r'^\u002B\**\s*', re.UNICODE)  # + symbol with optional *
    dagger_pattern = re.compile(r'^\u2020\**\s*', re.UNICODE)  # † symbol with optional *
    t_pattern = re.compile(r'^t\**\s*', re.IGNORECASE)  # t with * variations

    for _, row in df.iterrows():
        year = row['Year'].strip()
        name = row['Name'].strip()

        # Remove Unicode-based prefixes
        cleaned_name = re.sub(plus_pattern, '', name)
        cleaned_name = re.sub(dagger_pattern, '', cleaned_name)
        cleaned_name = re.sub(t_pattern, '', cleaned_name)

        if not year or not cleaned_name:
            continue  # Skip rows with missing data
        
        cleaned_data.append((year, cleaned_name))
    
    # Convert cleaned data to DataFrame
    cleaned_df = pd.DataFrame(cleaned_data, columns=['Year', 'Name'])
    
    # Save to CSV
    if cleaned_df.empty:
        print("Warning: No data was processed. Check the input format.")
    else:
        cleaned_df.to_csv(output_file, index=False)
        print(f"Cleaned data saved to {output_file}")

# File paths
input_file = 'names_by_year.csv'  # Ensure this file exists
output_file = 'honors_graduates.csv'

# Run the cleaning function
clean_names(input_file, output_file)
