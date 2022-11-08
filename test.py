# import requests
#
# url ="http://localhost/?q=love&categories=general&time_range=day&format=json"
#
# results = requests.get(url)
# jresult = results.json()
#
# print(jresult["results"])

import requests
from requests.exceptions import HTTPError

url ="https://searx.thegpm.org/?q=love&categories=general&format=json"

try:
    response = requests.get(url)
    #response.raise_for_status()
    # access JSOn content
    #response = open("data/data.json")
    jsonResponse = response.json()
    #print("Entire JSON response")
    print(jsonResponse)

except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')