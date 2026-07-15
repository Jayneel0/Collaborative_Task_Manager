from fastapi import FastAPI, Request
from app.database import Base,engine, SessionLocal
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
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
import time, logging
from sqlalchemy import text
from datetime import datetime, UTC
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
app = FastAPI()

app.include_router(users.router, prefix = "/api/v1")
app.include_router(teams.router, prefix = "/api/v1")
app.include_router(team_members.router, prefix = "/api/v1")
app.include_router(projects.router, prefix = "/api/v1")
app.include_router(tasks.router, prefix = "/api/v1")
app.include_router(task_assignments.router, prefix = "/api/v1")
app.include_router(comments.router, prefix = "/api/v1")

app = FastAPI(lifespan=lifespan)
@app.get("/")
def root():
    return{
        "message" : "Collaborative Task Manager API"
    }
    
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation Failed",
            "errors": exc.errors()
        }
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)   

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(
        "%s %s -> %d (%.4fs)",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )
    return response

@app.get("/health")
def health():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        database = "connected"
    except SQLAlchemyError:
        database = "disconnected"
    finally:
        db.close()

    return {
        "status": "healthy",
        "database": database,
        "timestamp": datetime.now(UTC)
    }