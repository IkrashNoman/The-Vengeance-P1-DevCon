// Frontend API Configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api';
export const API_TIMEOUT = 30000; // 30 seconds

export const API_ENDPOINTS = {
  // Authentication
  login: '/auth/login/',
  logout: '/auth/logout/',
  register: '/auth/register/',
  
  // Admin Dashboard & Organizer
  adminDashboard: '/admin/organizer/dashboard',
  organizerEvents: '/admin/organizer/events',
  organizerEventDetail: (id: string | number) => `/admin/organizer/events/${id}`,
  organizerCheckIn: (eventId: string | number, attendeeId: string | number) => 
    `/admin/organizer/events/${eventId}/attendees/${attendeeId}/checkin`,
  
  // Events
  events: '/events/',
  eventDetail: (id: string | number) => `/events/${id}/`,
  eventSessions: (eventId: string | number) => `/admin/events/${eventId}/sessions`,
  sessionDetail: (eventId: string | number, sessionId: string | number) => 
    `/admin/events/${eventId}/sessions/${sessionId}`,
  sessionAttendees: (eventId: string | number, sessionId: string | number) => 
    `/admin/events/${eventId}/sessions/${sessionId}/attendees`,
  
  // Tickets
  eventTickets: (eventId: string | number) => `/admin/events/${eventId}/tickets`,
  ticketDetail: (eventId: string | number, ticketId: string | number) => 
    `/admin/events/${eventId}/tickets/${ticketId}`,
  
  // Networking
  networkProfiles: '/networking/',
  findMatches: (profileId: string | number) => `/networking/${profileId}/find-matches/`,
  generateRecommendations: (profileId: string | number) => 
    `/networking/${profileId}/generate-recommendations/`,
  
  // Chatbot
  chatbot: '/chatbot/',
  chatbotConversation: (conversationId: string | number) => `/chatbot/${conversationId}/`,
  chatbotRebuild: '/chatbot/rebuild-knowledge-base/',
  
  // Notifications
  notifications: '/notifications/',
  
  // Analytics
  analytics: '/analytics/',
  dashboardMetrics: '/analytics/dashboard-metrics/',
};
