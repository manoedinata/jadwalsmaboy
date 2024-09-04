from os import environ 
from dotenv import load_dotenv

if not environ.get("ENV"):
    # Load dotenv if not using environment variable
    load_dotenv(".env")

# App secret key
SECRET_KEY = environ.get("SECRET_KEY")

# Database URL (MySQL/MariaDB preferred)
SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")

# Fonnte Bot token
BOT_TOKEN = environ.get("BOT_TOKEN")
