from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.security import get_current_user

router = APIRouter(prefix="/teams/{team_id}/projects/{project_id}/tasks/{task_id}/comments")

@router.post("/", response_model=schemas.CommentResponse)
def create_comment(team_id : int, project_id: int, task_id : int, comment : schemas.CommentCreate,
               current_user : models.User = Depends(get_current_user),
               db : Session = Depends(get_db)):
    user = db.query(models.TeamMember).filter(models.TeamMember.team_id == team_id
                                              and models.TeamMember.user_id == current_user.id).first()
    if user is None:
        raise HTTPException(
            status_code=403,
            detail="Only team members can add comments"
        )
    return crud.create_comment(db, team_id, project_id, task_id, current_user.id, comment)

@router.get("/", response_model=list[schemas.CommentResponse])
def get_comments(team_id : int, project_id : int, task_id : int, db : Session = Depends(get_db)):
    return crud.get_comments(db, team_id, project_id, task_id)

@router.get("/{comment_id}", response_model=schemas.CommentResponse)
def get_comment(team_id : int, project_id : int, task_id: int,
                comment_id : int, db : Session = Depends(get_db)):
    return crud.get_comment(db, team_id, project_id, task_id, comment_id)

@router.patch("/{comment_id}", response_model = schemas.CommentResponse)
def update_comment(team_id : int, project_id : int, task_id : int, comment_id : int,
                  update : schemas.CommentUpdate,
                  current_user : models.User = Depends(get_current_user),
                  db : Session = Depends(get_db)):
    comment = get_comment(team_id, project_id, task_id, comment_id, db)
    team_leaders = crud.get_leaders(db, team_id)
    if (current_user.id not in team_leaders and current_user.id != comment.author_id):
        raise HTTPException(
            status_code=403,
            detail = "Only the comment author or a team leader can update comment"
        )
    return crud.update_comment(db, team_id, project_id, task_id, comment_id, update)

@router.delete("/{comment_id}")
def delete_comment(team_id : int, project_id : int, task_id :int, comment_id : int,
                  current_user : models.User = Depends(get_current_user),
                  db : Session = Depends(get_db)):
    comment = get_comment(team_id, project_id, task_id, comment_id, db)
    team_leaders = crud.get_leaders(db, team_id)
    if (current_user.id not in team_leaders and current_user.id != comment.author_id):
        raise HTTPException(
            status_code=403,
            detail = "Only the comment author or a team leader can delete comment"
        )
    crud.delete_comment(db, team_id, project_id, task_id, comment_id)
    return {
        "message" : "Comment Deleted Succesfully"
    }