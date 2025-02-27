import csv
from collections import defaultdict

def count_years(filename):
    year_count = defaultdict(int)
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Extract year from the first column (assumes the year is the first entry in the row)
            year = row[0].split(',')[0]
            # Ensure the year is numeric before adding it to the count
            if year.isdigit():
                year_count[year] += 1
    return year_count

def compare_counts(matching_lines_counts, names_by_year_counts):
    years = set(matching_lines_counts.keys()).union(names_by_year_counts.keys())
    
    results = []
    for year in years:
        # Only process numeric years
        if year.isdigit():
            matching_count = matching_lines_counts.get(year, 0)
            names_by_year_count = names_by_year_counts.get(year, 0)
            diff = matching_count - names_by_year_count
            results.append([year, matching_count, names_by_year_count, diff])
    
    # Sort results by year
    results.sort(key=lambda x: int(x[0]))
    return results

def write_results(results, output_filename):
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Year', 'Count in matching_lines.csv', 'Count in names_by_year.csv', 'Difference'])
        writer.writerows(results)

if __name__ == "__main__":
    matching_lines_file = 'matching_lines.csv'
    names_by_year_file = '../output/names_by_year.csv'
    output_file = 'year_comparison_sorted.csv'

    matching_lines_counts = count_years(matching_lines_file)
    names_by_year_counts = count_years(names_by_year_file)

    results = compare_counts(matching_lines_counts, names_by_year_counts)
    write_results(results, output_file)

    print(f"Comparison results saved to {output_file}")