from dotenv import load_dotenv
import os

load_dotenv()

class Setting:
    # DB URL
    DB_URL = os.getenv('DB_URL')

    # JWT Variables
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    