# routers/research.py
from fastapi import APIRouter, HTTPException
import pandas as pd
import os
from db import db_admin1, db_admin2  # import both db connections

router = APIRouter()

# -------------------------
# Choose which admin to use for this collection
# -------------------------
collection = db_admin2['research']  # or db_admin1['research']

# -------------------------
# Upload CSV once on startup
# -------------------------
@router.on_event("startup")
async def create_indexes_research():
    # Text index for search queries
    await collection.create_index([
        ("ProjectTitle", "text"),
        ("PrincipalInvestigator", "text"),
        ("Organization", "text")
    ], name="research_text_index")

    # Unique index for TaskID
    await collection.create_index("TaskID")

    print("Indexes for Research collection created or ensured.")

# -------------------------
# Routes
# -------------------------

@router.get("/")
async def research_home():
    return {"message": "Welcome to the Research API!"}

# Get all tasks with pagination
@router.get("/tasks")
async def get_tasks(limit: int = 10, skip: int = 0):
    cursor = collection.find().skip(skip).limit(limit)
    tasks = await cursor.to_list(length=limit)
    
    # Convert MongoDB ObjectId to string for JSON compatibility
    for task in tasks:
        task["_id"] = str(task["_id"])
        
    return tasks

# Search tasks by text query
@router.get("/search")
async def search_tasks(query: str, limit: int = 10):
    cursor = collection.find({"$text": {"$search": query}}).limit(limit)
    tasks = await cursor.to_list(length=limit)
    for task in tasks:
        task["_id"] = str(task["_id"])
    return tasks

# Get single task by TaskID
@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = await collection.find_one({"TaskID": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task["_id"] = str(task["_id"])
    return task
