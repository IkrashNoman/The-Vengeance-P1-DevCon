// app/organizer/sessions/page.tsx
"use client";

import { useState } from "react";
import { CSVLink } from "react-csv";

type Speaker = {
  id: number;
  name: string;
  bio: string;
  email: string;
};

type Session = {
  id: number;
  title: string;
  description: string;
  speakerId: number;
  capacity: number;
  track: string;
  time: string; // Simplified for mock
  attendees: number;
};

type Event = {
  id: number;
  name: string;
  sessions: Session[];
  speakers: Speaker[];
};

const mockEvents: Event[] = [
  {
    id: 1,
    name: "AI & ML Conference 2026",
    speakers: [
      { id: 1, name: "Dr. Ali", bio: "Expert in AI healthcare solutions", email: "ali@example.com" },
      { id: 2, name: "Ms. Sara", bio: "ML engineer & workshop facilitator", email: "sara@example.com" },
    ],
    sessions: [
      { id: 1, title: "AI in Healthcare", description: "Explore AI applications in medicine", speakerId: 1, capacity: 100, track: "Track A", time: "10:00", attendees: 50 },
      { id: 2, title: "ML Workshop", description: "Hands-on ML session", speakerId: 2, capacity: 50, track: "Track B", time: "13:00", attendees: 20 },
    ],
  },
];

export default function SessionsPage() {
  const [events, setEvents] = useState(mockEvents);
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [isEditMode, setIsEditMode] = useState(false);

  const handleSelectEvent = (event: Event) => {
    setSelectedEvent(event);
    setIsEditMode(false);
  };

  const handleSessionChange = (sessionId: number, field: string, value: string | number) => {
    if (!selectedEvent) return;
    const updatedSessions = selectedEvent.sessions.map(s =>
      s.id === sessionId ? { ...s, [field]: value } : s
    );
    setSelectedEvent({ ...selectedEvent, sessions: updatedSessions });
  };

  const handleAddSession = () => {
    if (!selectedEvent) return;
    const newId = Math.max(...selectedEvent.sessions.map(s => s.id)) + 1;
    const newSession: Session = { id: newId, title: "", description: "", speakerId: selectedEvent.speakers[0].id, capacity: 50, track: "Track A", time: "09:00", attendees: 0 };
    setSelectedEvent({ ...selectedEvent, sessions: [...selectedEvent.sessions, newSession] });
    setIsEditMode(true);
  };

  const handleSaveSessions = async () => {
    if (!selectedEvent) return;
    setEvents(events.map(e => e.id === selectedEvent.id ? selectedEvent : e));
    setIsEditMode(false);

    try {
      const res = await fetch(`/api/events/${selectedEvent.id}/sessions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(selectedEvent.sessions),
      });
      if (!res.ok) throw new Error("Failed to save sessions");
      alert("Sessions saved successfully!");
    } catch (err) {
      console.error(err);
      alert("Error saving sessions.");
    }
  };

  const getSpeakerName = (speakerId: number) => selectedEvent?.speakers.find(s => s.id === speakerId)?.name || "";

  // Utility for rendering sessions by time
  const getSessionsByTrack = (track: string) => selectedEvent?.sessions.filter(s => s.track === track).sort((a, b) => a.time.localeCompare(b.time)) || [];

  return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-800">
      <header className="bg-mcs-red text-mcs-light p-6 shadow-md flex justify-between items-center">
        <h1 className="text-3xl font-bold">Sessions & Speakers Management</h1>
      </header>

      <main className="p-6 space-y-6">
        {/* Event Selector */}
        <section className="bg-white p-4 rounded shadow overflow-x-auto">
          <h2 className="text-xl font-bold mb-3 text-mcs-red">Select Event</h2>
          <div className="flex gap-2 flex-wrap">
            {events.map(e => (
              <button key={e.id} onClick={() => handleSelectEvent(e)}
                className={`px-4 py-2 rounded ${selectedEvent?.id === e.id ? "bg-mcs-yellow text-mcs-red" : "bg-gray-200 text-gray-700"} hover:bg-yellow-300`}>
                {e.name}
              </button>
            ))}
          </div>
        </section>

        {/* Sessions Table */}
        {selectedEvent && (
          <section className="bg-white p-4 rounded shadow overflow-x-auto">
            <div className="flex justify-between items-center mb-3">
              <h2 className="text-xl font-bold text-mcs-red">Sessions for {selectedEvent.name}</h2>
              <div className="flex flex-wrap gap-2">
                <CSVLink
                  data={selectedEvent.sessions.map(s => ({
                    title: s.title,
                    description: s.description,
                    speaker: getSpeakerName(s.speakerId),
                    track: s.track,
                    time: s.time,
                    capacity: s.capacity,
                    attendees: s.attendees,
                  }))}
                  filename={`${selectedEvent.name}-sessions.csv`}
                  className="px-4 py-2 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400"
                >
                  Export CSV
                </CSVLink>

                <button onClick={() => alert("Live Poll feature coming soon!")} className="px-4 py-2 bg-mcs-red text-mcs-light rounded hover:bg-red-700">Live Poll</button>
                <button onClick={() => alert("Q&A feature coming soon!")} className="px-4 py-2 bg-mcs-red text-mcs-light rounded hover:bg-red-700">Q&A</button>
                <button onClick={() => alert("Calendar export feature coming soon!")} className="px-4 py-2 bg-mcs-red text-mcs-light rounded hover:bg-red-700">Export to Calendar (.ics)</button>

                {!isEditMode ? (
                  <button onClick={() => setIsEditMode(true)} className="px-4 py-2 bg-mcs-red text-mcs-light rounded hover:bg-red-700">Edit Sessions</button>
                ) : (
                  <>
                    <button onClick={handleSaveSessions} className="px-4 py-2 bg-mcs-red text-mcs-light rounded hover:bg-red-700">Save Changes</button>
                    <button onClick={handleAddSession} className="px-4 py-2 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400">Add Session</button>
                  </>
                )}
              </div>
            </div>

            <table className="w-full table-auto border-collapse mb-6">
              <thead>
                <tr className="bg-gray-200 text-gray-700">
                  <th className="border px-4 py-2">Title</th>
                  <th className="border px-4 py-2">Description</th>
                  <th className="border px-4 py-2">Speaker</th>
                  <th className="border px-4 py-2">Track</th>
                  <th className="border px-4 py-2">Time</th>
                  <th className="border px-4 py-2">Capacity</th>
                  <th className="border px-4 py-2">Attendees</th>
                </tr>
              </thead>
              <tbody>
                {selectedEvent.sessions.map(s => (
                  <tr key={s.id} className="hover:bg-gray-100">
                    <td className="border px-2 py-1">{isEditMode ? <input type="text" value={s.title} onChange={e => handleSessionChange(s.id, "title", e.target.value)} className="w-32 p-1 border rounded focus:ring-2 focus:ring-mcs-red" /> : s.title}</td>
                    <td className="border px-2 py-1">{isEditMode ? <input type="text" value={s.description} onChange={e => handleSessionChange(s.id, "description", e.target.value)} className="w-48 p-1 border rounded focus:ring-2 focus:ring-mcs-red" /> : s.description}</td>
                    <td className="border px-2 py-1">{isEditMode ? <select value={s.speakerId} onChange={e => handleSessionChange(s.id, "speakerId", Number(e.target.value))} className="w-32 p-1 border rounded focus:ring-2 focus:ring-mcs-red">{selectedEvent.speakers.map(sp => <option key={sp.id} value={sp.id}>{sp.name}</option>)}</select> : getSpeakerName(s.speakerId)}</td>
                    <td className="border px-2 py-1">{isEditMode ? <input type="text" value={s.track} onChange={e => handleSessionChange(s.id, "track", e.target.value)} className="w-24 p-1 border rounded focus:ring-2 focus:ring-mcs-red" /> : s.track}</td>
                    <td className="border px-2 py-1">{isEditMode ? <input type="text" value={s.time} onChange={e => handleSessionChange(s.id, "time", e.target.value)} className="w-20 p-1 border rounded focus:ring-2 focus:ring-mcs-red" /> : s.time}</td>
                    <td className="border px-2 py-1">{isEditMode ? <input type="number" value={s.capacity} onChange={e => handleSessionChange(s.id, "capacity", Number(e.target.value))} className="w-16 p-1 border rounded focus:ring-2 focus:ring-mcs-red" /> : s.capacity}</td>
                    <td className="border px-2 py-1">{s.attendees}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Calendar Layout */}
            <h3 className="text-lg font-bold mb-2 text-mcs-red">Event Calendar</h3>
            <div className="grid grid-cols-3 gap-4">
              {["Track A", "Track B", "Track C"].map(track => (
                <div key={track} className="bg-gray-50 p-2 rounded shadow">
                  <h4 className="font-semibold text-mcs-red mb-2">{track}</h4>
                  {getSessionsByTrack(track).length === 0 ? (
                    <p className="text-gray-500 text-sm">No sessions</p>
                  ) : (
                    getSessionsByTrack(track).map(s => (
                      <div key={s.id} className="bg-white p-2 mb-2 rounded border">
                        <p className="font-semibold">{s.title}</p>
                        <p className="text-sm">{s.time}</p>
                        <p className="text-sm text-gray-600">{getSpeakerName(s.speakerId)}</p>
                      </div>
                    ))
                  )}
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}
