# DB connection setup 

from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

# Admin 1 connection
MONGO_URI_ADMIN1 = os.getenv("MONGO_URI_ADMIN1")
client1 = AsyncIOMotorClient(MONGO_URI_ADMIN1)

# Admin 2 connection
MONGO_URI_ADMIN2 = os.getenv("MONGO_URI_ADMIN2")
client2 = AsyncIOMotorClient(MONGO_URI_ADMIN2)

DB_NAME = os.getenv("DB_NAME")

# Two db objects
db_admin1 = client1[DB_NAME]
db_admin2 = client2[DB_NAME]
