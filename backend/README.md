# Smart Event Management & Networking Platform (Backend)

This folder contains a Django-based backend for a multi-tenant university olympiad and smart event management platform.

## Tech Stack

- Django 5
- Django REST Framework (DRF)
- JWT auth via `djangorestframework-simplejwt`
- Django Channels + Redis for WebSockets
- Celery + Redis for background tasks
- PostgreSQL (via AWS RDS in production)
- AWS S3 for media storage

## Getting Started (Local)

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations and run the dev server:

```bash
python manage.py migrate
python manage.py runserver
```

By default, the project uses SQLite; set `DB_ENGINE`, `DB_NAME`, `DB_USER`, etc. to use PostgreSQL.

