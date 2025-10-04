# main.py
from fastapi import FastAPI
from routers import literature  # import the router

app = FastAPI(title="NASA Bioscience Dashboard")

# Include the literature routes
app.include_router(literature.router, prefix="/literature", tags=["Literature"])
app.include_router(research.router, prefix="/research", tags=["Research"])
app.include_router(publications.router, prefix="/publications", tags=["Publications"])

@app.get("/")
async def root():
    return {"message": "Welcome to NASA Bioscience Dashboard API"}
