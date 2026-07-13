from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.security import get_current_user

router = APIRouter(prefix="/teams/{team_id}/projects/{project_id}/tasks")

@router.post("/", response_model=schemas.TaskResponse)
def create_task(team_id : int, project_id : int,
                   task : schemas.TaskCreate,
               current_user : models.User = Depends(get_current_user),
               db : Session = Depends(get_db)):
    team_leaders = [leader.user_id for leader in crud.get_leaders(db, team_id)]
    if (current_user.id not in team_leaders):
        raise HTTPException(
            status_code=403,
            detail = "Only team leaders can create tasks"
        )
    return crud.create_task(db, team_id,project_id,task, current_user.id)

@router.get("/", response_model=list[schemas.TaskResponse])
def get_tasks(team_id : int, project_id : int, db : Session = Depends(get_db)):
    return crud.get_tasks(db, team_id, project_id)

@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(team_id : int, project_id : int, task_id : int,
             db : Session = Depends(get_db)):
    return crud.get_task(db, team_id, project_id, task_id)

@router.patch("/{task_id}", response_model = schemas.TaskResponse)
def update_task(team_id : int, project_id : int, task_id : int,
                  update : schemas.TaskUpdate,
                  current_user : models.User = Depends(get_current_user),
                  db : Session = Depends(get_db)):
    team_leaders = [leader.user_id for leader in crud.get_leaders(db, team_id)]
    if (current_user.id not in team_leaders):
        raise HTTPException(
            status_code=403,
            detail = "Only team leaders can update tasks"
        )
    return crud.update_task(db, team_id, project_id, task_id, update)

@router.delete("/{task_id}")
def delete_task(team_id : int, project_id : int, task_id : int,
                current_user : models.User = Depends(get_current_user),
                db : Session = Depends(get_db)):
    team_leaders = [leader.user_id for leader in crud.get_leaders(db, team_id)]
    if (current_user.id not in team_leaders):
        raise HTTPException(
            status_code=403,
            detail = "Only team leaders can delete tasks"
        )
    crud.delete_task(db, team_id, project_id, task_id)
    return {
        "message" : "Task Deleted Succesfully"
    }