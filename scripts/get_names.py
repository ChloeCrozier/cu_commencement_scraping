import os
import pandas as pd
import re

def match_names(input_dir, output_file, append=False):
    # Define regex pattern that matches lines starting with t, †, or + followed by symbols
    # This will match the start of the line (^) followed by one of the symbols
    start_pattern = re.compile(r'^([tT][\*\u00B7\u2022\.\-]{1,3}|[\u2020][\*\u00B7\u2022\.\-]{0,2}|[\+][\*\u00B7\u2022\.\-]{0,3})\s*', re.IGNORECASE)
    
    # Pattern to find additional t, †, or + symbols within lines (not at the start)
    continuation_pattern = re.compile(r'([tT][\*\u00B7\u2022\.\-]{1,3}|[\u2020][\*\u00B7\u2022\.\-]{0,2}|[\+][\*\u00B7\u2022\.\-]{0,3})\s*')

    matched_data = []
    files_processed = 0
    total_lines_processed = 0

    # Walk through all files in the directory
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):  # Process only text files
                files_processed += 1
                file_path = os.path.join(root, file)
                
                # Extract year from filename
                year_match = re.search(r'(\d{4})', file)
                year = year_match.group(1) if year_match else "Unknown"
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                        lines = content.splitlines()
                        total_lines_processed += len(lines)

                        # Process each line to check for pattern matches
                        for line in lines:
                            line = line.strip()
                            
                            # Skip empty lines
                            if not line:
                                continue

                            # Only process lines that START with one of our patterns
                            start_match = start_pattern.match(line)
                            if start_match:
                                # Add the full line first
                                matched_data.append((year, line))
                                
                                # Find any additional patterns within the line (after the first one)
                                all_matches = list(continuation_pattern.finditer(line))
                                
                                # Skip the first match (which is the same as start_match)
                                # and add entries for each subsequent match
                                for match in all_matches[1:] if len(all_matches) > 1 else []:
                                    start_idx = match.start()
                                    matched_data.append((year, line[start_idx:]))
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    # Convert matched data to DataFrame
    matched_df = pd.DataFrame(matched_data, columns=['Year', 'Matched Line'])

    # Remove duplicate rows
    matched_df = matched_df.drop_duplicates()

    # Save to CSV file
    mode = 'a' if append else 'w'
    header = not append
    
    if matched_df.empty:
        print("Warning: No matching lines found. Check the input format.")
    else:
        matched_df.to_csv(output_file, index=False, mode=mode, header=header)
        print(f"Matching lines {'appended to' if append else 'saved to'} {output_file}")
    
    # Print the length of the matched data
    print(f"Total number of matching lines (after removing duplicates): {len(matched_df)}")
    print(f"Files processed: {files_processed}")
    print(f"Total lines processed: {total_lines_processed}")

    # Print samples of matched lines to help verify pattern matching
    if not matched_df.empty:
        print("\nSample matches (first 5):")
        for _, row in matched_df.head(5).iterrows():
            print(f"{row['Year']}: {row['Matched Line']}")

# File paths
input_dir = '../pdf_ingest/parsed_pdfs/text_files'  # Directory containing text files
output_file = 'matching_lines.csv'  # Output CSV file

# Run the function
match_names(input_dir, output_file, append=False)