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
git clone <repository-url>

cd Collaborative-Task-Manager

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

Run the server:

```bash
uvicorn app.main:app --reload
```

API documentation:

```
http://127.0.0.1:8000/docs
```

## Authentication

Authentication is implemented using JWT Bearer Tokens.

Login endpoint:

```
POST /users/login
```

Use the returned access token to authorize protected endpoints.

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