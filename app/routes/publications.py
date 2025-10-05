# routers/publications.py
from fastapi import APIRouter, HTTPException
from db import db_admin1, db_admin2  # import both db connections

router = APIRouter()

# -------------------------
# Choose which admin to use for this collection
# -------------------------
collection = db_admin2['publications']  # or db_admin1['publications']

# -------------------------
# Routes
# -------------------------

@router.on_event("startup")
async def create_indexes_publications():
    # Text index for search queries (only on Title, since that's the only text field)
    await collection.create_index([("Title", "text")], name="publications_text_index")

    # Unique index for Title
    await collection.create_index("Title")
    
    # Index for Link (non-unique)
    await collection.create_index("Link")
    
    print("Indexes for Publications collection created or ensured.")

# Home endpoint
@router.get("/")
async def publication_home():
    return {"message": "Welcome to the Publications API!"}

# Get publication by title
@router.get("/title/{title}")
async def get_publication_by_title(title: str):
    pub = await collection.find_one({"Title": title})
    if not pub:
        raise HTTPException(status_code=404, detail="Publication not found")
    pub["_id"] = str(pub["_id"])  # Convert ObjectId to string for JSON
    return pub

# Search publications
@router.get("/search")
async def search_publications(query: str, limit: int = 10):
    cursor = collection.find({"$text": {"$search": query}}).limit(limit)
    pubs = await cursor.to_list(length=limit)
    for pub in pubs:
        pub["_id"] = str(pub["_id"])  # Convert ObjectId to string for JSON
    return pubs

# Get limited publications list
@router.get("/list")
async def get_publications(limit: int = 10, skip: int = 0):
    cursor = collection.find().skip(skip).limit(limit)
    pubs = await cursor.to_list(length=limit)
    for pub in pubs:
        pub["_id"] = str(pub["_id"])  # Convert ObjectId to string
    return pubs
