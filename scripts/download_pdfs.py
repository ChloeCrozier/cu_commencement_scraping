import os
import json
import requests

# Define paths
json_path = "../data/graduations.json"
output_dir = "../pdf_ingest/output"

# Load the JSON data
try:
    with open(json_path, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("JSON file not found at {}".format(json_path))
    exit(1)
except json.JSONDecodeError as e:
    print("Error decoding JSON: {}".format(e))
    exit(1)

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Download PDFs
for year, months in data.items():
    for month, urls in months.items():
        for url in urls:
            # Create a unique filename
            filename = "{}_{}_{}.pdf".format(year, month, url.split('=')[1].split('&')[0])
            output_path = os.path.join(output_dir, filename)
            try:
                # Download the file
                response = requests.get(url, stream=True)
                response.raise_for_status()
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print("Downloaded: {}".format(output_path))
            except requests.exceptions.RequestException as e:
                print("Failed to download {}: {}".format(url, e))