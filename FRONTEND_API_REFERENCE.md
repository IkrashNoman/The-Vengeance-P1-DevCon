# Frontend - Backend API Contract Reference

## Quick API Reference for Frontend Developers

Use this as a quick reference while building frontend components.

---

## Base URL
```
Development: http://localhost:8000/api
Production: https://api.yourdomain.com/api
```

## Authentication Header
```javascript
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

---

## 1. Dashboard APIs

### Get Dashboard Metrics
```javascript
GET /admin/organizer/dashboard

Response: {
  events: 5,
  registrations: 120,
  revenue: 4500,
  sessions: 20,
  engagementScore: 87,
  registrationTrends: { labels, data },
  ticketSales: { labels, data },
  sessionAttendance: [],
  notifications: []
}
```

---

## 2. Event Management APIs

### List Events
```javascript
GET /admin/organizer/events

Response: [{
  id, name, description, startDate, endDate, venue,
  ticketTypes: [{ type, price, sold }],
  sessions: [{ id, title, speaker, time }],
  attendees: [{ id, name, email, checkedIn }]
}]
```

### Create Event
```javascript
POST /admin/organizer/events

Body: {
  name: string,
  description: string,
  startDate: date,
  endDate: date,
  ticketTypes: [{ type, price, quantity }],
  sessions: [{ title, start_time, end_time, room }]
}

Response: { id, message }
```

### Get Single Event
```javascript
GET /admin/organizer/events/:id

Response: { Event object with all details }
```

### Update Event
```javascript
PUT /admin/organizer/events/:id

Body: { name?, description?, startDate?, endDate? }

Response: { message, id }
```

### Delete Event
```javascript
DELETE /admin/organizer/events/:id

Response: 204 No Content
```

---

## 3. QR Check-In APIs

### Check In Attendee (QR Scan)
```javascript
PUT /admin/events/:eventId/attendees/:attendeeId/checkin

Body: { checkedIn: true|false }

Response: {
  success: true,
  message: string,
  data: { attendeeId, eventId, status, checkInTime }
}
```

---

## 4. Ticket APIs

### Get All Tickets for Event
```javascript
GET /admin/events/:eventId/tickets

Response: {
  eventId: number,
  tickets: [{
    id, type, price, earlyBirdPrice, groupDiscount,
    sold, revenue
  }]
}
```

### Update Ticket Pricing
```javascript
PUT /admin/events/:eventId/tickets/:ticketId

Body: {
  price?: number,
  earlyBirdPrice?: number,
  groupDiscount?: string
}

Response: {
  success: true,
  message: string,
  ticket: { updated ticket object }
}
```

### Create/Bulk Update Tickets
```javascript
POST /admin/events/:eventId/tickets

Body: [{
  type, price, earlyBirdPrice, groupDiscount, sold, quantity
}]

Response: {
  success: true,
  message: string,
  tickets: [ array of created tickets ]
}
```

### Export Tickets to CSV
```javascript
GET /admin/events/:eventId/tickets/export

Response: CSV file download
```

---

## 5. Session APIs

### Create Session
```javascript
POST /admin/events/:eventId/sessions

Body: {
  title: string,
  speaker: string,
  startTime: time,
  endTime: time,
  room: string,
  capacity: number
}

Response: { Session object }
```

### Update Session
```javascript
PUT /admin/events/:eventId/sessions/:sessionId

Body: Same as create

Response: { Session object }
```

### Delete Session
```javascript
DELETE /admin/events/:eventId/sessions/:sessionId

Response: 204 No Content
```

### Get Session Attendees
```javascript
GET /admin/events/:eventId/sessions/:sessionId/attendees

Response: [{
  id, name, email, checkedIn
}]
```

---

## 6. Chatbot APIs

### Rebuild Knowledge Base
```javascript
POST /chatbot/kb/rebuild_knowledge_base/

Response: {
  message: string,
  document_count: number,
  db_path: string
}
```

### Start Conversation
```javascript
POST /chatbot/conversations/

Body: {
  message: string,
  olympiad_id: number (optional)
}

Response: {
  session_id: string,
  user_message: string,
  bot_response: string,
  created_at: datetime
}
```

### Send Message
```javascript
POST /chatbot/conversations/:id/send_message/

Body: { message: string }

Response: {
  session_id: string,
  user_message: string,
  bot_response: string,
  message_count: number
}
```

---

## 7. Networking APIs

### Get My Profile
```javascript
GET /networking/profiles/my_profile/

Response: {
  id, user, job_title, company, industry,
  interests[], expertise[],
  show_in_discovery, allow_direct_messages
}
```

### Update My Profile
```javascript
PUT /networking/profiles/:id/

Body: {
  job_title?, company?, industry?,
  interests[]?, expertise[]?,
  show_in_discovery?, allow_direct_messages?
}

Response: { Updated profile }
```

### Discover Profiles
```javascript
GET /networking/profiles/discover/?limit=10

Response: [{ Profile objects }]
```

### Find Semantic Matches
```javascript
POST /networking/profiles/:id/find_matches/?top_n=3

Response: {
  user_id: number,
  matches: [{
    rank, user_id, name, email, job_title, company,
    interests[], expertise[],
    match_score (0-1),
    reason: string
  }]
}
```

### Generate Recommendations
```javascript
POST /networking/recommendations/generate_recommendations/?limit=5

Response: {
  message: string,
  recommendations: [{
    id, user, recommended_user,
    match_score, reason, created_at
  }]
}
```

### Create Connection
```javascript
POST /networking/connections/

Body: {
  user_to: number,
  message: string (optional)
}

Response: {
  id, user_from, user_to, status,
  message, initiated_at
}
```

### Accept Connection
```javascript
POST /networking/connections/:id/accept/

Response: {
  id, status: 'connected', connected_at
}
```

### Reject/Delete Connection
```javascript
POST /networking/connections/:id/reject/

Response: 204 No Content
```

---

## 8. Admin Dashboard APIs

### Get Events Overview
```javascript
GET /admin/events

Response: [{
  id, name, status, attendees, revenue, date
}]
```

### Get Notifications
```javascript
GET /admin/notifications

Response: [{
  id, msg
}]
```

### Get Attendance Chart Data
```javascript
GET /admin/attendance

Response: [{
  date: string,
  attendees: number
}]
```

### Get Revenue Data
```javascript
GET /admin/revenue

Response: [{
  event: string,
  revenue: number
}]
```

---

## Error Responses

All error responses follow this format:

```javascript
{
  status: 400,
  error: "Error message",
  details: {} // Additional info
}
```

### Common Status Codes
- `200` OK
- `201` Created
- `204` No Content
- `400` Bad Request
- `401` Unauthorized (invalid token)
- `403` Forbidden (no permission)
- `404` Not Found
- `500` Server Error

---

## usage Examples

### React Fetch Example
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Fetch dashboard
const getDashboard = () => api.get('/admin/organizer/dashboard');

// Create event
const createEvent = (eventData) => api.post('/admin/organizer/events', eventData);

// Check in attendee
const checkInAttendee = (eventId, attendeeId) =>
  api.put(`/admin/events/${eventId}/attendees/${attendeeId}/checkin`, {
    checkedIn: true
  });
```

### Vue/Nuxt Example
```javascript
// composable/useApi.js
import { useFetch } from 'nuxt/app';

export const useDashboard = () => {
  return useFetch('/api/admin/organizer/dashboard', {
    headers: {
      Authorization: `Bearer ${useAuthStore().token}`
    }
  });
};
```

### Angular Example
```typescript
import { HttpClient, HttpHeaders } from '@angular/common/http';

constructor(private http: HttpClient) {}

getDashboard() {
  const headers = new HttpHeaders({
    'Authorization': `Bearer ${this.authService.getToken()}`
  });
  return this.http.get('/api/admin/organizer/dashboard', { headers });
}
```

---

## Tips for Frontend Integration

1. **Always include Authorization header** even for public endpoints
2. **Handle error responses gracefully** - show user-friendly messages
3. **Use loading states** while fetching data
4. **Implement token refresh** when token expires
5. **Validate form data** before sending to backend
6. **Handle network timeouts** gracefully
7. **Cache dashboard data** to reduce API calls
8. **Use WebSockets** for real-time updates (future enhancement)

---

## Testing Endpoints Locally

### Using curl
```bash
# Get dashboard
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/admin/organizer/dashboard

# Create event
curl -X POST http://localhost:8000/api/admin/organizer/events \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name":"Test Event"}'
```

### Using Postman
1. Set base URL: `http://localhost:8000/api`
2. Add global Authorization header with Bearer token
3. Test endpoints with provided examples

### Using VS Code REST Client
```
# api.rest
@baseUrl = http://localhost:8000/api
@token = YOUR_JWT_TOKEN

### Get Dashboard
GET {{baseUrl}}/admin/organizer/dashboard
Authorization: Bearer {{token}}

### Create Event
POST {{baseUrl}}/admin/organizer/events
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "name": "Web Dev Workshop",
  "description": "Learn modern web development",
  "startDate": "2026-04-01",
  "endDate": "2026-04-02"
}
```

---

## Rate Limiting

Currently no rate limiting is enforced, but in production:
- Implement per-user rate limits
- Use Redis for distributed rate limiting
- Consider API versioning (v1, v2, etc.)

---

## API Versioning

Future API structure:
```
/api/v1/admin/...
/api/v2/admin/...
```

---

## Support & Contact

For API documentation issues or clarifications:
- Check BACKEND_INTEGRATION.md for detailed docs
- Review backend code comments
- Contact backend team

---

Last Updated: February 10, 2026
Version: 1.0
