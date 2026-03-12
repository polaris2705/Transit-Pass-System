'''FASTAPI application entry point '''

from fastapi import FastAPI
from app.database import engine
from app import models
from app.Routers import auth, passes, validate, trips, admin

app = FastAPI(title="Transit Pass System API")

app.include_router(auth.router)
app.include_router(passes.router)
app.include_router(validate.router)
app.include_router(trips.router)
app.include_router(admin.router)

# Root endpoint (GET)
@app.get("/")
def root():
    return {"message": "Transit Pass System API running"}

