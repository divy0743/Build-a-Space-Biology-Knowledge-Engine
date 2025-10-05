from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from routes import literature, research, publications

app = FastAPI(title="NASA Bioscience Dashboard")

# Include routers
app.include_router(literature.router, prefix="/literature", tags=["Literature"])
app.include_router(research.router, prefix="/research", tags=["Research"])
app.include_router(publications.router, prefix="/publications", tags=["Publications"])

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to NASA Bioscience Dashboard API"}

# -------------------------
# Global Error Handling
# -------------------------

# Handle routes that don't exist
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Page not found",
                "detail": f"The route '{request.url.path}' does not exist.",
                "suggestion": "Please check the available endpoints: /literature, /research, /publications"
            },
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail or "An unexpected error occurred."},
    )

# Handle unexpected server errors (500+)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc)
        },
    )

