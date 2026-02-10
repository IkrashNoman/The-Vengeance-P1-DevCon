# Quick Start Guide - Backend Setup

## Getting Started with the Vengeance Platform Backend

This guide will help you get the backend up and running quickly.

---

## Prerequisites

- Python 3.10+
- pip (Python package manager)
- PostgreSQL or SQLite (for development)
- Git

---

## Step 1: Environment Setup

### 1.1 Clone the Repository
```bash
git clone <repository-url>
cd The-Vengeance-P1-DevCon/backend
```

### 1.2 Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 1.4 Create .env File
```bash
# Create .env file in backend directory
cat > .env << EOF
# Database
DATABASE_URL=sqlite:///db.sqlite3
# Or for PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/olympiad_db

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256

# Groq API (for Chatbot)
GROQ_API_KEY=your-groq-api-key-here

# Email Settings (Optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EOF
```

### Get Groq API Key
1. Visit https://console.groq.com/
2. Sign up/Log in
3. Create an API key
4. Copy the key to .env as GROQ_API_KEY

---

## Step 2: Database Setup

### 2.1 Run Migrations
```bash
python manage.py migrate
```

### 2.2 Create Superuser
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 2.3 Load Sample Data (Optional)
```bash
# Create sample data
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> # Create test users
```

---

## Step 3: Start Development Server

### 3.1 Run Server
```bash
python manage.py runserver
```

Server will be available at `http://localhost:8000`

### 3.2 Access Admin Panel
```
URL: http://localhost:8000/admin/
Username: (your superuser username)
Password: (your superuser password)
```

---

## Step 4: Initialize Chatbot

### 4.1 Rebuild Knowledge Base
```bash
curl -X POST http://localhost:8000/api/chatbot/kb/rebuild_knowledge_base/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

Or use Django shell:
```bash
python manage.py shell
>>> from chatbot.services import initialize_chatbot_with_defaults
>>> initialize_chatbot_with_defaults()
>>> exit()
```

---

## Step 5: Test Endpoints

### 5.1 Using curl
```bash
# Get dashboard
curl -X GET http://localhost:8000/api/admin/organizer/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN"

# Create event
curl -X POST http://localhost:8000/api/admin/organizer/events \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Event",
    "description": "Test Description",
    "startDate": "2026-03-15",
    "endDate": "2026-03-16"
  }'
```

### 5.2 Using Postman
1. Import collection from `postman_collection.json`
2. Set Bearer token in Authorization tab
3. Test endpoints

---

## Step 6: Frontend Integration

### 6.1 Configure CORS (for frontend development)
Update `backend/event_platform/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React development server
    "http://127.0.0.1:3000",
    "https://yourdomain.com",
]
```

### 6.2 Frontend API Base URL
Configure in frontend `.env`:
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_BACKEND_URL=http://localhost:8000
```

---

## Project Structure

```
backend/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3               # SQLite database (dev)
│
├── event_platform/          # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                # User authentication
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── events/                  # Event management
│   ├── models.py           # Event, TicketType, EventSession
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── chatbot/                 # AI Chatbot
│   ├── models.py           # ChatbotKnowledgeBase, Conversation
│   ├── views.py
│   ├── services.py         # ChatbotService (RAG)
│   ├── serializers.py
│   └── urls.py
│
├── networking/              # Attendee Matching
│   ├── models.py           # NetworkProfile, Connection
│   ├── views.py
│   ├── services.py         # NetworkMatchingService (AI)
│   ├── serializers.py
│   └── urls.py
│
├── admin_api/              # Admin Dashboard APIs
│   ├── views.py            # Dashboard, Events, Tickets
│   ├── organizer_views.py  # Organizer endpoints
│   ├── urls.py
│   └── __init__.py
│
└── [other apps...]
```

---

## API Endpoints Quick Reference

### Dashboard
- `GET /api/admin/organizer/dashboard` - Overview metrics

### Events
- `GET /api/admin/organizer/events` - List events
- `POST /api/admin/organizer/events` - Create event
- `GET /api/admin/organizer/events/:id` - Get event details
- `PUT /api/admin/organizer/events/:id` - Update event
- `DELETE /api/admin/organizer/events/:id` - Delete event

### Check-In
- `PUT /api/admin/events/:eventId/attendees/:attendeeId/checkin` - QR check-in

### Tickets
- `GET /api/admin/events/:eventId/tickets` - Get tickets
- `PUT /api/admin/events/:eventId/tickets/:ticketId` - Update ticket
- `POST /api/events/:eventId/tickets` - Create tickets
- `GET /api/admin/events/:eventId/tickets/export` - Export CSV

### Chatbot
- `POST /api/chatbot/kb/rebuild_knowledge_base/` - Rebuild KB
- `POST /api/chatbot/conversations/` - Start conversation
- `POST /api/chatbot/conversations/:id/send_message/` - Send message

### Networking
- `GET /api/networking/profiles/my_profile/` - Your profile
- `POST /api/networking/profiles/:id/find_matches/` - Find matches
- `POST /api/networking/recommendations/generate_recommendations/` - Get recommendations
- `POST /api/networking/connections/` - Create connection request

---

## Common Issues & Solutions

### Issue 1: ModuleNotFoundError
```bash
# Solution: Install missing packages
pip install -r requirements.txt
```

### Issue 2: Database migration error
```bash
# Solution: Reset database (development only!)
python manage.py migrate zero
python manage.py migrate
```

### Issue 3: Groq API key not working
```
- Check GROQ_API_KEY in .env
- Verify key is valid at https://console.groq.com/
- Check for trailing/leading spaces
```

### Issue 4: CORS errors from frontend
```python
# In settings.py, add frontend URL to CORS_ALLOWED_ORIGINS
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
```

### Issue 5: Static files not loading
```bash
python manage.py collectstatic --no-input
```

---

## Development Commands

### Database
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migrations status
python manage.py showmigrations
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts

# Run with verbose output
python manage.py test -v 2
```

### Shell
```bash
# Interactive Django shell
python manage.py shell

# Load sample data
python manage.py loaddata fixtures/sample_data.json
```

### Admin
```bash
# Create superuser
python manage.py createsuperuser

# Change superuser password
python manage.py changepassword username
```

---

## Performance Optimization

### Caching
```python
# In settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

### Database Optimization
```python
# Use select_related for foreign keys
events = Event.objects.select_related('venue', 'speaker').all()

# Use prefetch_related for many-to-many
events = Event.objects.prefetch_related('sessions').all()
```

---

## Production Deployment

### 1. Environment Variables
```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECRET_KEY=<generate-secure-key>
DATABASE_URL=postgresql://...
```

### 2. Static Files
```bash
python manage.py collectstatic --no-input
```

### 3. Gunicorn
```bash
pip install gunicorn
gunicorn event_platform.wsgi:application --bind 0.0.0.0:8000
```

### 4. Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

---

## Debugging

### Enable Detailed Logging
```python
# In settings.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Django Debug Toolbar
```bash
pip install django-debug-toolbar

# Add to INSTALLED_APPS
INSTALLED_APPS = [..., 'debug_toolbar']

# Add to MIDDLEWARE
MIDDLEWARE = [..., 'debug_toolbar.middleware.DebugToolbarMiddleware']

# Add to urls.py
import debug_toolbar
urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
```

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [LangChain Documentation](https://python.langchain.com/)
- [Sentence Transformers](https://www.sbert.net/)

---

## Support

For issues or questions:
1. Check project documentation
2. Review error logs
3. Check Django debug toolbar
4. Contact development team

---

Happy coding! 🚀
