from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.security import get_current_user

router = APIRouter(prefix="/teams/{team_id}/projects/{project_id}/tasks/{task_id}/assigments")

@router.post("/", response_model=schemas.TaskAssignmentResponse)
def create_task(team_id : int, project_id : int, task_id : int,
                assignment : schemas.TaskAssignmentCreate,
               current_user : models.User = Depends(get_current_user),
               db : Session = Depends(get_db)):
    team_leaders = [leader.user_id for leader in crud.get_leaders(db, team_id)]
    if (current_user.id not in team_leaders):
        raise HTTPException(
            status_code=403,
            detail = "Only team leaders can assign users."
        )
    return crud.assign_user(db, team_id,project_id, task_id, assignment)

@router.get("/", response_model=list[schemas.TaskAssignmentResponse])
def get_assignments(team_id : int, project_id : int,
                    task_id : int, db : Session = Depends(get_db)):
    return crud.get_assignments(db, team_id, project_id, task_id)

@router.get("/{user_id}", response_model=schemas.TaskAssignmentResponse)
def get_assignment(team_id : int, project_id : int, user_id : int,
                    task_id : int, db : Session = Depends(get_db)):
    return crud.get_assignment(db, team_id, project_id, task_id, user_id)

@router.delete("/{user_id}")
def remove_assignment(team_id : int, project_id : int, task_id : int,
                      user_id : int,current_user : models.User = Depends(get_current_user),
                      db : Session = Depends(get_db)):
    team_leaders = [leader.user_id for leader in crud.get_leaders(db, team_id)]
    if (current_user.id not in team_leaders):
        raise HTTPException(
            status_code=403,
            detail = "Only team leaders can remove assignments"
        )
    crud.remove_assignment(db, team_id, project_id, task_id, user_id)
    return {
        "message" : "Assignment removed Succesfully"
    }