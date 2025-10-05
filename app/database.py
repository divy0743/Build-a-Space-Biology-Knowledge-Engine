# DB connection setup 

from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("mongodb+srv://divyanshikhare37_db_user:3OnM4mWUoH02B9OL@cluster0.vwumbxa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&authSource=admin")
DB_NAME = os.getenv("nasa_db")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
