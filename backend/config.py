import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# Example of connection URL, change this as needed
SQLALCHEMY_DATABASE_URI = 'postgres://bunty@localhost:5432/trivia'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # silence the deprecation warning
