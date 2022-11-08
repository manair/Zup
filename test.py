# import requests
#
# url ="http://localhost/?q=love&categories=general&time_range=day&format=json"

import requests

url = 'https://www.python.org/images/python-logo.gif'
filename = 'images/logo.gif'
res = requests.get(url)
print(res.status_code)
with open(filename, 'wb') as out:
    out.write(res.content)