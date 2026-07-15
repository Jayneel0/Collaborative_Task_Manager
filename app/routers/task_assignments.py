from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.security import (get_current_user,
                          is_owner,
                          is_member,
                          is_maintainer,
                          is_viewer)
router = APIRouter(prefix="/teams/{team_id}/projects/{project_id}/tasks/{task_id}/assignments")

@router.post("/", response_model=schemas.TaskAssignmentResponse)
def assign_user(team_id : int, project_id : int, task_id : int,
                assignment : schemas.TaskAssignmentCreate,
               current_user : models.User = Depends(get_current_user),
               db : Session = Depends(get_db)):
    if (not is_owner(db, team_id, current_user.id) and
        not is_maintainer(db, team_id, current_user.id)):
        raise HTTPException(
            status_code=403,
            detail = "Only team owners or maintainers can assign users"
        )
    return crud.assign_user(db, team_id,project_id, task_id, assignment)

@router.get("/", response_model=list[schemas.TaskAssignmentResponse])
def get_assignments(team_id : int, project_id : int, task_id : int,
                    current_user : models.User = Depends(get_current_user),
                    db : Session = Depends(get_db)):
    crud.get_member(db, team_id, current_user.id)
    return crud.get_assignments(db, team_id, project_id, task_id)

@router.get("/{user_id}", response_model=schemas.TaskAssignmentResponse)
def get_assignment(team_id : int, project_id : int, user_id : int, task_id : int,
                   current_user : models.User = Depends(get_current_user),
                   db : Session = Depends(get_db)):
    crud.get_member(db, team_id, current_user.id)
    return crud.get_assignment(db, team_id, project_id, task_id, user_id)

@router.delete("/{user_id}")
def remove_assignment(team_id : int, project_id : int, task_id : int,
                      user_id : int,current_user : models.User = Depends(get_current_user),
                      db : Session = Depends(get_db)):
    if (not is_owner(db, team_id, current_user.id) and
        not is_maintainer(db, team_id, current_user.id)):
        raise HTTPException(
            status_code=403,
            detail = "Only team owners or maintainers can remove assignments"
        )
    crud.remove_assignment(db, team_id, project_id, task_id, user_id)
    return {
        "message" : "Assignment removed Successfully"
    }