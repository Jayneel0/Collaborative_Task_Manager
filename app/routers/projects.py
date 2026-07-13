from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.security import get_current_user

router = APIRouter(prefix="/teams/{team_id}/projects")

@router.post("/", response_model=schemas.ProjectResponse)
def create_project(team_id : int, project : schemas.ProjectCreate,
               current_user : models.User = Depends(get_current_user),
               db : Session = Depends(get_db)):
    team_leaders = crud.get_leaders(db, team_id)
    if (current_user.id not in team_leaders.user_id):
        raise HTTPException(
            status_code=403,
            detail = "Only team leaders can create projects"
        )
    return crud.create_project(db, team_id, project)

@router.get("/", response_model=list[schemas.ProjectResponse])
def get_projects(team_id : int, db : Session = Depends(get_db)):
    return crud.get_projects(db, team_id)

@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project(team_id : int, project_id : int, db : Session = Depends(get_db)):
    return crud.get_project(db, team_id, project_id)

@router.patch("/{project_id}", response_model = schemas.ProjectResponse)
def update_project(team_id : int, project_id : int,
                  update : schemas.ProjectUpdate,
                  current_user : models.User = Depends(get_current_user),
                  db : Session = Depends(get_db)):
    team_leaders = crud.get_leader(db, team_id)
    if (current_user.id != team_leaders.user_id):
        raise HTTPException(
            status_code=403,
            detail = "Only team leaders can update projects"
        )
    return crud.update_project(db, team_id, project_id, update)


@router.delete("/{project_id}")
def delete_project(team_id : int,
                  project_id : int,
                  current_user : models.User = Depends(get_current_user),
                  db : Session = Depends(get_db)):
    team_leaders = crud.get_leaders(db, team_id)
    if (current_user.id not in team_leaders):
        raise HTTPException(
            status_code=403,
            detail = "Only team leaders can delete projects"
        )
    crud.delete_project(db, team_id, project_id)
    return {
        "message" : "Project Deleted Succesfully"
    }