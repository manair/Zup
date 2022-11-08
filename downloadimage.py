import requests # request img from web
import shutil # save img locally


def dwnimages(iurl):
    url = iurl

    filename = '/images/logo.gif'
    res = requests.get(url)
    print(res.status_code)
    with open(filename, 'wb') as out:
        out.write(res.content)