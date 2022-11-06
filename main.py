# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

import config
import emailsender
from localdata.DBConn import myConn
from searxsearchdata import check_keywords


def main():
    time_start = time.time()

    # execute your search once first to populate results
    pullKeys = "select words from keywords where status = 1"

    k = myConn(pullKeys)

    time_end = time.time()
    total_time = time_end - time_start

    for row in k:
        # print(row)
        keywords = row
        alert_email = check_keywords(keywords)
        if alert_email:
            # if we have alerts send them out
            emailsender.send_alert(alert_email)

            # if we complete the above inside of the max_sleep_time setting
            # we sleep. This is for Pastebin rate limiting
            if total_time < config.max_sleep_time:
                sleep_time = config.max_sleep_time - total_time

                print("[*] Sleeping for %d s" % sleep_time)

                time.sleep(sleep_time)
                main()
    #  now perform the main loop


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
