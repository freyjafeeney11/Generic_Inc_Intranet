# Generic_Inc_Intranet

## Skills Used
 - Web development with Flask.
 - Database management with SQLite.
 - User authentication and access control.
 - Password hashing and salting for security.
 - Version control with Git.

## Intranet System Overview
This project introduces an intranet system designed for Generic Inc., featuring user authentication, registration, and access control functionalities. Here's a concise summary of key components and features:

## User Authentication

Users can log in securely using a username and password.
Passwords are hashed and salted using SHA-1 for enhanced security.
Account locking mechanism triggers after three consecutive unsuccessful login attempts.

## Registration Process
<img width="455" alt="Screenshot 2024-04-24 at 10 32 18 AM" src="https://github.com/freyjafeeney11/Generic_Inc_Intranet/assets/83038656/de5275e1-799e-4596-94a1-88cd9cef862d">

New users can register by providing unique usernames and passwords.
Passwords meet specific criteria and are securely hashed and salted.
Includes a Generate Password option that generates a secure password.
Registration details are stored in an SQL database for data integrity.

## Database Management

User information, including hashed passwords and access levels, is securely stored.
SQL queries facilitate efficient database management and data retrieval.
