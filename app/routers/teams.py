from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.security import (get_current_user,
                          is_owner,
                          is_member,
                          is_maintainer,
                          is_viewer)

router = APIRouter(prefix ="/teams")

@router.post("/", response_model=schemas.TeamResponse)
def create_team(team : schemas.TeamCreate,
                current_user : models.User = Depends(get_current_user),
                db : Session = Depends(get_db)):
    new_team = crud.create_team(db, team)
    new_member = schemas.TeamMemberCreate(
        user_id=current_user.id,
        role = models.TeamRole.OWNER
    )
    crud.add_member(db, new_team.id, new_member)
    return new_team

@router.get("/", response_model=list[schemas.TeamResponse])
def get_teams(db : Session = Depends(get_db)):
    return crud.get_teams(db)

@router.get("/{team_id}", response_model=schemas.TeamResponse)
def get_team(team_id : int, db : Session = Depends(get_db)):
    return crud.get_team(db, team_id)

@router.patch("/{team_id}", response_model=schemas.TeamResponse)
def update_team(team_id : int,
                update : schemas.TeamUpdate,
                current_user : models.User = Depends(get_current_user),
                db : Session=Depends(get_db)):
    if (not is_owner(db, team_id, current_user.id)):
        raise HTTPException(
            status_code=403,
            detail = "Only team owners can update team"
        )
    return crud.update_team(db, team_id, update)

@router.delete("/{team_id}")
def delete_team(team_id : int,
                current_user : models.User = Depends(get_current_user),
                db : Session = Depends(get_db)):
    if (not is_owner(db, team_id, current_user.id)):
        raise HTTPException(
            status_code=403,
            detail = "Only team owners can delete team"
        )
    crud.delete_team(db, team_id)
    return {
        "message" : "Team Deleted Succesfully"
    }
   