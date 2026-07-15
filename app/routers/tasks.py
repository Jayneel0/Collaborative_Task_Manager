from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.security import (get_current_user,
                          is_owner,
                          is_member,
                          is_maintainer,
                          is_viewer)

router = APIRouter(prefix="/teams/{team_id}/projects/{project_id}/tasks")

@router.post("/", response_model=schemas.TaskResponse)
def create_task(team_id : int,
                project_id : int,
                task : schemas.TaskCreate,
                current_user : models.User = Depends(get_current_user),
                db : Session = Depends(get_db)):
    if (not is_owner(db, team_id, current_user.id) and
        not is_maintainer(db, team_id, current_user.id) and 
        not is_member(db, team_id, current_user.id)):
        raise HTTPException(
            status_code=403,
            detail = "Only team owners, maintainers or members can create tasks"
        )
    return crud.create_task(db, team_id,project_id,task, current_user.id)

@router.get("/", response_model=list[schemas.TaskResponse])
def get_tasks(team_id : int,
              project_id : int,
              title : str | None=None,
              status : models.TaskStatus | None=None,
              priority : models.TaskPriority | None=None,
              skip: int = Query(default=0, ge=0),
              limit: int | None=None,
              current_user : models.User = Depends(get_current_user),
              db : Session = Depends(get_db)):
    crud.get_member(db, team_id, current_user.id)
    return crud.get_tasks(db, team_id, project_id, title, status, priority, skip, limit)

@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(team_id : int,
             project_id : int,
             task_id : int,
             current_user : models.User = Depends(get_current_user),
             db : Session = Depends(get_db)):
    crud.get_member(db, team_id, current_user.id)
    return crud.get_task(db, team_id, project_id, task_id)

@router.patch("/{task_id}", response_model = schemas.TaskResponse)
def update_task(team_id : int,
                project_id : int,
                task_id : int,
                update : schemas.TaskUpdate,
                current_user : models.User = Depends(get_current_user),
                db : Session = Depends(get_db)):
    if (not is_owner(db, team_id, current_user.id) and
        not is_maintainer(db, team_id, current_user.id) and 
        not is_member(db, team_id, current_user.id)):
        raise HTTPException(
            status_code=403,
            detail = "Only team owners, maintainers or members can update tasks"
        )
    if (is_member(db, team_id, current_user.id)):
        crud.get_assignment(db, team_id, project_id, task_id, current_user.id)
    return crud.update_task(db, team_id, project_id, task_id, update)

@router.delete("/{task_id}")
def delete_task(team_id : int,
                project_id : int,
                task_id : int,
                current_user : models.User = Depends(get_current_user),
                db : Session = Depends(get_db)):
    if (not is_owner(db, team_id, current_user.id) and
        not is_maintainer(db, team_id, current_user.id)):
        raise HTTPException(
            status_code=403,
            detail = "Only team owners or maintainers can delete tasks"
        )
    crud.delete_task(db, team_id, project_id, task_id)
    return {
        "message" : "Task Deleted Succesfully"
    }