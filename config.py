"""
Flask app configuration
"""
import secrets

DEBUG = True
SC = ";"
TEMPLATES_AUTO_RELOAD = True
DB_FILE = './users.db'
# generate random secret key with secrets module, 64 characters
SECRET_KEY = secrets.token_hex(32)


display = {}



