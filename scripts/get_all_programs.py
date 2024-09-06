import requests

url = 'https://open.clemson.edu/comm_programs/'

id = 1
response = requests.get(url)
while response.status_code:
    response = requests.get(url + str(id))
    print(f"Status Code: %s, ID: %d", response.status_code, id)
    id += 1