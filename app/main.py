from fastapi import FastAPI
from app.database import Base,engine
from app import models
from app.routers import (
    users,
    teams,
    team_members,
    projects,
    tasks,
    task_assignments,
    comments,
)

app = FastAPI()

app.include_router(users.router)
app.include_router(teams.router)
app.include_router(team_members.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(task_assignments.router)
app.include_router(comments.router)
app.include_router(users.router)

Base.metadata.create_all(bind=engine)
@app.get("/")
def root():
    return{
        "message" : "Collaborative Task Manager API"
    }