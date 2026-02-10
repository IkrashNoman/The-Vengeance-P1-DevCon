# Admin API Documentation

Complete documentation for the admin dashboard API endpoints.

## Overview

The admin API provides comprehensive event management, session scheduling, attendance tracking, and analytics endpoints for administrators.

## Base URL

```
/api/admin/
```

All requests require JWT authentication via `Authorization: Bearer <token>` header.

---

## Events Management

### GET /api/admin/events
List all events with nested sessions and attendees.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "AI & ML Conference 2026",
    "sessions": [
      {
        "id": 1,
        "title": "AI in Healthcare",
        "speaker": "Dr. Ali",
        "startTime": "10:00",
        "endTime": "11:00",
        "room": "Auditorium",
        "capacity": 50,
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
  }
]
```

---

## Session Management

### POST /api/admin/events/:eventId/sessions
Create a new session for an event.

**Required Fields:**
- `title` (string): Session title
- `startTime` (string): Start time in HH:MM format
- `endTime` (string): End time in HH:MM format

**Optional Fields:**
- `speaker` (string): Speaker name
- `room` (string): Room/location
- `capacity` (integer): Max capacity (default: 50)
- `description` (string): Session description

**Request Example:**
```bash
POST /api/admin/events/1/sessions
Content-Type: application/json

{
  "title": "New Session",
  "speaker": "Dr. Someone",
  "startTime": "14:00",
  "endTime": "15:00",
  "room": "Auditorium",
  "capacity": 50
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "title": "New Session",
  "speaker": "Dr. Someone",
  "startTime": "14:00",
  "endTime": "15:00",
  "room": "Auditorium",
  "capacity": 50
}
```

---

### PUT /api/admin/events/:eventId/sessions/:sessionId
Update an existing session.

**Request Example:**
```bash
PUT /api/admin/events/1/sessions/2
Content-Type: application/json

{
  "title": "Updated Session Title",
  "speaker": "Dr. Updated",
  "startTime": "15:00",
  "endTime": "16:00",
  "room": "Main Hall",
  "capacity": 100
}
```

**Response (200 OK):** Returns updated session object.

---

### DELETE /api/admin/events/:eventId/sessions/:sessionId
Delete a session from an event.

**Request Example:**
```bash
DELETE /api/admin/events/1/sessions/2
```

**Response (204 No Content):** Empty response body.

---

## Session Attendees

### GET /api/admin/events/:eventId/sessions/:sessionId/attendees
Export attendees list for a specific session.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Akrash",
    "email": "akrash@example.com",
    "checkedIn": false
  },
  {
    "id": 2,
    "name": "Ahmed",
    "email": "ahmed@example.com",
    "checkedIn": true
  }
]
```

---

## Dashboard Analytics

### GET /api/admin/notifications
Recent notifications (last 20).

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "msg": "New registration for AI Conference"
  }
]
```

---

### GET /api/admin/attendance
Daily attendance time series data.

**Response (200 OK):**
```json
[
  {
    "date": "2026-03-15",
    "attendees": 45
  },
  {
    "date": "2026-03-16",
    "attendees": 78
  }
]
```

---

### GET /api/admin/revenue
Revenue breakdown by event.

**Response (200 OK):**
```json
[
  {
    "event": "AI Conference 2026",
    "revenue": 5000.00
  },
  {
    "event": "Web Development Workshop",
    "revenue": 1200.00
  }
]
```

---

## Error Handling

### 400 Bad Request
Invalid request data or missing required fields.

```json
{
  "error": "Tenant required"
}
```

### 403 Forbidden
User lacks permission to perform the action.

```json
{
  "error": "Permission denied"
}
```

### 404 Not Found
Resource not found.

```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
Server encountered an error processing the request.

---

## Authentication & Permissions

### Required Headers
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

### User Roles
- **Super Admin:** Full access to all events/sessions across all tenants
- **Organizer:** Access to events/sessions for their tenant only
- **Staff:** Read-only access
- **Others:** Limited or no access

### Permission Checks
- All endpoints require `IsAuthenticated`
- Create/Update/Delete operations require `IsSuperAdmin` or `can_manage_events` permission
- Multi-tenant data isolation enforced: users see only their tenant's data

---

## Rate Limiting

No rate limiting currently implemented. Subject to change in production.

---

## Pagination

Pagination not yet implemented. All results returned without limit.

---

## Example Usage with curl

### Get Events with Sessions
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/admin/events
```

### Create Session
```bash
curl -X POST \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "New Session",
       "speaker": "Dr. Someone",
       "startTime": "14:00",
       "endTime": "15:00",
       "room": "Auditorium",
       "capacity": 50
     }' \
     http://localhost:8000/api/admin/events/1/sessions
```

### Get Session Attendees
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/admin/events/1/sessions/1/attendees
```

### Update Session
```bash
curl -X PUT \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Updated Title",
       "speaker": "Dr. Updated",
       "startTime": "15:00",
       "endTime": "16:00",
       "room": "Main Hall",
       "capacity": 100
     }' \
     http://localhost:8000/api/admin/events/1/sessions/1
```

### Delete Session
```bash
curl -X DELETE \
     -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/admin/events/1/sessions/1
```

