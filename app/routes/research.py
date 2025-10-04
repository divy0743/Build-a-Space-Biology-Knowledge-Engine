from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import pandas as pd
import os

router = APIRouter()

# -------------------------
# MongoDB connection
# -------------------------
MONGO_URI = "mongodb+srv://suresharjun621_db_user:uTrU5S6Bv9CKPHDA@cluster0.vwumbxa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URI)
db = client['nasa_db']
collection = db['research']

# -------------------------
# Upload CSV once on startup
# -------------------------
@router.on_event("startup")
async def startup_db():
    csv_file = "TaskbookExport_.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        data = df.to_dict(orient="records")
        count = await collection.count_documents({})
        if count == 0:
            await collection.insert_many(data)
            # Indexes for fast search
            await collection.create_index([("ProjectTitle", "text"),
                                           ("PrincipalInvestigator", "text"),
                                           ("Organization", "text")])
            await collection.create_index("TaskID", unique=True)
            print("Research CSV uploaded and indexes created.")
        else:
            print("Research collection already has data.")
    else:
        print("Research CSV file not found!")

# -------------------------
# Routes
# -------------------------
@router.get("/tasks")
async def get_tasks(limit: int = 10, skip: int = 0):
    tasks = await collection.find().skip(skip).limit(limit).to_list(limit)
    return tasks

@router.get("/search")
async def search_tasks(query: str, limit: int = 10):
    tasks = await collection.find({"$text": {"$search": query}}).to_list(limit)
    return tasks

@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = await collection.find_one({"TaskID": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
