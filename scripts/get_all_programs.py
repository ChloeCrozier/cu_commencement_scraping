#!/usr/bin/env python3.10
import requests
from bs4 import BeautifulSoup
import json

url = 'https://open.clemson.edu/comm_programs/'
urlDict = []

id = 1
response = requests.get(url + str(id))
while response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string if soup.title else "No title found"
    pdfLink = soup.find('a', id='alpha-pdf').get('href') if soup.find('a', id='alpha-pdf') else "No PDF found"
    print(f"Title: {title} | PDF Link: {pdfLink}")
    urlDict.append({title: pdfLink})
    id += 1
    response = requests.get(url + str(id))

json.dump(urlDict, open('graduations.json', 'w'))