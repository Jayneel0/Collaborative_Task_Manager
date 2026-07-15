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
    crud.get_member(db, team_id, current_user.id)
    return crud.create_comment(db, team_id, project_id, task_id, current_user.id, comment)

@router.get("/", response_model=list[schemas.CommentResponse])
def get_comments(team_id : int, project_id : int, task_id : int,
                 current_user : models.User = Depends(get_current_user),
                 db : Session = Depends(get_db)):
    crud.get_member(db, team_id, current_user.id)
    return crud.get_comments(db, team_id, project_id, task_id)

@router.get("/{comment_id}", response_model=schemas.CommentResponse)
def get_comment(team_id : int, project_id : int, task_id: int, comment_id : int,
                current_user : models.User = Depends(get_current_user),
                db : Session = Depends(get_db)):
    crud.get_member(db, team_id, current_user.id)
    return crud.get_comment(db, team_id, project_id, task_id, comment_id)

@router.patch("/{comment_id}", response_model = schemas.CommentResponse)
def update_comment(team_id : int, project_id : int, task_id : int, comment_id : int,
                  update : schemas.CommentUpdate,
                  current_user : models.User = Depends(get_current_user),
                  db : Session = Depends(get_db)):
    comment = crud.get_comment(db, team_id, project_id, task_id, comment_id)
    member = crud.get_member(db, team_id, current_user.id)
    if (member.user_id != comment.author_id):
        raise HTTPException(
            status_code=403,
            detail="Only the comment author can update a comment"
        )
    return crud.update_comment(db, team_id, project_id, task_id, comment_id, update)

@router.delete("/{comment_id}")
def delete_comment(team_id : int, project_id : int, task_id :int, comment_id : int,
                  current_user : models.User = Depends(get_current_user),
                  db : Session = Depends(get_db)):
    comment = crud.get_comment(db, team_id, project_id, task_id, comment_id)
    member = crud.get_member(db, team_id, current_user.id)
    if (member.user_id != comment.author_id):
        raise HTTPException(
            status_code=403,
            detail="Only the comment author can delete a comment"
        )
    crud.delete_comment(db, team_id, project_id, task_id, comment_id)
    return {
        "message" : "Comment Deleted Successfully"
    }