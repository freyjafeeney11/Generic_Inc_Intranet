# Freyja Feeney
# CS2660
# Lab Assignment 8.0
# This is the main file!

import sqlite3
from datetime import datetime
import csv
from config import display
from flask import Flask, render_template, request, url_for, flash, redirect
from password_crack import hash_pw
from password_crack import authenticate
import sq_example as sq
import string
import secrets 

# constants
MAX_LOGIN_ATTEMPTS = 3

# setup app
app = Flask(__name__, static_folder='instance/static')
app.config.from_object('config')

# home page of generic inc portal, displays register or log in options
@app.route("/", methods=['GET', 'POST'])
def home():
    """Home page """
    return render_template('home.html',
                           heading="Generic Inc. Employee Portal",
                           show=display)

# if login is clicked
@app.route("/login", methods=['GET', 'POST'])
def login():
    # make array to store data
    credentials = []
    # initialize variable for user existing or not
    user_exists = False
    # connect to the database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # for each row in the database, append to credentials
    for row in c.execute("SELECT * FROM users"):
        credentials.append(row)
        # print out the data for testing
        print(row)

    # enter the username and password
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # first, check if this registered user is already blocked and if the username exists in the database
        for row in credentials:
            if row[0] == username:
                # user exists
                user_exists = True
                # if the number of sign in attempts is over 3, the account is blocked for this registered user
                if row[3] >= MAX_LOGIN_ATTEMPTS:
                    flash("Your account: " + str(username) + ", is blocked.", "alert-danger")
                    # returns the user back to home because blocked
                    return render_template('home.html')
                # if the password and and username match
                if authenticate(row[1], password):
                    # redirect to a successful login screen and pass username along with it
                    return redirect(url_for('login_success',
                                            id_=username))
                # if the login failed
                else:
                    # connect to the database again
                    with sqlite3.connect('users.db') as conn:
                        c = conn.cursor()
                        # increment the integer blocked by one in the db
                        # didnt use parameterized for blocked because it is an internal variable, never modified by user
                        c.execute("UPDATE users SET blocked = blocked + 1 WHERE username = ?", (username,))
                        conn.commit()
                        # if the number of blocks currently plus one is the max
                        if (row[3] + 1 == MAX_LOGIN_ATTEMPTS):
                            # return to home because the account is blocked
                            flash("Your account has been blocked.", "alert-danger")
                            return redirect(url_for('home'))
                        else:
                            # if the account isn't blocked, show an alert and prompt to log in again
                            flash("Invalid password!", 'alert-danger')
                        return redirect(url_for('login'))
        # if the user doesn't exist in the db
        if user_exists == False:
            # notify and prompt to try logging in with a different username
            flash("No account with this username.", "alert-danger")
            return redirect(url_for('login'))
    return render_template('login.html', title="Welcome Back!", heading="Welcome Back!")


# if register is clicked
@app.route("/register", methods=['GET', 'POST'])
def register():
    # initialize array for db contents
    credentials = []
    # initialize variables
    present = False
    num = False
    upper = False
    lower = False
    # populate array w db
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    for row in c.execute("SELECT * FROM users"):
        credentials.append(row)
        print(row)
    # checks for generated password
    generated_password = request.args.get('generated_password', None)
    # create special chars string
    special_char = "!@#$%^&*:;()\/<>"

    # input username and password
    if request.method == 'POST':
        username = request.form.get('username')
        for user in credentials:
            if user[0] == username:
                # if username already exists, redirect and prompt to choose a different username
                flash("Username already taken.")
                return render_template('register.html',
                            title="Log In!",
                            heading="Welcome Back!")
        # if generate password option was picked
        if 'generate_password' in request.form:
            # set generated password to the result of generate_password function
            generated_password = generate_password()
            # show the result
            flash("Your randomly generated strong password is: " + generated_password)
            # render the template with the username and password fields filled out
            return render_template('register.html', generated_password=generated_password, username=username)
        else:
            # if the button wasn't pressed, just enter the password
            password = request.form['password']
        # hash the pw
        hashed_password = hash_pw(password)
        # password input validation
        if any(char in special_char for char in password):
            present = True
        for letter in password: 
            if letter.isupper():
                upper = True
            if letter.islower():
                lower = True
            if letter.isdigit():
                num = True
        # Password must be 8-25 characters and contain at least one special character, capital letter, lowercase letter, and number
        if (present == False) or (len(password) > 25 or len(password) < 8) or (upper == False) or (lower == False) or (num == False):
            flash("Password must be 8-25 characters and contain at least one special character, capital letter, lowercase letter, and number.")
            return render_template('register.html',
                        title="Log In!",
                        heading="Welcome Back!")
        #### ADMIN LEVEL SET #####
        admin_level = str("guest")
        # blocked is number of failed login attempts
        blocked = 0
        # insert data into db with parameterized queries
        data_to_insert = [(username, hashed_password, admin_level, blocked)]
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", data_to_insert)
            conn.commit()
        except sqlite3.IntegrityError:
            print("Error. Tried to add duplicate record!")
        else:
            print("Success")
        finally:
            if c is not None:
                c.close()
            if conn is not None:
                conn.close()
        # success message!
        flash("Account created! Now log in!", 'alert-success')
        # redirect to login directly!
        return redirect(url_for('login',
            id_=username))
    return render_template('register.html',
                        title="Log In!",
                        heading="Welcome Back!")

# if login was successful
@app.route("/login_success/<string:id_>", methods=['GET', ])
def login_success(id_):
    flash("Welcome back, " + id_ + "! You have logged in!", 'alert-success')
    # check access level:
    access = get_access_level(id_)
    # redirect to access level specific menus
    # didnt add input validation here because the access level is technically set by the db
    if access == "admin":
        flash("You have the top-secret access to top-secret documents!")
        return render_template('admin_home.html',
                               title="Menu",
                               heading="Menu",
                               access_level=access)
    if access == "standard":
        flash("You have standard access to these documents!")
        return render_template('standard_home.html',
                               title="Menu",
                               heading="Menu",
                               access_level=access)
    if access == "guest":
        flash("Welcome guest! You may log your hours.")
        return render_template('guest_home.html',
                               title="Menu",
                               heading="Menu",
                               access_level=access)

# this are the different document portals
@app.route("/engineering", methods=['GET', ])
def engineering():
    flash("You accessed the engineering documents!", 'alert-success')
    # render the same html because there isn't functionality, just demonstrates access
    return render_template('accessed.html')
@app.route("/accounting", methods=['GET', ])
def accounting():
    flash("You accessed the account documents!", 'alert-success')
    return render_template('accessed.html')
@app.route("/time", methods=['GET', ])
def time():
    flash("You accessed the time reporting portal!", 'alert-success')
    return render_template('accessed.html')

## Functions ##

# this function returns the access level when given the username    
def get_access_level(id_):
    # get access level from database
    access_level = ""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    for row in c.execute("SELECT * FROM users WHERE username = ?", (id_,)):
        # set access level to the third element, the access level
        access_level = row[2]
    return access_level

# this function generates the strong password using secrets
def generate_password():
    # special chars
    special_char = "!@#$%^&*:;()\/<>"
    # append the chars to the letters and digits
    alphabet = string.ascii_letters + string.digits + special_char
    while True:
        # generate a 12 char long password
        password = ''.join(secrets.choice(alphabet) for i in range(12))
        # make sure all requirements are met
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password)
                and any(c in special_char for c in password)):
            break
    # return pw
    return password

# use these for database management
#sq.create_db()
#sq.query_db()