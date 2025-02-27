import os
import pandas as pd
import re

def match_names(input_dir, output_file):
    # Refined regex patterns to match the symbols with specific requirements
    t_asterisk_pattern = re.compile(r'^[tT]\*{1,3}\s*', re.IGNORECASE)  # t* to t***
    t_bullet_pattern = re.compile(r'^[tT][\u00B7\u2022]{1,3}\s*', re.IGNORECASE)  # t• to t•••
    t_dot_pattern = re.compile(r'^[tT][\u00B7\u2022\u00B7]{1,3}\s*', re.IGNORECASE)  # t· to t···

    # Plus patterns
    plus_asterisk_pattern = re.compile(r'^[\+]\*{0,3}\s*', re.IGNORECASE)  # +* to +***
    plus_bullet_pattern = re.compile(r'^[\+][\u00B7\u2022]{0,3}\s*', re.IGNORECASE)  # +• to +•••
    plus_dot_pattern = re.compile(r'^[\+][\u00B7\u2022\u00B7]{0,3}\s*', re.IGNORECASE)  # +· to +···

    # Dagger patterns
    dagger_asterisk_pattern = re.compile(r'^[\u2020]\*{0,3}\s*', re.IGNORECASE)  # †* to †***
    dagger_bullet_pattern = re.compile(r'^[\u2020][\u00B7\u2022]{0,3}\s*', re.IGNORECASE)  # †• to †•••
    dagger_dot_pattern = re.compile(r'^[\u2020][\u00B7\u2022\u00B7]{0,3}\s*', re.IGNORECASE)  # †· to †···

    matched_data = []

    # Walk through all files in the directory
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):  # Process only text files
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                    # Process each line to check for pattern matches
                    for line in lines:
                        line = line.strip()

                        # Skip lines containing "honors"
                        if 'honors' in line.lower():
                            continue

                        # Remove excess whitespace to ensure matching (ignore extra spaces)
                        line = re.sub(r'\s+', ' ', line)

                        # Extract year from filename
                        year_match = re.match(r'(\d{4})', file)
                        if year_match:
                            year = year_match.group(1)

                            # Find all matches for the patterns in the line
                            matches = []
                            for match in re.finditer(t_asterisk_pattern, line):
                                matches.append(match.group(0))
                            for match in re.finditer(t_bullet_pattern, line):
                                matches.append(match.group(0))
                            for match in re.finditer(t_dot_pattern, line):
                                matches.append(match.group(0))

                            for match in re.finditer(plus_asterisk_pattern, line):
                                matches.append(match.group(0))
                            for match in re.finditer(plus_bullet_pattern, line):
                                matches.append(match.group(0))
                            for match in re.finditer(plus_dot_pattern, line):
                                matches.append(match.group(0))

                            for match in re.finditer(dagger_asterisk_pattern, line):
                                matches.append(match.group(0))
                            for match in re.finditer(dagger_bullet_pattern, line):
                                matches.append(match.group(0))
                            for match in re.finditer(dagger_dot_pattern, line):
                                matches.append(match.group(0))

                            # If there are multiple matches, split the line at each match
                            if matches:
                                for match in matches:
                                    start_idx = line.find(match)  # Find the match start point
                                    # Append the full line first
                                    matched_data.append((year, line.strip()))
                                    # Append the portion after the match
                                    matched_data.append((year, line[start_idx:].strip()))

    # Convert matched data to DataFrame
    matched_df = pd.DataFrame(matched_data, columns=['Year', 'Matched Line'])

    # Remove duplicate rows
    matched_df = matched_df.drop_duplicates()

    # Save to a new CSV file (output file will be overwritten if it already exists)
    if matched_df.empty:
        print("Warning: No matching lines found. Check the input format.")
    else:
        matched_df.to_csv(output_file, index=False)
        print(f"Matching lines saved to {output_file}")
    
    # Print the length of the matched data
    print(f"Total number of matching lines (after removing duplicates): {len(matched_df)}")

# File paths
input_dir = '../pdf_ingest/parsed_pdfs/text_files'  # Directory containing text files
output_file = 'matching_lines.csv'  # Output CSV file for new results

# Run the function
match_names(input_dir, output_file)