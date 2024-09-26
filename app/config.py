import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
MYSQL_SERVER = os.getenv('MYSQL_SERVER')
MYSQLUSER = os.getenv('MYSQLUSER')
MYSQLPASSWORD = quote_plus(os.getenv('MYSQLPASSWORD'))
MYSQLPORT = os.getenv('MYSQLPORT')
MYSQLDB = os.getenv('MYSQLDB')

# Construct the DATABASE_URL
DATABASE_URL = (f"mysql+pymysql://{MYSQLUSER}:{MYSQLPASSWORD}@{MYSQL_SERVER}:{MYSQLPORT}/{MYSQLDB}")

# Secret key for JWT encoding and decoding
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Token expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")

# OTP expiration time
OTP_LENGTH = os.getenv("OTP_LENGTH")
OTP_VALID_DURATION = os.getenv("OTP_VALID_DURATION")
OTP_MAX_ATTEMPTS = os.getenv("OTP_MAX_ATTEMPTS")

# Power Automate Workflow URL
SEND_EMAIL_URL = os.getenv("SEND_EMAIL_URL")
OTP_TEST_EMAIL = os.getenv("OTP_TEST_EMAIL")
OTP_TEST_CC_EMAIL = os.getenv("OTP_TEST_CC_EMAIL")