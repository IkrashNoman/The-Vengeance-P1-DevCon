# Backend Integration Roadmap

## Overview
All 7 new organizer pages are frontend-complete with mock data. Below is the detailed roadmap for connecting them to Django backend APIs.

---

## 1. Attendees Management (`/organizer/attendees`)

### Current State
- ✅ Search & filter functionality (client-side)
- ✅ Attendee profile modal
- ✅ CSV export
- ⏳ Data sourcing from API

### Required Backend Endpoints

#### GET `/api/admin/organizer/events/<event_id>/attendees`
```python
# Response format:
{
  "count": 385,
  "results": [
    {
      "id": 1,
      "name": "Akrash Noman",
      "email": "akrash@nust.edu.pk",
      "company": "TechCorp",
      "interests": ["AI", "ML", "Networking"],
      "sessions_registered": 5,
      "vip_status": true,
      "checked_in": true,
      "ai_connections_count": 12,
      "badge_type": "VIP",
      "registration_date": "2026-02-01T10:30:00Z"
    }
  ]
}
```

#### Implementation Steps
1. Create view in `admin_api/organizer_views.py`:
```python
class OrganizerAttendeesView(viewsets.ModelViewSet):
    """List and manage attendees for organizer's events"""
    serializer_class = AttendeeSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOrAdmin]
    
    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Attendee.objects.filter(
            event__id=event_id,
            event__tenant=self.request.user.current_tenant
        )
```

2. Add URL route:
```python
path('organizer/events/<event_id>/attendees', OrganizerAttendeesView.as_view({'get': 'list'}))
```

3. Update `apiService.ts`:
```typescript
getEventAttendees: async (eventId) => {
  const response = await apiClient.get(`/admin/organizer/events/${eventId}/attendees`);
  return response.data;
}
```

4. Update component:
```typescript
useEffect(() => {
  const fetchAttendees = async () => {
    const data = await apiService.getEventAttendees(eventId);
    setAttendees(data.results);
  };
  fetchAttendees();
}, [eventId]);
```

---

## 2. Reports & Analytics (`/organizer/reports`)

### Current State
- ✅ Charts and visualizations
- ✅ Date range filters
- ⏳ Data sourcing from API

### Required Backend Endpoints

#### GET `/api/admin/organizer/reports`
```python
# Query params: ?from_date=2026-02-01&to_date=2026-02-28&report_type=overview

# Response format:
{
  "date_range": {
    "from": "2026-02-01",
    "to": "2026-02-28"
  },
  "revenue": {
    "total": 9000,
    "by_date": [
      {"date": "2026-02-01", "amount": 500},
      {"date": "2026-02-05", "amount": 1200}
    ],
    "by_ticket_type": [
      {"name": "VIP", "amount": 1200},
      {"name": "Standard", "amount": 3500}
    ]
  },
  "attendance": {
    "total_attendees": 385,
    "sessions": [
      {
        "title": "AI in Healthcare",
        "attendees": 156,
        "capacity": 200
      }
    ]
  },
  "engagement": {
    "poll_participation": 84,
    "qa_activity": 342,
    "avg_score": 87,
    "by_session": [
      {
        "session": "AI Workshop",
        "polls": 142,
        "qa": 67
      }
    ]
  }
}
```

#### Implementation Steps
1. Create analytics aggregator service:
```python
# analytics/services.py
class ReportAggregatorService:
    @staticmethod
    def get_revenue_report(event_id, from_date, to_date):
        """Aggregate revenue data"""
        tickets = TicketType.objects.filter(event_id=event_id)
        # Calculate revenue by type and date
        
    @staticmethod
    def get_engagement_report(event_id, from_date, to_date):
        """Aggregate engagement metrics"""
        sessions = EventSession.objects.filter(event_id=event_id)
        # Count polls, Q&A, attendance
```

2. Create view:
```python
class ReportsView(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        report_type = request.query_params.get('type', 'overview')
        
        service = ReportAggregatorService()
        # Combine multiple data sources
        return Response(aggregated_data)
```

3. Add to apiService:
```typescript
getReports: async (filters) => {
  const response = await apiClient.get('/admin/organizer/reports', {
    params: filters
  });
  return response.data;
}
```

---

## 3. Badge Designer (`/organizer/badges`)

### Current State
- ✅ Template selection
- ✅ QR code generation
- ✅ Live preview
- ⏳ PDF export backend

### Required Backend Endpoints

#### POST `/api/admin/badges/generate-pdf`
```python
# Request:
{
  "attendee_id": 1,
  "template_id": "template1",
  "colors": {
    "bg": "#FFFFFF",
    "text": "#003366",
    "accent": "#EE2022"
  }
}

# Response: PDF binary file
```

#### POST `/api/admin/badges/batch-print`
```python
# Request:
{
  "attendee_ids": [1, 2, 3, 4, 5],
  "template_id": "template1"
}

# Response: Multi-page PDF
```

#### Implementation
```python
# admin_api/badge_views.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class BadgeGeneratorView(viewsets.ViewSet):
    def generate_pdf(self, request):
        attendee_id = request.data['attendee_id']
        attendee = Attendee.objects.get(id=attendee_id)
        
        # Generate PDF using reportlab
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        # Draw badge elements
        return FileResponse(buffer, content_type='application/pdf')
```

---

## 4. AI Matching (`/organizer/ai/matching`)

### Current State
- ✅ Match display and filtering
- ✅ Connection status tracking
- ✅ Network graph visualization (mock)
- ✅ Backend service ready: `NetworkMatchingService`

### Backend Already Implemented
✅ `POST /api/networking/<profile_id>/find-matches/`
✅ `POST /api/networking/<profile_id>/generate-recommendations/`

### Connection Integration
```typescript
// In matching/page.tsx - already using service
const handleRefreshMatches = async () => {
  try {
    const matches = await apiService.findMatches(profileId);
    setMatches(matches);
  } catch (error) {
    alert('Failed to fetch matches');
  }
};
```

**Status**: ✅ Ready to connect

---

## 5. Personalized Agendas (`/organizer/ai/agenda`)

### Current State
- ✅ Agenda display and registration
- ✅ Export functionality
- ⏳ AI recommendation backend

### Required Backend Endpoint

#### GET `/api/ai/agenda/<attendee_id>`
```python
# Response:
{
  "attendee_id": 1,
  "attendee_name": "John Doe",
  "interests": ["AI", "ML", "Data Science"],
  "overall_score": 89,
  "recommended_sessions": [
    {
      "id": 1,
      "title": "AI in Healthcare",
      "speaker": "Dr. Smith",
      "start_time": "09:00",
      "end_time": "10:00",
      "room": "Auditorium A",
      "capacity": 200,
      "attendees": 180,
      "relevance_score": 98,
      "tags": ["AI", "Healthcare", "Innovation"],
      "status": "upcoming"
    }
  ]
}
```

#### Implementation
```python
# ai_services/agenda_service.py
class AgendaRecommendationService:
    @staticmethod
    def get_personalized_agenda(attendee_id):
        """Generate personalized agenda using AI"""
        attendee = Attendee.objects.get(id=attendee_id)
        profile = attendee.network_profile
        
        # Get attendee's interests
        interests = profile.interests_list
        
        # Score all sessions using semantic similarity
        sessions = EventSession.objects.filter(
            event=attendee.event
        )
        
        scored_sessions = [
            {
                'session': session,
                'score': semantic_similarity(interests, session.keywords)
            }
            for session in sessions
        ]
        
        # Return top 10 scored sessions
        return sorted(scored_sessions, key=lambda x: x['score'], reverse=True)[:10]
```

---

## 6. Chatbot Management (`/organizer/ai/chatbot`)

### Current State
- ✅ FAQ management interface
- ✅ Live chatbot tester
- ✅ Backend service ready: `ChatbotService`

### Backend Already Implemented
✅ `POST /api/chatbot/` - Send message
✅ `POST /api/chatbot/rebuild-knowledge-base/` - Rebuild KB
✅ `GET /api/chatbot/` - Get conversations
✅ `ChatbotDataLoader` - Default FAQ knowledge base

### Connection Ready
```typescript
// Already using service
const handleTestChatbot = async () => {
  const response = await apiService.sendChatMessage(testMessage);
  // Display response
};

const handleRebuildKnowledgeBase = async () => {
  const result = await apiService.rebuildKnowledgeBase();
};
```

**Status**: ✅ Ready to use

---

## 7. Trending & Recommendations (`/organizer/ai/recommendations`)

### Current State
- ✅ Trending sessions display
- ✅ Recommendation metrics
- ✅ Engagement breakdown
- ⏳ Backend ranking service

### Required Backend Features

#### GET `/api/admin/organizer/analytics/trending-sessions`
```python
# Response:
{
  "trending_sessions": [
    {
      "id": 1,
      "title": "AI in Healthcare",
      "recommendation_count": 234,
      "engagement_rate": 92,
      "avg_rating": 4.8,
      "is_trending": true
    }
  ],
  "engagement_metrics": [
    {
      "session_id": 1,
      "poll_participation": 142,
      "qa_activity": 67,
      "avg_rating": 4.8,
      "trend": "up"
    }
  ]
}
```

#### Implementation
```python
# admin_api/trending_views.py
class TrendingSessionsView(viewsets.ViewSet):
    def list(self, request):
        # Calculate trends based on:
        # - Number of recommendations (popularity)
        # - Engagement metrics (polls, Q&A)
        # - Ratings (quality score)
        # - Time-based changes (trending indicator)
        
        sessions = EventSession.objects.all()
        scored = [
            {
                'session': s,
                'recommendation_score': s.recommendation_set.count(),
                'engagement_score': calculate_engagement(s),
                'rating': s.get_average_rating(),
                'trending': is_trending(s)
            }
            for s in sessions
        ]
        return Response(scored)
```

---

## Integration Checklist

### Phase 1: Data Models
- [ ] Verify Attendee model fields match API response
- [ ] Verify EventSession model fields
- [ ] Check TicketType model for badge data
- [ ] Confirm Event model has all required fields

### Phase 2: API Endpoints
- [ ] Create `/api/admin/organizer/events/<id>/attendees` endpoint
- [ ] Create `/api/admin/organizer/reports` endpoint
- [ ] Create `/api/admin/badges/generate-pdf` endpoint
- [ ] Create `/api/ai/agenda/<attendee_id>` endpoint
- [ ] Create `/api/admin/analytics/trending-sessions` endpoint
- [ ] Implement ReportAggregatorService
- [ ] Implement AgendaRecommendationService
- [ ] Implement TrendingSessionsService

### Phase 3: Frontend Integration
- [ ] Update `apiService.ts` with all new endpoints
- [ ] Replace mock data with API calls in each page
- [ ] Add error handling and loading states
- [ ] Test with actual backend data
- [ ] Add pagination for large datasets
- [ ] Implement real-time updates (optional)

### Phase 4: Testing
- [ ] Unit test aggregator services
- [ ] Integration test API endpoints
- [ ] E2E test frontend workflows
- [ ] Performance test with large datasets
- [ ] Load test for concurrent requests

---

## Code Examples

### Template for Adding New Endpoint Integration

```typescript
// 1. Add to apiService.ts
yourNewFeature: async (params) => {
  const response = await apiClient.get('/api/your/endpoint', { params });
  return response.data;
}

// 2. Update component
useEffect(() => {
  const fetchData = async () => {
    try {
      setLoading(true);
      const data = await apiService.yourNewFeature(filters);
      setData(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };
  fetchData();
}, [filters]);

// 3. Display with loading state
{loading ? (
  <div>Loading...</div>
) : error ? (
  <div className="text-red-600">{error}</div>
) : (
  <div>{/* Display data */}</div>
)}
```

---

## Timeline Estimate

- **Phase 1**: 2-4 hours (model verification)
- **Phase 2**: 8-12 hours (endpoint creation)
- **Phase 3**: 6-8 hours (frontend integration)
- **Phase 4**: 4-6 hours (testing)

**Total**: 20-30 hours

---

## Questions & Support

For issues during integration:
1. Check Django logs for 500 errors
2. Verify request/response format matches documentation
3. Test endpoint with curl before frontend integration
4. Check CORS settings if getting browser errors
5. Verify JWT token is included in requests

---

**Last Updated**: February 10, 2026
**Status**: Ready for backend integration
