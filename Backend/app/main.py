
from fastapi import FastAPI
from app.database import engine
from app import models



app = FastAPI(title="Transit Pass System API")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Transit Pass System API running"}

