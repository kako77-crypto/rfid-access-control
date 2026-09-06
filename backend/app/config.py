import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://rfid_app:change-me-app-password@localhost:3306/rfid_access",
)

