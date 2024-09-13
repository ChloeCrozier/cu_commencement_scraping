#!/usr/bin/env python3.10
import requests
from bs4 import BeautifulSoup
import json

def getMonth(month):
    switcher = {
        "1": "January",
        "2": "February",
        "3": "March",
        "4": "April",
        "5": "May",
        "6": "June",
        "7": "July",
        "8": "August",
        "9": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }
    if(month.split(" ")[0] == "Summer"):
        return "August"
    elif(month.split(" ")[0] == "Winter"):
        return "December"
    elif(month.split(" ")[0] == "Spring"):
        return "May"
    else:
        return switcher.get(month, month.split(" ")[0])

url = 'https://open.clemson.edu/comm_programs/'
urlDict = {}

id = 1
response = requests.get(url + str(id))

while response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    publicationHeader = soup.find('h2', class_='field-heading', text='Publication Date')
    date = publicationHeader.find_next_sibling('p').text.split("-")
    month = getMonth(date[0])
    year = date[-1]
    pdfLink = soup.find('a', id='alpha-pdf').get('href') if soup.find('a', id='alpha-pdf') else "No PDF found"

    if year not in urlDict:
        urlDict[year] = {month: [pdfLink]}
    else:
        if month in urlDict[year]:
            count = len(urlDict[year][month]) + 1
            month_key = f"{month}_{count}"
            urlDict[year][month_key] = [pdfLink]
        else:
            urlDict[year][month] = [pdfLink]

    print(f"Scrape ID: {id} \t {year} {month} graduation @ {pdfLink}")

    id += 1
    response = requests.get(url + str(id))

json.dump(urlDict, open('data/graduations.json', 'w'))
print("Successfully saved data to data/graduations.json")