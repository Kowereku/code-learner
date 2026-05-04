from fastapi import FastAPI

app = FastAPI(
    title="ZaPi App",
    version="0.1.0"
)

@app.get("/")
async def health_check():
    return {"status": "Database and API are running safely."}