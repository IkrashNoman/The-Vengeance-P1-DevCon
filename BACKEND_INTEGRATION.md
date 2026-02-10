# Backend Integration Guide

## Complete API Documentation for Frontend Integration

This guide provides comprehensive documentation for integrating all backend APIs with the frontend application.

---

## 1. Authentication & Authorization

All endpoints require JWT authentication except public endpoints.

```
Headers: {
  "Authorization": "Bearer <jwt_token>",
  "Content-Type": "application/json"
}
```

---

## 2. Organizer Dashboard API

### Get Dashboard Overview
**Endpoint:** `GET /api/admin/organizer/dashboard`

**Response:**
```json
{
  "events": 5,
  "registrations": 120,
  "revenue": 4500.00,
  "sessions": 20,
  "engagementScore": 87,
  "registrationTrends": {
    "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
    "data": [10, 25, 40, 35, 50]
  },
  "ticketSales": {
    "labels": ["VIP", "Standard", "Early Bird"],
    "data": [30, 70, 20]
  },
  "sessionAttendance": [
    [5, 10, 8, 12],
    [7, 9, 14, 10],
    [10, 12, 9, 15],
    [8, 6, 11, 12]
  ],
  "notifications": [
    {
      "id": 1,
      "type": "warning",
      "message": "Session 'AI Networking' is full"
    }
  ]
}
```

---

## 3. Event Management API

### Get All Events
**Endpoint:** `GET /api/admin/organizer/events`

**Response:**
```json
[
  {
    "id": 1,
    "name": "AI & ML Conference 2026",
    "description": "Explore latest in AI and ML",
    "startDate": "2026-03-15",
    "endDate": "2026-03-17",
    "venue": "MCS NUST Auditorium",
    "ticketTypes": [
      {
        "type": "Early Bird",
        "price": 20,
        "sold": 50
      },
      {
        "type": "Regular",
        "price": 40,
        "sold": 100
      }
    ],
    "sessions": [
      {
        "id": 1,
        "title": "AI in Healthcare",
        "speaker": "Dr. Ali",
        "time": "10:00"
      }
    ],
    "attendees": [
      {
        "id": 1,
        "name": "Akrash",
        "email": "akrash@example.com",
        "checkedIn": false
      }
    ]
  }
]
```

### Get Event Details
**Endpoint:** `GET /api/admin/organizer/events/:id`

**Response:** Same structure as single event object above

### Create Event
**Endpoint:** `POST /api/admin/organizer/events`

**Request:**
```json
{
  "name": "Web Dev Workshop",
  "description": "Learn modern web development",
  "event_type": "workshop",
  "startDate": "2026-04-01",
  "endDate": "2026-04-02",
  "ticketTypes": [
    {
      "type": "Standard",
      "price": 50,
      "quantity": 100
    }
  ],
  "sessions": [
    {
      "title": "Frontend Basics",
      "start_time": "2026-04-01T10:00:00Z",
      "end_time": "2026-04-01T11:00:00Z",
      "room": "Room 101"
    }
  ]
}
```

### Update Event
**Endpoint:** `PUT /api/admin/organizer/events/:id`

**Request:** Same as create (all fields optional)

### Delete Event
**Endpoint:** `DELETE /api/admin/organizer/events/:id`

---

## 4. QR Check-In API

### Check In Attendee
**Endpoint:** `PUT /api/admin/events/:eventId/attendees/:attendeeId/checkin`

**Request:**
```json
{
  "checkedIn": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Attendee check-in updated successfully",
  "data": {
    "attendeeId": 1,
    "eventId": 1,
    "status": "checked_in",
    "checkInTime": "2026-02-10T14:30:00Z"
  }
}
```

---

## 5. Ticket Management API

### Get Event Tickets
**Endpoint:** `GET /api/admin/events/:eventId/tickets`

**Response:**
```json
{
  "eventId": 1,
  "tickets": [
    {
      "id": 1,
      "type": "Standard",
      "price": 100,
      "earlyBirdPrice": 80,
      "groupDiscount": "10% for 5+",
      "sold": 50,
      "revenue": 5000
    },
    {
      "id": 2,
      "type": "VIP",
      "price": 250,
      "earlyBirdPrice": 200,
      "groupDiscount": "15% for 3+",
      "sold": 20,
      "revenue": 5000
    }
  ]
}
```

### Update Ticket Prices
**Endpoint:** `PUT /api/admin/events/:eventId/tickets/:ticketId`

**Request:**
```json
{
  "price": 120,
  "earlyBirdPrice": 90,
  "groupDiscount": "10% for 4+"
}
```

### Create/Bulk Update Tickets
**Endpoint:** `POST /api/events/:eventId/tickets`

**Request:**
```json
[
  {
    "type": "Standard",
    "price": 100,
    "earlyBirdPrice": 80,
    "groupDiscount": "10% for 5+",
    "sold": 50,
    "quantity": 100
  },
  {
    "type": "VIP",
    "price": 250,
    "earlyBirdPrice": 200,
    "groupDiscount": "15% for 3+",
    "sold": 20,
    "quantity": 50
  }
]
```

### Export Tickets to CSV
**Endpoint:** `GET /api/admin/events/:eventId/tickets/export`

**Response:** CSV file download

---

## 6. Chatbot API

### Initialize Chatbot
**Endpoint:** `POST /api/chatbot/kb/rebuild_knowledge_base/`

**Response:**
```json
{
  "message": "Knowledge base rebuilt successfully with 15 documents",
  "document_count": 15,
  "db_path": "./chroma_db_1"
}
```

### Create Conversation
**Endpoint:** `POST /api/chatbot/conversations/`

**Request:**
```json
{
  "message": "What is the olympiad schedule?",
  "olympiad_id": 1
}
```

**Response:**
```json
{
  "session_id": "uuid-string",
  "user_message": "What is the olympiad schedule?",
  "bot_response": "The olympiad is scheduled for...",
  "created_at": "2026-02-10T14:30:00Z"
}
```

### Send Message in Conversation
**Endpoint:** `POST /api/chatbot/conversations/:id/send_message/`

**Request:**
```json
{
  "message": "What about venue information?"
}
```

**Response:**
```json
{
  "session_id": "uuid-string",
  "user_message": "What about venue information?",
  "bot_response": "The venue is located at...",
  "message_count": 2
}
```

---

## 7. Networking & Matching API

### Get My Network Profile
**Endpoint:** `GET /api/networking/profiles/my_profile/`

**Response:**
```json
{
  "id": 1,
  "user": 1,
  "job_title": "Software Engineer",
  "company": "Tech Corp",
  "industry": "Technology",
  "interests": ["AI", "Web Development", "Cybersecurity"],
  "expertise": ["Python", "Django", "React"],
  "show_in_discovery": true,
  "allow_direct_messages": true
}
```

### Discover Other Users
**Endpoint:** `GET /api/networking/profiles/discover/?limit=10`

**Response:** Array of profile objects

### Find Semantic Matches
**Endpoint:** `POST /api/networking/profiles/:id/find_matches/?top_n=3`

**Response:**
```json
{
  "user_id": 1,
  "matches": [
    {
      "rank": 1,
      "user_id": 2,
      "name": "Zahra Khan",
      "email": "zahra@example.com",
      "job_title": "UI/UX Designer",
      "company": "Design Inc",
      "interests": ["Web Design", "AI", "User Experience"],
      "expertise": ["Figma", "UI Design", "Prototyping"],
      "match_score": 0.85,
      "reason": "Common interests in Web Development | Aligned expertise in design and development"
    }
  ]
}
```

### Generate AI Recommendations
**Endpoint:** `POST /api/networking/recommendations/generate_recommendations/?limit=5`

**Response:**
```json
{
  "message": "Generated 3 recommendations",
  "recommendations": [
    {
      "id": 1,
      "user": 1,
      "recommended_user": 2,
      "match_score": 0.85,
      "reason": "Common interests in Web Development",
      "created_at": "2026-02-10T14:30:00Z"
    }
  ]
}
```

### Create Connection Request
**Endpoint:** `POST /api/networking/connections/`

**Request:**
```json
{
  "user_to": 2,
  "message": "Hi, I'd like to connect with you!"
}
```

**Response:**
```json
{
  "id": 1,
  "user_from": 1,
  "user_to": 2,
  "status": "pending",
  "message": "Hi, I'd like to connect with you!",
  "initiated_at": "2026-02-10T14:30:00Z"
}
```

### Accept Connection Request
**Endpoint:** `POST /api/networking/connections/:id/accept/`

**Response:**
```json
{
  "id": 1,
  "status": "connected",
  "connected_at": "2026-02-10T14:30:00Z"
}
```

---

## 8. Session Management API

### Create Session
**Endpoint:** `POST /api/admin/events/:eventId/sessions`

**Request:**
```json
{
  "title": "AI in Healthcare",
  "speaker": "Dr. Ali",
  "startTime": "10:00",
  "endTime": "11:00",
  "room": "Auditorium",
  "capacity": 50
}
```

### Update Session
**Endpoint:** `PUT /api/admin/events/:eventId/sessions/:sessionId`

**Request:** Same as create

### Delete Session
**Endpoint:** `DELETE /api/admin/events/:eventId/sessions/:sessionId`

### List Session Attendees
**Endpoint:** `GET /api/admin/events/:eventId/sessions/:sessionId/attendees`

**Response:**
```json
[
  {
    "id": 1,
    "name": "Akrash",
    "email": "akrash@example.com",
    "checkedIn": true
  }
]
```

---

## 9. Analytics API

### Get Events List
**Endpoint:** `GET /api/admin/events`

**Response:**
```json
[
  {
    "id": 1,
    "name": "AI & ML Conference 2026",
    "date": "2026-03-15",
    "attendees": 150,
    "revenue": 4500,
    "status": "Ongoing"
  }
]
```

### Get Notifications
**Endpoint:** `GET /api/admin/notifications`

**Response:**
```json
[
  {
    "id": 1,
    "msg": "Event 'Web Dev Workshop' has 5 sessions exceeding capacity."
  }
]
```

### Get Attendance Trends
**Endpoint:** `GET /api/admin/attendance`

**Response:**
```json
[
  {
    "date": "2026-02-01",
    "attendees": 50
  },
  {
    "date": "2026-02-05",
    "attendees": 120
  }
]
```

### Get Revenue Data
**Endpoint:** `GET /api/admin/revenue`

**Response:**
```json
[
  {
    "event": "AI & ML Conference",
    "revenue": 4500
  },
  {
    "event": "Web Dev Workshop",
    "revenue": 1200
  }
]
```

---

## 10. Error Handling

All error responses follow this format:

```json
{
  "error": "Description of the error",
  "status": 400,
  "details": {}
}
```

Common HTTP Status Codes:
- `200` OK
- `201` Created
- `204` No Content
- `400` Bad Request
- `401` Unauthorized
- `403` Forbidden
- `404` Not Found
- `500` Internal Server Error

---

## 11. Frontend Integration Examples

### Dashboard Component
```typescript
// Fetch dashboard data
const fetchDashboard = async () => {
  const response = await fetch('/api/admin/organizer/dashboard', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.json();
};
```

### QR Scanner Integration
```typescript
// Handle QR code scan
const handleQRScan = async (attendeeId: number, eventId: number) => {
  const response = await fetch(
    `/api/admin/events/${eventId}/attendees/${attendeeId}/checkin`,
    {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ checkedIn: true })
    }
  );
  return response.json();
};
```

### Chatbot Widget
```typescript
// Send message to chatbot
const sendMessage = async (message: string, sessionId: string) => {
  const response = await fetch('/api/chatbot/conversations/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message, olympiad_id: 1 })
  });
  return response.json();
};
```

### Networking Feed
```typescript
// Get recommendations for current user
const getRecommendations = async () => {
  const response = await fetch(
    '/api/networking/recommendations/generate_recommendations/?limit=5',
    {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    }
  );
  return response.json();
};
```

---

## 12. Multi-Tenant Support

All endpoints are secured with multi-tenant support. Users automatically see only data from their tenant unless they are Super Admins.

```
User Role -> Visibility
- Super Admin: All data
- Tenant Admin: Tenant-specific data
- Organizer: Their own event data
- Attendee: Event they registered for
```

---

## 13. Dependencies

Required Python packages:
```
djangorestframework>=3.14.0
langchain>=0.1.0
langchain-groq>=0.1.0
langchain-chroma>=0.1.0
langchain-community>=0.0.1
sentence-transformers>=2.2.0
scikit-learn>=1.3.0
pandas>=2.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 14. Environment Variables

```
# Groq LLM API
GROQ_API_KEY=your_groq_api_key

# Database
DATABASE_URL=your_database_url

# JWT Settings
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
```

---

## 15. Deployment Checklist

- [ ] Set all environment variables
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create super user: `python manage.py createsuperuser`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Initialize chatbot KB: Rebuild knowledge base via API
- [ ] Test all endpoints with Postman/Insomnia
- [ ] Configure CORS for frontend domain
- [ ] Set up logging and monitoring
- [ ] Enable HTTPS/SSL in production

---

## Support

For issues or questions, refer to the project documentation or contact the development team.
