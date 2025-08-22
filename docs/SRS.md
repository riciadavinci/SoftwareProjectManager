# Software Requirements Specification (SRS)

**Project Name:** Software Project Manager (SPM)

**Prepared by:** Rishikesh Arunkumar Nerurkar

**Date:** 22-Aug-2025

---

## 1. Introduction

### 1.1 Purpose

The purpose of this document is to specify the requirements for the **Software Project Manager (SPM)** web application, which allows software teams to manage projects, tasks, and resources in a structured and collaborative manner. The system will support multiple user roles, provide task tracking, and integrate project resources.

### 1.2 Scope

SPM is a web-based project management tool, similar to Jira, designed for software development teams. The system will allow:

* Project creation and management.
* Task creation, assignment, and tracking.
* Resource management.
* Role-based access control (Admin, Project Manager, Developer).
* Kanban-style task visualization for developers.
* Tagging tasks for categorization.

### 1.3 Definitions, Acronyms, and Abbreviations

* **SPM:** Software Project Manager
* **PM:** Project Manager
* **Dev:** Developer
* **Kanban Board:** Task visualization using columns representing status (TODO, WIP, Done).

### 1.4 References

* Python 3.x
* Flask / Flask-Restful
* SQLAlchemy ORM
* Flask-WTForms for form validation
* JWT for authentication
* HTML, CSS, JavaScript, Bootstrap 5 for UI

---

## 2. Overall Description

### 2.1 Product Perspective

SPM will be a standalone web application with a RESTful backend and a responsive frontend. It will interact with a relational database (PostgreSQL or SQLite for development).

**Entity Relationships:**

* **User** ↔ **UserRole** (Many-to-One)
* **SoftwareProject** ↔ **User** (Many-to-Many via `members`)
* **SoftwareProject** ↔ **Task** (One-to-Many)
* **Task** ↔ **TaskStatus** (Many-to-One)
* **Task** ↔ **User** (creator, assignor, developer)
* **Task** ↔ **Tag** (Many-to-Many)
* **SoftwareProject** ↔ **ProjectResource** (One-to-Many)
* **ProjectResource** ↔ **ResourceType** (Many-to-One)

### 2.2 User Classes and Characteristics

| Role            | Permissions                                           | Views                                                       |
| --------------- | ----------------------------------------------------- | ----------------------------------------------------------- |
| Admin           | CRUD Users & Roles, CRUD Projects, Assign PMs         | Dashboard with all projects & users                         |
| Project Manager | CRUD Tasks, Assign Tasks, CRUD Project Resources      | Project Dashboard, Task Kanban (full status), Resource List |
| Developer       | View assigned Tasks, Update Task Status, Add Comments | 3-Bucket Kanban Board (TODO, WIP, Done)                     |

### 2.3 Operating Environment

* Backend: Flask RESTful API, Python 3.10+
* Frontend: HTML5, CSS3, JavaScript, Bootstrap 5, Jinja Templates
* Database: PostgreSQL / SQLite
* Authentication: JWT tokens
* Deployment: Docker optional, Linux/Windows compatible

### 2.4 Design & Implementation Constraints

* REST API endpoints must be secured using JWT.
* All sensitive data (passwords) must be hashed using bcrypt or equivalent.
* Project data must enforce referential integrity via foreign keys.
* Responsive design for desktop and tablet use.

### 2.5 Assumptions and Dependencies

* Users are registered and assigned roles before accessing the system.
* Developers may work on multiple projects concurrently.
* Project resources can include links, documents, or other external media.

---

## 3. Functional Requirements

### 3.1 User Management

* **FR1.1:** Admin can create, read, update, delete users.
* **FR1.2:** Admin can assign roles to users.
* **FR1.3:** Passwords must be stored securely.
* **FR1.4:** Users can update personal details.

### 3.2 Project Management

* **FR2.1:** Admin and PMs can create projects.
* **FR2.2:** Projects contain members (users), tasks, resources, and repository links.
* **FR2.3:** PM can add/remove members to/from projects.
* **FR2.4:** Project details (description, repo links) can be updated.

### 3.3 Task Management

* **FR3.1:** PM can create tasks under a project (status default: Backlog).
* **FR3.2:** PM can assign tasks to developers.
* **FR3.3:** Task fields: name, description, status, creator, assignor, developer, tags.
* **FR3.4:** Developers can update task status (TODO → WIP → Done).
* **FR3.5:** Tasks can have multiple tags.

### 3.4 Task Status

* **FR4.1:** TaskStatus options: Backlog, TODO, WIP, Done, Archive, Cancelled.
* **FR4.2:** Developer sees only TODO, WIP, Done buckets on Kanban.

### 3.5 Tags

* **FR5.1:** Tags: Feature, Bug-fix, Document, Test, etc.
* **FR5.2:** PM can assign tags to tasks.

### 3.6 Project Resources

* **FR6.1:** PM can add resources to a project.
* **FR6.2:** Resource fields: name, link (optional), resource type.
* **FR6.3:** ResourceType: Book, Youtube Video, Youtube Playlist, Online Documentation, Research Paper, Journal Article, Web Article.

### 3.7 Kanban Board

* **FR7.1:** Developer sees assigned tasks in a 3-bucket board (TODO, WIP, Done).
* **FR7.2:** PM can see all tasks in full status columns.
* **FR7.3:** Drag-and-drop support for task status updates (optional for future enhancement).

### 3.8 Authentication & Security

* **FR8.1:** JWT-based authentication for all endpoints.
* **FR8.2:** Role-based access control enforced on all CRUD operations.
* **FR8.3:** Password hashing and optional 2FA in future versions.

---

## 4. Non-functional Requirements

### 4.1 Performance

* API should respond within 200ms for normal queries.
* Kanban board should load all tasks within 1 second for <100 tasks.

### 4.2 Reliability

* Database must ensure ACID compliance.
* JWT tokens expire after configurable duration.

### 4.3 Usability

* Responsive UI using Bootstrap 5.
* Intuitive dashboard for PMs and developers.

### 4.4 Maintainability

* Modular backend structure (Flask Blueprints for Users, Projects, Tasks, Resources).
* Unit tests using pytest and coverage >80%.

### 4.5 Scalability

* Support multiple projects, users, and tasks without significant performance degradation.
* RESTful API allows future migration to microservices.

---

## 5. Suggestions / Thoughts

1. **Task Comments:** Consider adding a comments feature for tasks for collaboration.
2. **Activity Log:** Maintain an audit log for task assignments and status updates.
3. **Notifications:** Optional email/real-time notifications for task assignments or updates.
4. **Repository Integration:** Optionally link GitHub/GitLab repositories to projects for auto-updating tasks from commits/issues.
5. **Search & Filters:** Implement search by project, task, tag, or user.
6. **Tags for Developers:** Consider allowing developers to add personal labels or “sub-tags” for easier filtering.
7. **Kanban Enhancements:** Drag-and-drop task movement with real-time backend updates.

---

## 6. Data Model (Summary)

**Tables and Relationships:**

```
User(id, role_id, email, password_hash, name, date_of_birth)
UserRole(id, name)

SoftwareProject(id, name, description)
ProjectMembers(project_id, user_id)   // Many-to-Many
ProjectRepositories(project_id, link)
ProjectResources(id, project_id, name, link, resource_type_id)

Task(id, name, description, task_status_id, software_project_id, creator_id, assignor_id, developer_id)
TaskTags(task_id, tag_id)  // Many-to-Many

TaskStatus(id, name)
Tag(id, name)
ResourceType(id, name)
```


