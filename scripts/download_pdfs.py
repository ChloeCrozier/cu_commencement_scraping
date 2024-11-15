import os
import json
import requests

json_path = "../data/graduations.json"
output_dir = "../pdf_ingest/output"

try:
    with open(json_path, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("JSON file not found at {}".format(json_path))
    exit(1)
except json.JSONDecodeError as e:
    print("Error decoding JSON: {}".format(e))
    exit(1)

os.makedirs(output_dir, exist_ok=True)

for year, months in data.items():
    if int(year) >= 2005:
        for month, urls in months.items():
            for url in urls:
                filename = "{}_{}_{}.pdf".format(year, month, url.split('=')[1].split('&')[0])
                output_path = os.path.join(output_dir, filename)
                try:
                    response = requests.get(url, stream=True)
                    response.raise_for_status()
                    with open(output_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print("Downloaded: {}".format(output_path))
                except requests.exceptions.RequestException as e:
                    print("Failed to download {}: {}".format(url, e))
    else:
        print(f"Skipping year {year} (before 2005)")