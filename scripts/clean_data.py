input_file = "matching_lines.csv"
output_file = input_file  # Overwrite the original file

# Read the file and remove duplicate lines
with open(input_file, 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

# Remove duplicate lines while preserving order
seen = set()
unique_lines = []
for line in lines:
    if line not in seen:
        unique_lines.append(line)
        seen.add(line)

# Write the unique lines to the output file
with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.writelines(unique_lines)

print(f"Duplicates removed. Cleaned file saved as {output_file}")
print(f"Original lines: {len(lines)}, Cleaned lines: {len(unique_lines)}")