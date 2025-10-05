# Mongo DB Connection + env config

# config.py (or db.py)
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient

# Load variables from .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")

# -------------------------
# Admin 1 connection
# -------------------------
MONGO_URI_ADMIN1 = os.getenv("MONGO_URI_ADMIN1")
client_admin1 = AsyncIOMotorClient(MONGO_URI_ADMIN1)
db_admin1 = client_admin1[DB_NAME]

# -------------------------
# Admin 2 connection
# -------------------------
MONGO_URI_ADMIN2 = os.getenv("MONGO_URI_ADMIN2")
client_admin2 = AsyncIOMotorClient(MONGO_URI_ADMIN2)
db_admin2 = client_admin2[DB_NAME]
