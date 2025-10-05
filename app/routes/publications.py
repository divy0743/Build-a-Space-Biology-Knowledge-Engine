# routers/publications.py
from fastapi import APIRouter, HTTPException
import pandas as pd
import os
from db import db_admin1, db_admin2  # import both db connections

router = APIRouter()

# -------------------------
# Choose which admin to use for this collection
# -------------------------
collection = db_admin2['publications']  # or db_admin1['publications']

# -------------------------
# Upload CSV once on startup
# -------------------------
@router.on_event("startup")
async def startup_db():
    csv_file = "SB_publication_PMC.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        data = df.to_dict(orient="records")
        count = await collection.count_documents({})
        if count == 0:
            await collection.insert_many(data)
            # Create indexes
            await collection.create_index("Title", unique=True)
            await collection.create_index("Link")
            print("Publications CSV uploaded and indexes created.")
        else:
            print("Publications collection already has data.")
    else:
        print("Publications CSV file not found!")

# -------------------------
# Routes
# -------------------------
@router.get("/")
async def get_publications(limit: int = 10, skip: int = 0):
    pubs = await collection.find().skip(skip).limit(limit).to_list(length=limit)
    return pubs

@router.get("/title/{title}")
async def get_publication_by_title(title: str):
    pub = await collection.find_one({"Title": title})
    if not pub:
        raise HTTPException(status_code=404, detail="Publication not found")
    return pub

@router.get("/search")
async def search_publications(query: str, limit: int = 10):
    pubs = await collection.find({"$text": {"$search": query}}).limit(limit).to_list(length=limit)
    return pubs
