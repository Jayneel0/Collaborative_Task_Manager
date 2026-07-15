from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.security import (get_current_user,
                          is_owner,
                          is_member,
                          is_maintainer,
                          is_viewer)

router = APIRouter(prefix = "/teams/{team_id}/members")

@router.post("/", response_model=schemas.TeamMemberResponse)
def add_member(team_id : int,
               member : schemas.TeamMemberCreate,
               current_user : models.User = Depends(get_current_user),
               db : Session = Depends(get_db)):
    if (not is_owner(db, team_id, current_user.id) and
        not is_maintainer(db, team_id, current_user.id)):
        raise HTTPException(
            status_code=403,
            detail = "Only team owners or maintainers can add members"
        )
    return crud.add_member(db, team_id, member)

@router.get("/", response_model=list[schemas.TeamMemberResponse])
def get_members(team_id : int,
                current_user : models.User = Depends(get_current_user),
                db : Session = Depends(get_db)):
    crud.get_member(db, team_id, current_user.id)
    return crud.get_members(db, team_id)

@router.get("/{user_id}", response_model=schemas.TeamMemberResponse)
def get_member(team_id : int,
               user_id : int,
               current_user : models.User = Depends(get_current_user),
               db : Session = Depends(get_db)):
    crud.get_member(db, team_id, current_user.id)
    return crud.get_member(db, team_id, user_id)

@router.patch("/{user_id}", response_model = schemas.TeamMemberResponse)
def update_member(team_id : int, user_id : int,
                  update : schemas.TeamMemberUpdate,
                  current_user : models.User = Depends(get_current_user),
                  db : Session = Depends(get_db)):
    if (not is_owner(db, team_id, current_user.id)):
        raise HTTPException(
            status_code=403,
            detail = "Only team owners can change member roles"
        )
    owners = crud.get_owners(db, team_id)
    if (len(owners) == 1 and
        owners[0].user_id == user_id and
        update.role != models.TeamRole.OWNER):
        raise HTTPException(
            status_code=409,
            detail="A team must have at least one owner."
        )
    return crud.update_member(db, team_id, user_id, update)

@router.delete("/{user_id}")
def remove_member(team_id : int,
                  user_id : int,
                  current_user : models.User = Depends(get_current_user),
                  db : Session = Depends(get_db)):
    if (not is_owner(db, team_id, current_user.id)):
        raise HTTPException(
            status_code=403,
            detail = "Only team owners can delete members"
        )
    owners = crud.get_owners(db, team_id)
    if (len(owners) == 1 and
        owners[0].user_id == user_id):
        raise HTTPException(
            status_code=409,
            detail="A team must have at least one owner."
        )
    crud.remove_member(db, team_id, user_id)
    return {
        "message" : "Member Removed Succesfully"
    }
