"""
Freyja Feeney
Final Lab

"""

import sqlite3 as sqlite3
from datetime import datetime
import password_crack as pc

def create_db():
    """ Create table 'users' in 'users' database """
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        # four fields, user, pass, access level and number of failed login attempts (blocked)
        c.execute('''CREATE TABLE users
                    (
                    username text,
                    password text,
                    access_level text,
                    blocked integer
                    )''')
        conn.commit()
        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def get_date():
    """ Generate timestamp for data inserts """
    d = datetime.now()
    return d.strftime("%m/%d/%Y, %H:%M:%S")

# display the db
def query_db():
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        for row in c.execute("SELECT * FROM users"):
            print(row)
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()



#create_db()  # Run create_db function first time to create the database
#query_db()  # View all data stored in the