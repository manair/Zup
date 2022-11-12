import copy
import os
import requests
import time
import config
import downloadimage as dw


# if not os.path.exists("keywords"):
#    os.mkdir("keywords")
from localdata.DBConn import myConn


def addDBurlToList(dbTuple):
    db_urls = [item for t in dbTuple for item in t]

    return db_urls


#
# Check if the URL is new.
#
def check_urls(keyword, urls, category):
    new_urls = []
    new_results = {}
    new_results['searx'] = {}
    cdTime = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
    chkUrl = 'select url from search_result where kword ="' + keyword + '";'
    #print(chkUrl)
    saveUrl = myConn(chkUrl)
    urlDB = addDBurlToList(saveUrl)

    i = 0
    if len(urlDB) == 0 and category == 'general':
        for result in urls['results']:
            reUrl = result['url']
            reScore = result['score']
            reCatego = result['category']
            reEngin = result['engines'][0]
            reTitle = result['title']
            #reContent = result['content']
            reContent = ''
            new_results['searx'][keyword] = result
            i = i + 1

            #insSQl = 'insert into search_result(url, kword, udate, score, category, engines, title, content) values("' + reUrl + '","' + keyword + '","' + cdTime + '",' + str(reScore) + ',"' + reCatego + '","' + reEngin + '","' + reTitle + '","' + reContent + '");'
            insSQl = 'insert into search_result(url, kword, udate, score, category, engines, title, content) values("' + reUrl + '","' + keyword + '","' + cdTime + '",' + str(reScore) + ',"' + reCatego + '","' + reEngin + '","' + reTitle + '","' + reContent + '");'
#insSQl = 'insert into search_result(url, kword, udate, score, category, engines, title, content) values(?,?,?,?,?,?,?,?)',(reUrl, keyword, cdTime , reScore , reCatego , reEngin , reTitle, reContent)

            print(insSQl)
            # this is just to pass the new url around
            new_urls.append(reUrl)
            myConn(insSQl)

    if len(urlDB) == 0  and category == 'images':
            for result in urls['results']:
                reUrl = result['img_src']
                reScore = result['score']
                reCatego = result['category']
                reEngin = result['engines'][0]
                reTitle = result['title']
                # reContent = result['content']
                reContent = ''
                new_results['searx'][keyword] = result
                i = i + 1

                # insSQl = 'insert into search_result(url, kword, udate, score, category, engines, title, content) values("' + reUrl + '","' + keyword + '","' + cdTime + '",' + str(reScore) + ',"' + reCatego + '","' + reEngin + '","' + reTitle + '","' + reContent + '");'
                insSQl = 'insert into search_result(url, kword, udate, score, category, engines, title, content) values("' + reUrl + '","' + keyword + '","' + cdTime + '",' + str(
                    reScore) + ',"' + reCatego + '","' + reEngin + '","' + reTitle + '","' + reContent + '");'
                # insSQl = 'insert into search_result(url, kword, udate, score, category, engines, title, content) values(?,?,?,?,?,?,?,?)',(reUrl, keyword, cdTime , reScore , reCatego , reEngin , reTitle, reContent)

                # print(insSQl)
                # download image localy

                dw.dwnimages(reUrl)

                new_urls.append(reUrl)
                myConn(insSQl)

    else:
        for result in urls['results']:
            reUrl = result['url']
            reScore = result['score']
            reCatego = result['category']
            reEngin = result['engines'][0]
            reTitle = result['title']
            #reContent = result['content']
            reContent = ''
            if reUrl in urlDB:
                print("[*] Old URL for %s discovered: %s" % (keyword, reUrl))

            else:
                print("[*] New URL for %s discovered: %s" % (keyword, reUrl))
                #insSQl = 'insert into search_result(url, kword, udate, score, category, engines, title, content) values("' + reUrl + '","' + keyword + '","' + cdTime + '",' + reScore + ',"' + reCatego + '","' + str(reEngin) + '","' + reTitle + '","' + reContent + '");'
                insSQl = 'insert into search_result(url, kword, udate, score, category, engines, title, content) values("' + reUrl + '","' + keyword + '","' + cdTime + '",' + str(reScore) + ',"' + reCatego + '","' + reEngin + '","' + reTitle + '","' + reContent + '");'

                print(insSQl)
                # this is just to pass the new url around
                new_urls.append(reUrl)
                #new_results = copy.result
                new_results['searx'][keyword] = result
                myConn(insSQl)
                i = i + 1
    return new_urls


#
# Poll Searx instance for keyword.
#
def check_searx(keyword,category):
    hits = []


    for cat in category:

        # build parameter dictionary
        params = {}
        params['q'] = keyword
        params['categories'] = cat
        # params['time_range'] = 'day'  # day,week,month or year will work
        params['format'] = 'json'

        print("[*] Querying Searx for: %s" % keyword)

        # send the request off to searx
        try:
            response = requests.get(config.searx_url, params=params)

            results = response.json()

        except:
            return hits

        # if we have results we want to check them against our stored URLs
        # To Do: Handle multi content
        if len(results['results']):

            urls = []

            for result in results['results']:

                if result['url'] not in urls:
                    urls.append(result['url'])

            hits = check_urls(keyword, results, cat)

        return hits


def check_keywords(keywords,category):
    alert_email = {}
    # use the list of keywords and check each against searx
    for keyword in keywords:

        # query searx for the keyword
        result = check_searx(keyword,category)

        if len(result):
            alert_email['searx'] = {}
            alert_email['searx'][keyword] = result
            return alert_email

