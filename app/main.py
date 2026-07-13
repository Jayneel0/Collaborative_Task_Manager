from fastapi import FastAPI
from app.routers import users
from app.database import Base,engine
from app import models

app = FastAPI()
app.include_router(users.router)
Base.metadata.create_all(bind=engine)
@app.get("/")
def root():
    return{
        "message" : "Collaborative Task Manager API"
    }