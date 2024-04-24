Freyja Feeney
CS2660
Cybersecurity Principles
Final Project/Lab Assignment 8

Hello! Welcome to my company Generic Inc.'s intranet system. The site opens up with a menu where you can choose to either
log in or register. The format of the site is similar to the lab 6 flask app. I drew a little owl/chicken/hamster to be the
company logo. You can click on that image to return to home at any point.

#### LOGGING IN ###

Once you click login, you are able to enter a username and password into the username and password fields. The system will
search through the database and test whether or not a user already exists with that username. If a user already exists,
you will be allowed to log in, if not, it will notify you that no user exists with that name. 

A registered user has 3 attempts to log in. After the third attempt, the account with that username is locked. I did this by
keeping track of the login attempts in the database, with each account created having 0. Once an unsuccessful attempt is made, 
that counter is incremented for the respective username. The program will use authenticate to compare the plaintext entered password and the hashed password in the database by hashing
the plaintext password and returning either true or false. 

Once logged in, a user, based on their access level, is presented with a success message and a menu displaying their options.
The user can access the documents specified by their access level only. I created an admin and standard user for testing purposes, but the
users created in registration are all "guest". 

The usernames and passwords are case sensitve!!

#### REGISTERING ###

When you click register, the screen displays a similar username and password field. Below them are a register button and a 
"generate passsword" button. When registering with a username, the system will check to see if there is already a user with that name,
if there is, you will be prompted to choose a new one. The password must be 8-25 characters long, and I included the validation for each type of letter, 
number, and special character. I did this using the secrets module in python, and I have cited it below in the works cited section.

The generate password button also uses the secrets module. If you click this button, a strong password is generated and automatically
entered into the password field. It will also display a flash of the password, so you can copy and paste it if you need to. If the user chooses not to use this option, the generated_password is set to None and nothing is displayed in the
password field. The plaintext password is then hashed, using a salt with 40 characters, and stored in the database. 

Once you register successfully, the page will take you to the login page immediately, where you are prompted to now log in. 

#### DATABASE: ###

The database, users.db, has four fields. Username, a hashed password, the access level, and the number of failed login attempts.
You can use sq.query_db() at the bottom of bank.py to print out the database if needed. 

#### TESTING ###

1. Unzip the compressed file
3. Make sure the instance and template folders are intact!
4. Run werk.py!
5. Try logging in / registering!

- make sure you remember/save your password in registration because it isn't stored in plaintext anywhere
(users.db should be created already but if you need to make a new one use the sq.create_db() call at the end of bank.py!)
(if you want to create users that aren't guest, change the line #### ADMIN LEVEL SET ##### admin_level = str("guest") to either "admin" or "standard")

I created three users already in the database, one of each access level, to demonstrate the different levels of access
the users have in this system:

user - admin
pass - Admin123!

user - standard
pass - Standard123!

user - guest
pass - Guest123!

I wrote them down here in case you need them for testing! The database only stores hashed passwords also. The admin
has access to all three tiers, engineering documents, accounting, and time reporting. The standard level has all but the 
engineering documents, and the guest only has access to time reporting. 

Thank you for using my program!

#### SOURCES ###

// Previous Lab Code:
Eddy, Jim (2023)
Lab Assignment 4.0-6.0 Flask App Code + Hashing
https://gitlab.uvm.edu/James.Eddy/cs-166-catamount-community-bank
- password_crack.py (modified it but referenced))
- style.css (modified it but referenced)
- layout.html (modified it but referenced)
- home.html
- bank.py, modified, added methods from sql example provided
- setup.py (changed secret key to be secure)
- sql example functions provided

// Rainbow Button Styling: I used this to make my buttons rainbow
Raza, S. M. (2023, March 3). 
22 useful CSS tips and tricks every developer should know. 
DEV Community. 
https://dev.to/devsyedmohsin/22-useful-css-tips-and-tricks-every-developer-should-know-13c6 

// Python secrets documentation:
Secrets - generate secure random numbers for managing secrets. 
Python documentation. (n.d.). 
https://docs.python.org/3/library/secrets.html 

// HTML conditionals: I used this because I didn't know how to include a conditional in an HTML statement
How to build HTML for conditional statements. (n.d.). 
https://help.retentionscience.com/hc/en-us/articles/115003025814-How-To-Build-HTML-for-Conditional-Statements 

