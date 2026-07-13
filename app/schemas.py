from pydantic import BaseModel
from datetime import datetime
from app.models import TeamRole, TaskStatus, TaskPriority

class UserCreate(BaseModel):
    name : str
    email : str
    password : str
    
class UserResponse(BaseModel):
    id : int
    name : str
    email : str
    created_at : datetime
    model_config = {
        "from_attributes" : True
    }
    
class UserUpdate(BaseModel):
    name : str | None = None
    email : str | None = None
    password : str | None = None
    
class UserLogin(BaseModel):
    email : str
    password : str
    
class Token(BaseModel):
    access_token : str
    token_type : str
    
class TeamCreate(BaseModel):
    name : str  
    
class TeamResponse(BaseModel):
    team_id : int
    name : str
    created_at : datetime
    model_config ={
        "from_attributes" : True
    }
    
class TeamUpdate(BaseModel):
    name : str | None = None
    
class TeamMemberCreate(BaseModel):
    user_id : int
    role : TeamRole

class TeamMemberResponse(BaseModel):
    team_id : int
    user_id : int
    role : TeamRole
    joined_at : datetime
    model_config = {
        "from_attributes" : True
    }
    
class TeamMemberUpdate(BaseModel):
    role : TeamRole | None=None
    
class ProjectCreate(BaseModel):
    name : str
    
class ProjectResponse(BaseModel):
    id : int
    team_id : int
    name : str
    created_at : datetime
    model_config = {
        "from_attributes" : True
    }
    
class ProjectUpdate(BaseModel):
    name : str | None=None
    
class TaskCreate(BaseModel):
    title : str
    description : str
    priority : TaskPriority
    due_date : datetime

class TaskUpdate(BaseModel):
    title : str | None = None
    description : str | None = None
    status : TaskStatus | None = None
    priority : TaskPriority | None = None
    due_date : datetime | None = None
    
class TaskResponse(BaseModel):
    id : int
    project_id : int
    title : str
    description : str
    status : TaskStatus
    priority : TaskPriority
    due_date : datetime
    created_by : int
    created_at : datetime
    model_config = {
        "from_attributes" : True
    }
    
class TaskAssignmentCreate(BaseModel):
    user_id : int

class TaskAssignmentResponse(BaseModel):
    task_id : int
    user_id : int
    assigned_at : datetime
    model_config = {
        "from_attributes" : True
    }
    
class CommentCreate(BaseModel):
    content : str
    
class CommentUpdate(BaseModel):
    content : str | None = None
    
class CommentResponse(BaseModel):
    id : int
    task_id : int
    author_id : int
    content : str
    created_at : datetime
    model_config = {
        "from_attributes" : True
    }
    
    

    
    