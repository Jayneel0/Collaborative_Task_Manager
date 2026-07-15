# ENGINEERING_DECISIONS.md

# Engineering Decisions

## 1. Project Structure

### Architecture

The project follows a layered architecture to separate responsibilities across different parts of the application.

```
Client
      │
      ▼
Routers (API Endpoints)
      │
      ▼
CRUD / Business Logic
      │
      ▼
SQLAlchemy Models
      │
      ▼
Database
```

### Folder Structure

```
app/
├── routers/
├── crud.py
├── database.py
├── models.py
├── schemas.py
├── security.py
└── main.py
```

### Why this structure?

- Routers only handle HTTP requests and responses.
- CRUD contains all database operations and business logic.
- Models define the database schema.
- Schemas validate requests and responses using Pydantic.
- Security centralizes authentication and authorization logic.
- Database configuration is isolated from the rest of the application.

Separating responsibilities improves readability, maintainability, and allows each component to evolve independently.

### Why FastAPI?

FastAPI was chosen because it provides:

- Automatic request validation using Pydantic
- Automatic OpenAPI and Swagger documentation
- High performance through ASGI
- Native support for dependency injection
- Clean integration with SQLAlchemy
- Excellent developer experience

For a REST API with authentication and RBAC, FastAPI offers a good balance between simplicity and production-ready features.

---

# 2. Database Design

The application models a collaborative task management system.

## Entities

- User
- Team
- TeamMember
- Project
- Task
- TaskAssignment
- Comment

## Relationships

```
User
 │
 ├────< TeamMember >──── Team
 │
 ├────< TaskAssignment >──── Task
 │
 ├───────────────┐
 │               │
 ▼               ▼
Comment       Created Tasks

Team
 │
 ▼
Project
 │
 ▼
Task
 │
 ▼
Comment
```

### Design Decisions

**TeamMember**

A separate TeamMember table was used instead of storing team IDs inside the User model because:

- A user can belong to multiple teams.
- Each membership has its own role.
- Membership contains additional information such as joined_at.

This naturally forms a many-to-many relationship.

---

**TaskAssignment**

Tasks can be assigned to multiple users.

Instead of storing a single assigned user inside the Task table, a junction table was created.

Benefits:

- Supports multiple assignees.
- Easier future expansion.
- Keeps the schema normalized.

---

**Projects**

Projects belong to exactly one team.

Tasks belong to exactly one project.

This hierarchy keeps authorization straightforward while maintaining clear ownership.

---

### Indexing

Primary keys and unique constraints are automatically indexed by PostgreSQL.

Additional indexes were not added because the expected dataset for this project is relatively small.

If scaled further, indexes would likely be added on:

- User email
- Task status
- Task priority
- Project team_id
- Task project_id

---

# 3. Authentication

JWT authentication was chosen.

### Why JWT?

- Stateless authentication.
- No server-side session storage.
- Easy integration with REST APIs.
- Works well with frontend clients and mobile applications.

### Token Strategy

After successful login:

- Password is verified.
- A JWT is generated.
- The token contains the user ID (`sub` claim).
- The token includes an expiration time.

Protected endpoints retrieve the current user by decoding the JWT.

### Logout

JWT is inherently stateless.

To support logout, a token blacklist is maintained.

Blacklisted tokens are rejected even if they have not expired.

This solution is suitable for the scope of this project.

### Security Considerations

- Passwords are hashed using Argon2 through pwdlib.
- Plain text passwords are never stored.
- JWT expiration limits token lifetime.
- Environment variables store secrets instead of hardcoding them.

---

# 4. Authorization

Authorization is implemented using Role-Based Access Control (RBAC).

## Roles

- Owner
- Maintainer
- Member
- Viewer

### Permissions

### Owner

- Full team control
- Manage members
- Change member roles
- Create/Edit/Delete projects
- Create/Delete tasks
- Assign tasks

### Maintainer

- Create/Edit/Delete projects
- Create tasks
- Delete tasks
- Assign tasks
- Invite members

### Member

- View projects
- View tasks
- Create tasks
- Update assigned tasks
- Add comments

### Viewer

- View projects
- View tasks
- Add comments

### Enforcement

Authorization is enforced before every protected operation.

Permission helper functions verify the current user's role within the requested team before allowing the operation.

This ensures that authorization is enforced by the backend rather than relying on frontend restrictions.

---

# 5. Problems Faced

## Authentication

Initially, JWT authentication was implemented without logout support.

A token blacklist was introduced to invalidate tokens after logout.

---

## Relationship Mapping

Multiple relationships between User and Task initially caused ambiguity.

Separate relationships were introduced for:

- Task creator
- Task assignments

This made the ORM mapping clearer.

---

## Role Management

Ensuring that only authorized users could perform sensitive actions required multiple iterations.

RBAC checks were gradually centralized into helper functions to reduce duplication.

---

## Docker Deployment

The application initially failed to connect to PostgreSQL because SQLite configuration was still being used.

The project was updated to load the database URL from environment variables, allowing both local development and deployment without changing the code.

---

## Render Deployment

The deployment initially failed due to missing environment variables and incorrect database configuration.

Using Render's managed PostgreSQL database together with environment variables resolved the issue.

---

# 6. Tradeoffs

## JWT instead of Sessions

JWT was chosen because:

- Easier to scale.
- No server-side session storage.
- Better suited for REST APIs.

A blacklist was added to support logout despite JWT being stateless.

---

## PostgreSQL over MongoDB

The application contains many structured relationships:

- Teams
- Projects
- Tasks
- Members
- Assignments

A relational database naturally models these relationships using foreign keys and junction tables.

SQLAlchemy also integrates well with PostgreSQL.

---

## SQLAlchemy ORM instead of Raw SQL

The ORM was chosen because it:

- Reduces boilerplate SQL.
- Improves maintainability.
- Makes relationships easier to express.
- Helps prevent SQL injection through parameterized queries.

---

## SQLite for Development

SQLite was used during initial development because it requires no setup and allows rapid iteration.

The deployment uses PostgreSQL for better production compatibility.

---

## No Redis

Token blacklisting is currently stored in memory.

Redis was intentionally omitted to keep the project simple and reduce deployment complexity.

For a production-scale application, Redis would be the preferred solution.

---

# Future Improvements

If additional development time were available, the following improvements would be implemented:

- Automated unit and integration tests using Pytest
- Alembic database migrations
- Redis-backed token blacklist
- File attachments
- Notifications
- Activity logs
- Email verification
- Password reset
- Rate limiting using Redis
- Background jobs using Celery
- WebSocket support for live collaboration
- Improved monitoring and observability