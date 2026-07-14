# Collaborative Task Manager API

A backend REST API for collaborative task management built using FastAPI and SQLAlchemy.

## Features

- User registration and authentication using JWT
- Secure password hashing
- Team management
- Team member management with roles (Leader / Member)
- Project management
- Task management
- Task assignment
- Comments on tasks
- Role-based authorization

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- pwdlib (Argon2)

## Project Structure

```
app/
├── crud.py
├── database.py
├── models.py
├── schemas.py
├── security.py
├── routers/
│   ├── users.py
│   ├── teams.py
│   ├── team_members.py
│   ├── projects.py
│   ├── tasks.py
│   ├── task_assignments.py
│   └── comments.py
```

## Installation

```bash
git clone https://github.com/Jayneel0/Collaborative_Task_Manager.git

cd Collaborative-Task-Manager

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

Run the server:

```bash
uvicorn app.main:app --reload
```
## Environment Variables

Create a `.env` file using `.env.example` before running the project.

API documentation:

```
Interactive API documentation is available after starting the server:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
```
## API Version

Current API version:

/api/v1

## Database Schema

The application consists of the following entities:

- User
- Team
- TeamMember
- Project
- Task
- TaskAssignment
- Comment

Relationships:

- One Team → Many Projects
- One Project → Many Tasks
- One Task → Many Comments
- Many Users ↔ Many Teams (TeamMember)
- Many Users ↔ Many Tasks (TaskAssignment)


## Team Roles

The API supports role-based authorization.

- Owner
  - Full access to the team
  - Manage members
  - Change member roles
  - Create, edit and delete projects
  - Delete tasks
  - Assign tasks

- Maintainer
  - Create, edit and delete projects
  - Create tasks
  - Assign tasks
  - Delete tasks
  - Invite members

- Member
  - View projects
  - View tasks
  - Create tasks
  - Update assigned tasks
  - Comment on tasks

- Viewer
  - View projects
  - View tasks
  - Comment on tasks


## API Endpoints

### Users
- POST /users
- POST /users/login
- POST /users/logout
- GET /users/me
- GET /users/{user_id}
- PATCH /users/{user_id}
- DELETE /users/{user_id}

### Teams
- POST /teams
- GET /teams
- GET /teams/{team_id}
- PATCH /teams/{team_id}
- DELETE /teams/{team_id}

### Team Members
- POST /teams/{team_id}/members
- GET /teams/{team_id}/members
- GET /teams/{team_id}/members/{user_id}
- PATCH /teams/{team_id}/members/{user_id}
- DELETE /teams/{team_id}/members/{user_id}

### Projects
- POST /teams/{team_id}/projects
- GET /teams/{team_id}/projects
- GET /teams/{team_id}/projects/{project_id}
- PATCH /teams/{team_id}/projects/{project_id}
- DELETE /teams/{team_id}/projects/{project_id}

### Tasks
- POST /teams/{team_id}/projects/{project_id}/tasks
- GET /teams/{team_id}/projects/{project_id}/tasks
- GET /teams/{team_id}/projects/{project_id}/tasks/{task_id}
- PATCH /teams/{team_id}/projects/{project_id}/tasks/{task_id}
- DELETE /teams/{team_id}/projects/{project_id}/tasks/{task_id}

### Task Assignments
- POST /teams/{team_id}/projects/{project_id}/tasks/{task_id}/assignments
- GET /teams/{team_id}/projects/{project_id}/tasks/{task_id}/assignments
- GET /teams/{team_id}/projects/{project_id}/tasks/{task_id}/assignments/{user_id}
- DELETE /teams/{team_id}/projects/{project_id}/tasks/{task_id}/assignments/{user_id}

### Comments
- POST /teams/{team_id}/projects/{project_id}/tasks/{task_id}/comments
- GET /teams/{team_id}/projects/{project_id}/tasks/{task_id}/comments
- GET /teams/{team_id}/projects/{project_id}/tasks/{task_id}/comments/{comment_id}
- PATCH /teams/{team_id}/projects/{project_id}/tasks/{task_id}/comments/{comment_id}
- DELETE /teams/{team_id}/projects/{project_id}/tasks/{task_id}/comments/{comment_id}

## Authentication

Authentication is implemented using JWT Bearer Tokens.

Login endpoint:

```
POST /users/login
```

Use the returned access token to authorize protected endpoints.

## Authorization

Protected endpoints require a JWT Bearer Token.

After logging in, include the token in the Authorization header:

Authorization: Bearer <access_token>

## Database

SQLite is used as the database.

## Future Improvements

- Admin role
- Activity logs
- File attachments
- Notifications
- Search and filtering
- Pagination
- Environment variable configuration
