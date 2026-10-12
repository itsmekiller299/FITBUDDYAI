from fastapi import FastAPI

app = FastAPI(
    title="FitBuddy AI",
    description="AI-powered fitness plan generator and tracker",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "FitBuddy API is running"}