from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime
from datetime import datetime, UTC
from app.database import Base
from enum import Enum
from sqlalchemy import Enum as SQLEnum, ForeignKey


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email : Mapped[str] = mapped_column(String, unique=True)
    hashed_password : Mapped[str] = mapped_column(String)
    created_at : Mapped[datetime] = mapped_column(DateTime)
    
    memberships : Mapped[list["TeamMember"]] = relationship(back_populates="user",
                                                            cascade="all, delete-orphan")
    tasks : Mapped[list["TaskAssignment"]] = relationship(back_populates="user",
                                                          cascade="all, delete-orphan")
    comments : Mapped[list["Comment"]] = relationship(back_populates="author",
                                                      cascade="all, delete-orphan")
    created_tasks : Mapped[list["Task"]] = relationship(back_populates="creator")
    
class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    created_at : Mapped[datetime]= mapped_column(DateTime, default=lambda: datetime.now(UTC))
    memberships : Mapped[list["TeamMember"]] = relationship(back_populates="team",
                                                            cascade="all, delete-orphan")
    projects : Mapped[list["Project"]]=relationship(back_populates="team",
                                                    cascade = "all, delete-orphan")

class TeamRole(Enum):
    OWNER = "leader"
    MAINTAINER = "maintainer"
    MEMBER = "member"
    VIEWER = "viewer"
    
class TeamMember(Base):
    __tablename__ = "team_members"    
    
    team_id : Mapped[int] = mapped_column(ForeignKey("teams.id"), primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role : Mapped[TeamRole] = mapped_column(SQLEnum(TeamRole), default = TeamRole.MEMBER)
    joined_at : Mapped[datetime] = mapped_column(DateTime, default = lambda: datetime.now(UTC))
    team : Mapped["Team"] = relationship(back_populates="memberships")
    user : Mapped["User"] = relationship(back_populates="memberships")
    
class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id : Mapped[int] = mapped_column(ForeignKey("teams.id"))
    name: Mapped[str] = mapped_column(String)
    created_at : Mapped[datetime]= mapped_column(DateTime, default= lambda: datetime.now(UTC))
    team : Mapped["Team"] = relationship(back_populates="projects")
    tasks : Mapped[list["Task"]] = relationship(back_populates="project",
                                                cascade="all, delete-orphan")

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id : Mapped[int] = mapped_column(ForeignKey("projects.id"))
    title : Mapped[str] = mapped_column(String)
    description : Mapped[str] = mapped_column(String)
    status : Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default = TaskStatus.TODO)
    priority : Mapped[TaskPriority] = mapped_column(SQLEnum(TaskPriority))
    due_date : Mapped[datetime] = mapped_column(DateTime)
    created_by : Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at : Mapped[datetime]= mapped_column(DateTime, default= lambda : datetime.now(UTC))
    project : Mapped["Project"] = relationship(back_populates="tasks")
    creator : Mapped["User"] = relationship(back_populates="created_tasks")
    assignments : Mapped[list["TaskAssignment"]] = relationship(back_populates="task",
                                                                cascade="all, delete-orphan")
    comments : Mapped[list["Comment"]] = relationship(back_populates="task",
                                                      cascade="all, delete-orphan")
    
class TaskAssignment(Base):
    __tablename__ = "task_assignments"
    
    task_id : Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    assigned_at : Mapped[datetime] = mapped_column(DateTime, default= lambda : datetime.now(UTC))
    task : Mapped["Task"] = relationship(back_populates="assignments")
    user : Mapped["User"] = relationship(back_populates="tasks")

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id : Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    author_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    content : Mapped[str] = mapped_column(String)
    created_at : Mapped[datetime]= mapped_column(DateTime, default= lambda : datetime.now(UTC))
    task : Mapped["Task"] = relationship(back_populates="comments")
    author : Mapped["User"] = relationship(back_populates="comments")