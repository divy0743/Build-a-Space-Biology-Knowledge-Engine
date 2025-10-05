# test_mongo.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get MongoDB URI and DB name from .env
MONGO_URI_ADMIN1 = os.getenv("MONGO_URI_ADMIN1")
MONGO_URI_ADMIN2 = os.getenv("MONGO_URI_ADMIN2")
DB_NAME = os.getenv("DB_NAME")

# Choose which admin to test
uri = MONGO_URI_ADMIN2  # or MONGO_URI_ADMIN2
client = MongoClient(uri)
db = client[DB_NAME]

try:
    # Test connection by listing databases
    print("Databases:", client.list_database_names())

    # Test collections
    print("Literature count:", db['literature'].count_documents({}))
    print("Publications count:", db['publications'].count_documents({}))
    print("Research count:", db['research'].count_documents({}))

    # Fetch one sample document from each collection
    print("\nSample Literature doc:", db['literature'].find_one({}))
    print("Sample Publications doc:", db['publications'].find_one({}))
    print("Sample Research doc:", db['research'].find_one({}))

    print("\nConnection test successful!")

except Exception as e:
    print("Connection failed:", e)
