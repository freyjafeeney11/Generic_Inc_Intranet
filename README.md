# Generic_Inc_Intranet
## Intranet System Overview
This project introduces an intranet system designed for Generic Inc., featuring user authentication, registration, and access control functionalities. Here's a concise summary of key components and features:

## User Authentication

Users can log in securely using a username and password.
Passwords are hashed and salted using SHA-1 for enhanced security.
Account locking mechanism triggers after three consecutive unsuccessful login attempts.
Registration Process

New users can register by providing unique usernames and passwords.
Passwords meet specific criteria and are securely hashed and salted.
Registration details are stored in an SQL database for data integrity.

## Database Management

User information, including hashed passwords and access levels, is securely stored.
SQL queries facilitate efficient database management and data retrieval.
