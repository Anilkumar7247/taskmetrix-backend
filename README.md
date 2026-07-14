# TaskFlow 🚀

**Production‑Grade Backend‑Only Task Management System**

This repository contains the complete backend for **TaskFlow**, a task management system built using Django, Django REST Framework, PostgreSQL, Redis, Celery, JWT, and Docker.

---

## 🧠 Why TaskFlow?

TaskFlow is designed to reflect how **real SaaS backends** are built and maintained:

* Explicit API design using `APIView` (no magic ViewSets)
* Role‑Based Access Control (RBAC)
* Asynchronous processing with Celery
* Redis for caching & rate limiting
* Production‑safe Docker setup
* Clean separation of concerns (apps, services, permissions, common infra)

---

## 🏗️ System Architecture (High Level)

```
Client (Web / Mobile)
        |
        |  HTTPS + JWT
        v
+----------------------+
| Django REST API      |
| (APIView, RBAC)     |
+----------------------+
        |
        | Business Logic
        v
+----------------------+
| Service Layer        |
+----------------------+
   |              |
   |              |
   v              v
PostgreSQL         Redis
(Source of Truth) (Cache, Rate Limit)
        |
        v
+----------------------+
| Celery Workers       |
| (Emails, Events)    |
+----------------------+
```

---

## ⚙️ Tech Stack

* **Language**: Python 3.12
* **Framework**: Django 5.2, Django REST Framework
* **Auth**: JWT (SimpleJWT)
* **Database**: PostgreSQL
* **Cache / Broker**: Redis
* **Async Jobs**: Celery
* **Server**: Gunicorn
* **Containerization**: Docker & Docker Compose

---

## 📁 Project Structure

```
taskflow/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
│
├── taskflow/              # Core config
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   ├── asgi.py
│   └── wsgi.py
│
├── common/                # Shared infrastructure
│   ├── redis_client.py
│   ├── cache.py
│   ├── rate_limit.py
│   ├── pagination.py
│   └── responses.py
│
├── accounts/              # Auth & users
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   └── urls.py
│
├── projects/              # Projects domain
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── services.py
│   ├── views.py
│   └── urls.py
│
├── tasks/                 # Tasks domain
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── services.py
│   ├── tasks.py           # Celery jobs
│   ├── views.py
│   └── urls.py
```

---

## 🔐 Authentication & Authorization

* JWT‑based authentication
* Stateless and scalable
* Role‑Based Access Control (RBAC)

### User Roles

| Role    | Capabilities                   |
| ------- | ------------------------------ |
| Admin   | Full access                    |
| Manager | Create & manage projects/tasks |
| Member  | Work on assigned tasks         |

Object‑level permissions ensure:

* Only owners / assignees can modify tasks
* Only admins/managers can create projects & tasks

---

## 🔄 Task Workflow Engine

Supported status flow:

```
TODO → IN_PROGRESS → DONE
```

Rules enforced in the **service layer**:

* Invalid transitions are rejected
* Status changes are auditable
* Side effects (notifications/emails) are async

---

## ⚡ Performance & Scalability

### Redis is used for:

* API rate limiting
* Caching task lists
* Celery message broker

### Pagination & Filtering

* Consistent pagination across APIs
* Filtering by task status
* Optimized queryset handling

---

## 🧵 Asynchronous Processing (Celery)

Background jobs handled asynchronously:

* Task notifications
* Email alerts
* Retry‑safe execution

Celery workers run independently from API requests, keeping response times low.

---

## 📡 API Overview

### Authentication

* `POST /api/auth/login/`
* `POST /api/auth/refresh/`

### Accounts

* `GET /api/accounts/profile/`
* `GET /api/accounts/users/` (admin)

### Projects

* `GET /api/projects/`
* `POST /api/projects/`
* `PUT /api/projects/{id}/`
* `DELETE /api/projects/{id}/` (archive)

### Tasks

* `GET /api/tasks/`
* `POST /api/tasks/`
* `PUT /api/tasks/{id}/`
* `POST /api/tasks/{id}/status/`
* `POST /api/tasks/{id}/comments/`

---

## 🐳 Docker Setup

### Run the project

```
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Services:

* Django API
* PostgreSQL
* Redis
* Celery Worker

---

## 🧪 Engineering Principles Used

* Thin views, fat services
* Explicit APIViews (no magic)
* Centralized business rules
* Strong permission boundaries
* Async‑first mindset
* Production‑safe defaults

---

**Author**: Senior Backend Engineer (Python / Django)
