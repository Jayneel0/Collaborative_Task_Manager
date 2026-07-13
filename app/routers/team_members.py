from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.security import get_current_user

router = APIRouter(prefix = "/teams/{team_id}/members")

@router.post("/", response_model=schemas.TeamMemberResponse)
def add_member(team_id : int, member : schemas.TeamMemberCreate,
               current_user : models.User = Depends(get_current_user),
               db : Session = Depends(get_db)):
    team_leaders = [leader.user_id for leader in crud.get_leaders(db, team_id)]
    if (current_user.id not in team_leaders):
        raise HTTPException(
            status_code=403,
            detail = "Only team leaders can add members"
        )
    return crud.add_member(db, team_id, member)

@router.get("/", response_model=list[schemas.TeamMemberResponse])
def get_members(team_id : int, db : Session = Depends(get_db)):
    return crud.get_members(db, team_id)

@router.get("/{user_id}", response_model=schemas.TeamMemberResponse)
def get_member(team_id : int, user_id : int, db : Session = Depends(get_db)):
    return crud.get_member(db, team_id, user_id)

@router.patch("/{user_id}", response_model = schemas.TeamMemberResponse)
def update_member(team_id : int, user_id : int,
                  update : schemas.TeamMemberUpdate,
                  current_user : models.User = Depends(get_current_user),
                  db : Session = Depends(get_db)):
    team_leaders = [leader.user_id for leader in crud.get_leaders(db, team_id)]
    if (current_user.id not in team_leaders):
        raise HTTPException(
            status_code=403,
            detail = "Only team leaders can change member roles"
        )
    if (len(team_leaders) == 1 and user_id == current_user.id and update.role == models.TeamRole.MEMBER):
        raise HTTPException(
            status_code=409,
            detail = "A team cannot have zero leaders"
        )
    return crud.update_member(db, team_id, user_id, update)

@router.delete("/{user_id}")
def remove_member(team_id : int,
                  user_id : int,
                  current_user : models.User = Depends(get_current_user),
                  db : Session = Depends(get_db)):
    team_leaders = [leader.user_id for leader in crud.get_leaders(db, team_id)]
    if (current_user.id not in team_leaders):
        raise HTTPException(
            status_code=403,
            detail = "Only team leaders can remove members"
        )
    if (len(team_leaders) == 1 and user_id == current_user.id):
        raise HTTPException(
            status_code=409,
            detail = "A team cannot have zero leaders"
        )
    crud.remove_member(db, team_id, user_id)
    return {
        "message" : "Member Removed Succesfully"
    }
