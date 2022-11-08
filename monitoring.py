import os
import requests
import smtplib
import time
import sqlite3
from email.mime.text import MIMEText

#Email setup
alert_email_account  = "info@dataphenix.com"
alert_email_password = "airMan3"
searx_url            = "http://192.168.1.130:8888/?"
max_sleep_time       = 240

# read in our list of keywords
#with open("keywords.txt", "r") as fd:
#    file_contents = fd.read()
#    keywords = file_contents.splitlines()

conn = None
try:
    conn = sqlite3.connect('kmoni.sqlite')
except sqlite3.Error as e:
    print(e)
if conn:
    print('you are connected')
    cur = conn.cursor()
    cur.execute("select words from keywords where status = 1")

    rows = cur.fetchall()
    #conn.close()
else:
    print("You are not connected.")



for row in rows:
    #print(row)
    keywords = row


#if not os.path.exists("keywords"):
#    os.mkdir("keywords")


#
# Check if the URL is new.
#
def check_urls(keyword, urls):
    new_urls = []

    with open("keywords/%s.txt" % keyword, "r") as fd:

       if(conn):
            chkUrl = 'select url from search_result where kword ="' + keyword +'" '
            print(chkUrl)

            cur = conn.cursor()
            cur.execute(chkUrl)

            #stored_urls = fd.read().splitlines()
                urlrow = cur.fetchall
                stored_urls = urlrow

        for url in urls:

            if url not in stored_urls:
                print ("[*] New URL for %s discovered: %s" % (keyword, url))
                #myconn = create_connection('kmoni.sqlite')
                insSQl = "insert into search_result(url, kword, date) values (" + url + " , " + keyword + " ," + time() +") "

                print(insSQl)
                if(conn):
                    cur.execute(insSQl)
                else:
                    print("You are not Connected")

                #new_urls.append(url)

    else:

        new_urls = urls

    # now store the new urls back in the file
    with open("keywords/%s.txt" % keyword, "ab") as fd:

        for url in new_urls:
            print( url)


    return new_urls


#
# Poll Searx instance for keyword.
#
def check_searx(keyword):
    hits = []

    # build parameter dictionary
    params = {}
    params['q'] = keyword
    params['categories'] = 'general'
    params['time_range'] = 'day'  # day,week,month or year will work
    params['format'] = 'json'

    print ("[*] Querying Searx for: %s" % keyword)

    # send the request off to searx
    try:
        response = requests.get(searx_url, params=params)

        results = response.json()

    except:
        return hits

    # if we have results we want to check them against our stored URLs
    if len(results['results']):

        urls = []

        for result in results['results']:

            if result['url'] not in urls:
                urls.append(result['url'])

        hits = check_urls(keyword, urls)

    return hits

def check_keywords(keywords):
    alert_email = {}

    time_start = time.time()

    # use the list of keywords and check each against searx
    for keyword in keywords:

        # query searx for the keyword
        result = check_searx(keyword)

        if len(result):

            print(result)


    time_end = time.time()
    total_time = time_end - time_start

    # if we complete the above inside of the max_sleep_time setting
    # we sleep. This is for Pastebin rate limiting
    if total_time < max_sleep_time:
        sleep_time = max_sleep_time - total_time

        print ("[*] Sleeping for %d s" % sleep_time)

        time.sleep(sleep_time)

    #return alert_email



# execute your search once first to populate results

check_keywords(keywords)

# now perform the main loop