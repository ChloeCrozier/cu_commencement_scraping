#!/usr/bin/env python3.10
import requests

url = 'https://open.clemson.edu/comm_programs/'
validUrls = []

id = 1
response = requests.get(url + str(id))
while response.status_code == 200:
    print(f"status code: {response.status_code} for id: {id}")
    validUrls.append(url + str(id))
    id += 1
    response = requests.get(url + str(id))