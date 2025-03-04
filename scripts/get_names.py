import os
import pandas as pd
import re

def match_and_count_lines(input_dir, output_file, append=False):
    """
    Extracts lines containing:
    - 't' followed by 1-3 bullets/middle dots/* (star)
    - '†' (cross) followed by 0-3 bullets/middle dots/* (star)
    - '+' followed by 0-3 bullets/middle dots/* (star)

    Saves the matching lines and prints a count summary.
    """
    # Unicode-friendly regex for required patterns (searching anywhere in the line)
    pattern = re.compile(
        r'(?:t[\u2022\u00B7]{1,3}|[\u2020\+][\u2022\u00B7]{1,3})',
        re.UNICODE
    )

    matched_data = []
    files_processed = 0
    total_lines_processed = 0
    match_count = 0  # Counter for matched lines

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

                        # Process each line
                        for line in lines:
                            line = line.strip()
                            if not line:
                                continue

                            # Match the line containing the pattern
                            match = pattern.search(line)
                            if match:
                                matched_data.append((year, line))
                                match_count += 1

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
        matched_df.to_csv(output_file, index=False, mode=mode, header=header, encoding='utf-8')
        print(f"Matching lines {'appended to' if append else 'saved to'} {output_file}")

    # Print summary
    print("\n========= Summary =========")
    print(f"Total matching lines: {match_count}")
    print(f"Total files processed: {files_processed}")
    print(f"Total lines processed: {total_lines_processed}")
    print("===========================\n")

    # Print sample matches for verification
    if not matched_df.empty:
        print("\nSample matches (first 5):")
        for _, row in matched_df.head(5).iterrows():
            print(f"{row['Year']}: {row['Matched Line']}")

    return match_count  # Return count for further analysis

# File paths
input_dir = '../pdf_ingest/parsed_pdfs/text_files'  # Directory containing text files
output_file = 'matching_lines.csv'  # Output CSV file

# Run the function
match_count = match_and_count_lines(input_dir, output_file, append=False)

print(f"\nFound {match_count} matching lines.")