# routers/literature.py
from fastapi import APIRouter, HTTPException
from db import db_admin1, db_admin2

router = APIRouter()

# -------------------------
# Choose which admin to use for this collection
# -------------------------
collection = db_admin2['literature']  # or db_admin1['literature']

# -------------------------
# Routes
# -------------------------
@router.on_event("startup")
async def create_indexes():
    # Text index for search queries
    await collection.create_index([
        ("Title", "text"),
        ("Abstract", "text"),
        ("Authors", "text"),
        ("FirstAuthor", "text"),
        ("JournalTitle", "text")
    ], name="literature_text_index")

    # Unique indexes for ID fields
    await collection.create_index("PMID", unique=True)
    await collection.create_index("DOI", unique=True)

    # Optional index for sorting/filtering by year
    await collection.create_index("PubYear")
    
    print("Indexes for Literature collection created or ensured.")
    
@router.get("/")
async def literature_home():
    return {"message": "Welcome to the Literature API!"}

# Get paper by PMID
@router.get("/papers/{pmid}")
async def get_paper(pmid: str):
    paper = await collection.find_one({"PMID": pmid})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    paper["_id"] = str(paper["_id"])  # Convert ObjectId to string
    return paper

# Search papers
@router.get("/search")
async def search_papers(query: str, limit: int = 10):
    cursor = collection.find({"$text": {"$search": query}}).limit(limit)
    papers = await cursor.to_list(length=limit)
    for paper in papers:
        paper["_id"] = str(paper["_id"])
    return papers

# Get limited papers list
@router.get("/papers")
async def get_papers(limit: int = 10, skip: int = 0):
    cursor = collection.find().skip(skip).limit(limit)
    papers = await cursor.to_list(length=limit)
    for paper in papers:
        paper["_id"] = str(paper["_id"])
    return papers
