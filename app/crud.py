from sqlalchemy.orm import Session
from app import schemas, models
from datetime import datetime, UTC
from fastapi import HTTPException
from app.security import hash_password

def create_user(db : Session, user : schemas.UserCreate):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )
        
    db_user = models.User(
        name = user.name,
        email = user.email,
        hashed_password = hash_password(user.password),
        created_at = datetime.now(UTC)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
def get_users(db : Session):
    return db.query(models.User).all()

def get_user(db : Session, user_id : int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code = 404,
            detail = "User Not Found"
        )
    return user

def update_user(db : Session, user_id : int, update : schemas.UserUpdate):
    user = get_user(db, user_id)
    if update.name is not None :
        user.name = update.name
    if update.email is not None:
        user.email = update.email
    if update.password is not None:
        user.hashed_password = hash_password(update.password)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db : Session, user_id : int):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    
def get_user_by_email(db : Session, email : str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_team(db : Session, team : schemas.TeamCreate):
    existing_team = db.query(models.Team).filter(models.Team.name == team.name).first()
    if existing_team:
        raise HTTPException(
            status_code=409,
            detail = "Team already registered"
        )
    db_team = models.Team(
        name = team.name
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_team(db : Session, team_id : int):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if team is None:
        raise HTTPException(
            status_code = 404,
            detail = "Team Not Found"
        )
    return team

def get_teams(db : Session):
    return db.query(models.Team).all()

def update_team(db : Session, team_id : int, update : schemas.TeamUpdate):
    team = get_team(db, team_id)
    team.name = update.name
    db.commit()
    db.refresh(team)
    return team

def delete_team(db : Session, team_id : int):
    team = get_team(db, team_id)
    db.delete(team)
    db.commit()

def add_member(db : Session, team_id : int, member : schemas.TeamMemberCreate):
    team = get_team(db, team_id)
    user = get_user(db, member.user_id)
    existing_member = db.query(models.TeamMember).filter(models.TeamMember.team_id == team_id,
                                             models.TeamMember.user_id == member.user_id).first()
    if existing_member is not None:
        raise HTTPException(
            status_code=409,
            detail = "Member already exists"
        )
    db_member = models.TeamMember(
        team_id = team_id,
        user_id = member.user_id,
        role = member.role
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_members(db : Session, team_id : int):
    team = get_team(db, team_id)
    return db.query(models.TeamMember).filter(models.TeamMember.team_id == team_id).all()

def get_member(db : Session, team_id : int, user_id : int):
    team = get_team(db, team_id)
    member = db.query(models.TeamMember).filter(models.TeamMember.team_id == team_id,
                                             models.TeamMember.user_id == user_id).first()
    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Team does not have this member"
        )
    return member

def get_leaders(db : Session, team_id : int):
    team = get_team(db, team_id)
    leaders = db.query(models.TeamMember).filter(models.TeamMember.team_id == team_id,
                                             models.TeamMember.role == models.TeamRole.LEADER).all()
    return leaders

def remove_member(db : Session, team_id : int, user_id : int):
    team_member = get_member(db, team_id, user_id)
    db.delete(team_member)
    db.commit()
    
def update_member(db : Session, team_id : int, user_id : int, update : schemas.TeamMemberUpdate):
    member = get_member(db, team_id, user_id)
    member.role = update.role
    db.commit()
    db.refresh(member)
    return member

def create_project(db : Session, team_id : int, project : schemas.ProjectCreate):
    team = get_team(db, team_id)
    db_project = models.Project(
        team_id = team_id,
        name = project.name
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_project(db : Session, team_id : int, project_id : int):
    team = get_team(db, team_id)
    project = db.query(models.Project).filter(models.Project.team_id == team_id,
                                              models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Team does not have this project"
        )
    return project

def get_projects(db : Session, team_id : int):
    team = get_team(db, team_id)
    return db.query(models.Project).filter(models.Project.team_id == team_id).all()

def update_project(db : Session, team_id : int, project_id : int, update : schemas.ProjectUpdate):
    project = get_project(db, team_id, project_id)
    if update.name is not None:
        project.name = update.name
    db.commit()
    db.refresh(project)
    return project

def delete_project(db : Session, team_id : int, project_id : int):
    project = get_project(db, team_id, project_id)
    db.delete(project)
    db.commit()
    
def create_task(db : Session, team_id : int, project_id : int, task : schemas.TaskCreate,
                current_user_id : int):
    get_project(db, team_id, project_id)
    db_task = models.Task(
        project_id = project_id,
        title = task.title,
        description = task.description,
        priority = task.priority,
        due_date = task.due_date,
        created_by = current_user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db : Session, team_id : int, project_id : int, task_id : int):
    get_project(db, team_id, project_id)
    task = db.query(models.Task).filter(models.Task.project_id == project_id,
                                        models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Project does not have this task"
        )
    return task

def get_tasks(db : Session, team_id : int, project_id : int):
    get_project(db, team_id, project_id)
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()

def update_task(db : Session, team_id : int, project_id : int,
                task_id : int, update : schemas.TaskUpdate):
    task = get_task(db, team_id, project_id, task_id)
    if update.title is not None :
        task.title = update.title
    if update.description is not None:
        task.description = update.description
    if update.status is not None:
        task.status = update.status
    if update.priority is not None:
        task.priority = update.priority
    if update.due_date is not None:
        task.due_date = update.due_date
    db.commit()
    db.refresh(task)
    return task

def delete_task(db : Session, team_id : int, project_id : int, task_id : int):
    task = get_task(db, team_id, project_id, task_id)
    db.delete(task)
    db.commit()

def assign_user(db : Session, team_id : int, project_id : int, task_id:int,
                assignment : schemas.TaskAssignmentCreate):
    task = get_task(db, team_id, project_id, task_id)
    user = get_user(db, assignment.user_id)
    member = get_member(db, team_id, assignment.user_id)
    existing_assignment = db.query(models.TaskAssignment).filter(
        models.TaskAssignment.task_id==task_id,
        models.TaskAssignment.user_id==assignment.user_id).first()
    if existing_assignment is not None:
        raise HTTPException(
            status_code=409,
            detail="User already assigned to this task."
        )
    db_assignment = models.TaskAssignment(
        task_id = task_id,
        user_id = assignment.user_id
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def get_assignment(db : Session, team_id : int, project_id : int, task_id:int, user_id:int):
    task = get_task(db, team_id, project_id, task_id)
    assignment = db.query(models.TaskAssignment).filter(
        models.TaskAssignment.task_id == task_id, models.TaskAssignment.user_id == user_id
    ).first()
    if assignment is None:
        raise HTTPException(
            status_code=404,
            detail="User is not assigned to this task"
        )
    return assignment

def get_assignments(db : Session, team_id : int, project_id : int, task_id:int):
    task = get_task(db, team_id, project_id, task_id)
    assignments = db.query(models.TaskAssignment).filter(models.TaskAssignment.task_id == task_id).all()
    return assignments

def remove_assignment(db : Session, team_id : int, project_id : int,
                      task_id:int, user_id: int):
    assignment = get_assignment(db, team_id, project_id, task_id, user_id)
    db.delete(assignment)
    db.commit()
    
def create_comment(db : Session, team_id : int, project_id : int, task_id : int,
                   current_user_id : int, comment : schemas.CommentCreate):
    task = get_task(db, team_id, project_id, task_id)
    
    db_comment = models.Comment(
        task_id = task_id,
        author_id = current_user_id,
        content = comment.content
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(db : Session, team_id : int, project_id : int, task_id:int,
                comment_id : int):
    task = get_task(db, team_id, project_id, task_id)
    comment = db.query(models.Comment).filter(
        models.Comment.task_id == task_id, models.Comment.id == comment_id
    ).first()
    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )
    return comment

def get_comments(db : Session, team_id : int, project_id : int, task_id:int):
    task = get_task(db, team_id, project_id, task_id)
    comments = db.query(models.Comment).filter(models.Comment.task_id == task_id).all()
    return comments

def update_comment(db : Session, team_id : int, project_id : int,
                   task_id : int, comment_id : int, update : schemas.CommentUpdate):
    comment = get_comment(db, team_id, project_id, task_id, comment_id)
    if update.content is not None:
        comment.content = update.content
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db : Session, team_id : int, project_id : int,
                   task_id : int, comment_id : int):
    comment = get_comment(db, team_id, project_id, task_id, comment_id)
    db.delete(comment)
    db.commit()
