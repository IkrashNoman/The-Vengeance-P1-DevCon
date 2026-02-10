#!/usr/bin/env python
"""
Admin API Test Guide

This guide demonstrates how to use the new admin API endpoints for session management.
API Base: http://localhost:8000/api/admin/
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/admin"

# Assume you have a valid JWT token (get from login endpoint)
HEADERS = {
    "Authorization": "Bearer YOUR_JWT_TOKEN_HERE",
    "Content-Type": "application/json"
}

def test_list_events_with_sessions():
    """
    GET /api/admin/events
    List all events with nested sessions and attendees
    """
    print("\n=== GET all events with sessions ===")
    url = f"{BASE_URL}/events"
    response = requests.get(url, headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


def test_create_session(event_id):
    """
    POST /api/admin/events/:eventId/sessions
    Create a new session for an event
    """
    print(f"\n=== POST create session for event {event_id} ===")
    url = f"{BASE_URL}/events/{event_id}/sessions"
    
    payload = {
        "title": "Advanced Python Programming",
        "speaker": "Dr. Ahmed Hassan",
        "startTime": "14:00",
        "endTime": "15:30",
        "room": "Main Auditorium",
        "capacity": 100,
        "description": "Deep dive into Python best practices"
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 201:
        return response.json()['id']  # Return session ID for next operations
    return None


def test_update_session(event_id, session_id):
    """
    PUT /api/admin/events/:eventId/sessions/:sessionId
    Update an existing session
    """
    print(f"\n=== PUT update session {session_id} for event {event_id} ===")
    url = f"{BASE_URL}/events/{event_id}/sessions/{session_id}"
    
    payload = {
        "title": "Advanced Python Programming - Updated",
        "speaker": "Dr. Ahmed Hassan",
        "startTime": "15:00",
        "endTime": "16:30",
        "room": "Conference Hall A",
        "capacity": 120
    }
    
    response = requests.put(url, headers=HEADERS, json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


def test_get_session_attendees(event_id, session_id):
    """
    GET /api/admin/events/:eventId/sessions/:sessionId/attendees
    Export attendees for a specific session
    """
    print(f"\n=== GET attendees for session {session_id} (event {event_id}) ===")
    url = f"{BASE_URL}/events/{event_id}/sessions/{session_id}/attendees"
    
    response = requests.get(url, headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


def test_delete_session(event_id, session_id):
    """
    DELETE /api/admin/events/:eventId/sessions/:sessionId
    Delete a session
    """
    print(f"\n=== DELETE session {session_id} from event {event_id} ===")
    url = f"{BASE_URL}/events/{event_id}/sessions/{session_id}"
    
    response = requests.delete(url, headers=HEADERS)
    print(f"Status: {response.status_code}")
    if response.content:
        print(json.dumps(response.json(), indent=2))
    else:
        print("(No content - session deleted successfully)")


def test_get_notifications():
    """GET /api/admin/notifications"""
    print("\n=== GET recent notifications ===")
    url = f"{BASE_URL}/notifications"
    response = requests.get(url, headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


def test_get_attendance():
    """GET /api/admin/attendance"""
    print("\n=== GET daily attendance statistics ===")
    url = f"{BASE_URL}/attendance"
    response = requests.get(url, headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


def test_get_revenue():
    """GET /api/admin/revenue"""
    print("\n=== GET revenue per event ===")
    url = f"{BASE_URL}/revenue"
    response = requests.get(url, headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


def test_workflows():
    """
    Run complete workflow:
    1. Create a session
    2. Update the session
    3. Get session attendees
    4. Test other analytics
    """
    print("\n" + "="*60)
    print("ADMIN API SESSION MANAGEMENT - WORKFLOW TEST")
    print("="*60)
    
    event_id = 1  # Change this to your actual event ID
    
    # Create session
    session_id = test_create_session(event_id)
    
    if session_id:
        # Update session
        test_update_session(event_id, session_id)
        
        # Get attendees
        test_get_session_attendees(event_id, session_id)
        
        # Delete session
        test_delete_session(event_id, session_id)
    
    # Test analytics endpoints
    test_get_notifications()
    test_get_attendance()
    test_get_revenue()
    
    print("\n" + "="*60)
    print("WORKFLOW TEST COMPLETE")
    print("="*60)


if __name__ == "__main__":
    print("""
    Instructions:
    1. Get a JWT token from POST /api/accounts/login/
    2. Replace YOUR_JWT_TOKEN_HERE with your actual token above
    3. Run this script: python admin_api_test.py
    4. Uncomment the functions you want to test
    """)
    
    # Uncomment to run tests:
    # test_workflows()
