import sqlite3


def myConn(mySQL):
    conn = None
    qType = mySQL[0:6]

    try:
        conn = sqlite3.connect('localdata/zupDB.sqlite')
        if conn:
            if (qType == 'select'):
                #conn.row_factory = tuple_factory
                cur = conn.cursor()
                # cur.execute("select words from keywords where status = 1")
                cur.execute(mySQL)
                rows = cur.fetchall()
                conn.close()
                return rows
            elif (qType == 'insert'):
                cur = conn.cursor()
                # cur.execute("select words from keywords where status = 1")
                cur.execute(mySQL)
                conn.commit()
                conn.close()
            elif (qType == 'update'):

                return "Data Inserted"
            else:
                return "What are you trying to do stupid"
        else:
            print("You are not connected.")
    except sqlite3.Error as e:
        print(e)
