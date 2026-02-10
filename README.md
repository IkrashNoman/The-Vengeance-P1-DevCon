# Smart Event Management & Networking Platform (The Vengeance)

A comprehensive Django REST Framework backend for an AI-powered multi-tenant event management and networking platform. Supports olympiad organization, module/sports management, real-time interactions, and advanced analytics.

## Project Status

✅ **Database & Models:** 95% complete  
✅ **API Routing:** 100% complete  
✅ **Admin Dashboard APIs:** 100% complete  
⚠️ **Serializers:** 70% complete  
⚠️ **AI/ML Features:** 0% (planned)  
⚠️ **Payment Integration:** 0% (planned)  

See [PROJECT_ANALYSIS.md](PROJECT_ANALYSIS.md) for detailed assessment.

---

## Quick Start

### Installation

```bash
cd backend
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Backend runs on `http://localhost:8000/`

---

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login (returns JWT token)
- `POST /api/auth/signup/` - User registration
- `POST /api/auth/users/:id/change_password/` - Change password
- `GET /api/auth/users/me/` - Get current user profile

### Admin Dashboard APIs

#### Events Management
- `GET /api/admin/events` - List all events (with summary stats)
- `GET /api/admin/events/:id` - Get detailed event with sessions, attendees, tickets
- `POST /api/admin/events` - Create new event
- `PUT /api/admin/events/:id` - Update event
- `DELETE /api/admin/events/:id` - Delete event

**Example POST /api/admin/events:**
```json
{
  "name": "AI & ML Conference 2026",
  "description": "Explore latest in AI and ML",
  "event_type": "workshop",
  "startDate": "2026-03-15T09:00:00Z",
  "endDate": "2026-03-17T17:00:00Z",
  "tenant": 1,
  "ticketTypes": [
    {"type": "Early Bird", "price": 20, "quantity": 100, "sold": 50},
    {"type": "Regular", "price": 40, "quantity": 200, "sold": 100}
  ]
}
```

**Example GET /api/admin/events/:id Response:**
```json
{
  "id": 1,
  "name": "AI & ML Conference 2026",
  "description": "Explore latest in AI and ML",
  "startDate": "2026-03-15",
  "endDate": "2026-03-17",
  "venue": "MCS NUST Auditorium",
  "ticketTypes": [
    {"type": "Early Bird", "price": 20.0, "sold": 50},
    {"type": "Regular", "price": 40.0, "sold": 100}
  ],
  "sessions": [
    {"id": 1, "title": "AI in Healthcare", "speaker": "Dr. Ali", "time": "10:00 AM"},
    {"id": 2, "title": "ML Workshop", "speaker": "Ms. Sara", "time": "1:00 PM"}
  ],
  "attendees": [
    {"id": 1, "name": "Akrash", "email": "akrash@example.com", "checkedIn": false},
    {"id": 2, "name": "Ali", "email": "ali@example.com", "checkedIn": true}
  ]
}
```

#### Analytics & Monitoring
- `GET /api/admin/events` - List events with attendee counts and revenue
- `GET /api/admin/notifications` - Get recent system notifications (top 20)
- `GET /api/admin/attendance` - Daily attendance time series data
- `GET /api/admin/revenue` - Revenue per event

**Example GET /api/admin/attendance Response:**
```json
[
  {"date": "2026-02-01", "attendees": 50},
  {"date": "2026-02-05", "attendees": 120},
  {"date": "2026-02-10", "attendees": 180},
  {"date": "2026-02-15", "attendees": 220},
  {"date": "2026-02-20", "attendees": 250}
]
```

### Core Entity APIs

#### Olympiad Management
- `GET /api/olympiad/` - List olympiads
- `POST /api/olympiad/` - Create olympiad
- `GET /api/olympiad/:id/` - Get olympiad details
- `PUT /api/olympiad/:id/` - Update olympiad
- `DELETE /api/olympiad/:id/` - Delete olympiad

#### Modules (Competitions)
- `GET /api/modules/` - List modules
- `POST /api/modules/` - Create module
- `GET /api/modules/:id/` - Get module details
- `GET /api/modules/rounds/` - List module rounds
- `GET /api/modules/judges/` - List judges

#### Sports
- `GET /api/sports/` - List sports
- `POST /api/sports/` - Create sport
- `GET /api/sports/:id/` - Get sport details
- `GET /api/sports/matches/` - List sport matches

#### Events
- `GET /api/events/` - List events
- `POST /api/events/` - Create event
- `GET /api/events/:id/` - Get event details
- `GET /api/events/attendance/` - List event attendances
- `GET /api/events/sessions/` - List event sessions

#### Registrations
- `GET /api/registrations/` - List registrations
- `POST /api/registrations/` - Register for event/module/sport
- `GET /api/registrations/:id/` - Get registration details
- `GET /api/registrations/my_registrations/` - Get my registrations
- `GET /api/registrations/teams/` - List teams
- `GET /api/registrations/team-members/` - List team members

#### Venues
- `GET /api/venues/` - List venues
- `POST /api/venues/` - Create venue
- `GET /api/venues/:id/` - Get venue details
- `GET /api/venues/spaces/` - List venue spaces

#### Networking
- `GET /api/networking/profiles/` - List network profiles
- `GET /api/networking/connections/` - List connections
- `GET /api/networking/recommended/` - Get recommended connections

#### Interactions (Polls, Q&A)
- `GET /api/interactions/polls/` - List polls
- `POST /api/interactions/polls/` - Create poll
- `GET /api/interactions/responses/` - List poll responses
- `GET /api/interactions/qna/` - List Q&A

#### Notifications
- `GET /api/notifications/` - List notifications
- `GET /api/notifications/templates/` - List notification templates

#### Recommendations & Analytics
- `GET /api/recommendations/activity/` - User activity logs
- `GET /api/recommendations/sessions/` - Session recommendations
- `GET /api/recommendations/modules/` - Module recommendations
- `GET /api/analytics/events/` - Event analytics
- `GET /api/analytics/modules/` - Module analytics
- `GET /api/analytics/sports/` - Sport analytics

#### Chatbot
- `GET /api/chatbot/kb/` - Knowledge base articles
- `GET /api/chatbot/conversations/` - Chatbot conversations

---

## Authentication

All endpoints (except signup/login) require JWT authentication. Include token in header:

```bash
Authorization: Bearer <your_jwt_token>
```

### Get JWT Token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {...}
}
```

---

## Role-Based Access Control (RBAC)

### User Roles
- **super_admin**: Full platform access
- **organizer**: Can manage their tenant's events/olympiads
- **staff**: Limited administrative privileges
- **attendee**: Can register, attend events
- **speaker**: Can lead sessions
- **sponsor**: Sponsor management access

### Permission Classes Used
- `IsAuthenticated` - Authenticated users only
- `IsSuperAdmin` - Super admin users only
- `IsOrganizer` - Organizer users only
- `CanManageEvents` - Users with event management permission
- `CanViewAnalytics` - Users with analytics viewing permission
- `IsTenantMember` - Users within same tenant
- `RoleBasedPermission` - Custom role-based checks

---

## Database Models Overview

### Auth & Tenancy
- `User` - Custom user model with roles
- `Tenant` - Multi-tenant organization
- `Department` - Organizational departments
- `UserPermission` - Fine-grained permissions

### Olympiad & Competition
- `Olympiad` - Main olympiad/event
- `Category` - Age groups, skill levels, etc.
- `Module` - Technical/non-technical competitions
- `ModuleRound` - Rounds in competitions
- `Sport` - Athletic competitions
- `SportMatch` - Individual sport matches

### Events
- `Event` - Individual events/sessions
- `EventSession` - Breakout sessions
- `TicketType` - Ticket pricing tiers
- `EventAttendance` - Check-in tracking

### Registrations & Teams
- `Registration` - Registration records
- `Team` - Team entities
- `TeamMember` - Team membership

### Networking & Interactions
- `NetworkProfile` - Network profiles
- `Connection` - Network connections
- `Poll` - Live polls
- `QnA` - Q&A system
- `Notification` - System notifications

### Analytics & Recommendations
- `EventAnalytics` - Event statistics
- `UserActivityLog` - Activity tracking
- `SessionRecommendation` - Recommended sessions

---

## File Structure

```
backend/
├── event_platform/          # Main project
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL routing
│   └── asgi.py              # Async support
├── accounts/                # User management
├── admin_api/               # Admin dashboard APIs ✨ NEW
├── analytics/               # Analytics
├── olympiad_core/           # Olympiad management
├── modules/                 # Module/competition management
├── sports/                  # Sports management
├── events/                  # Event management
├── registrations/           # Registration system
├── venues/                  # Venue management
├── networking/              # Networking features
├── interactions/            # Polls, Q&A, feedback
├── notifications/           # Notification system
├── recommendations/         # AI recommendations
├── chatbot/                 # RAG-powered chatbot
├── societies/               # Society/club management
├── departments/             # Department management
├── tenants/                 # Multi-tenancy
├── core_permissions.py      # Permission classes
├── requirements.txt         # Python dependencies
└── manage.py                # Django management
```

---

## Key Features Implemented

✅ Multi-tenant architecture  
✅ Role-based access control (RBAC)  
✅ Admin dashboard with analytics  
✅ Event CRUD with nested data  
✅ Registration system with payment tracking  
✅ Event attendance & check-in  
✅ Networking & connections  
✅ Real-time interactions (polls, Q&A)  
✅ Notification system  
✅ Analytics & recommendations  
✅ Activity logging  
✅ Chatbot knowledge base  

---

## Planned Features

🔄 Payment Integration (Stripe, PayPal)  
🔄 QR code generation & validation  
🔄 Email notifications  
🔄 WebSocket real-time updates  
🔄 AI/ML recommendation engine  
🔄 RAG-powered chatbot inference  
🔄 Advanced search & discovery  
🔄 Gesture recognition  
🔄 Accessibility features  
🔄 Progressive Web App (PWA) support  

---

## Development Notes

- Database: SQLite (dev) / MySQL (prod)
- Auth: JWT tokens via `djangorestframework-simplejwt`
- Real-time: Django Channels configured (not yet used)
- Task queue: Celery configured (not yet used)
- CORS: Enabled for all origins (dev only)

---

## Next Steps

1. ✅ Complete API routing
2. ✅ Add admin dashboard APIs
3. ⏳ Implement payment integration
4. ⏳ Add QR code generation
5. ⏳ Implement WebSocket support
6. ⏳ Build recommendation engine
7. ⏳ Add comprehensive testing

---

## Contact & Support

For issues or questions, refer to [PROJECT_ANALYSIS.md](PROJECT_ANALYSIS.md) for detailed architecture documentation.

