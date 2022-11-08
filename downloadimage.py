import requests # request img from web
import shutil # save img locally


def dwnimages(iurl):
    url = iurl

    res = requests.get(url, stream=True)
    imglocal =res.request.path_url

    if res.status_code == 200:
        with open(imglocal, 'wb') as f:
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ')
        #return 'Dowloded'
    # else:
    #     print('Image Couldn\'t be retrieved')