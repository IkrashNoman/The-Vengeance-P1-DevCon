// app/admin/sessions/page.tsx
"use client";

import { useState } from "react";
import { CSVLink } from "react-csv";

type Attendee = { id: number; name: string; email: string; checkedIn: boolean };
type Session = { id: number; title: string; speaker: string; startTime: string; endTime: string; room: string; capacity: number; attendees: Attendee[] };
type Event = { id: number; name: string; sessions: Session[] };

const mockEvents: Event[] = [
  {
    id: 1,
    name: "AI & ML Conference 2026",
    sessions: [
      { id: 1, title: "AI in Healthcare", speaker: "Dr. Ali", startTime: "10:00", endTime: "11:00", room: "Auditorium", capacity: 50, attendees: [{ id: 1, name: "Akrash", email: "akrash@example.com", checkedIn: false }] },
      { id: 2, title: "ML Workshop", speaker: "Ms. Sara", startTime: "11:30", endTime: "13:00", room: "Lab 1", capacity: 30, attendees: [{ id: 2, name: "Ali", email: "ali@example.com", checkedIn: true }] },
    ],
  },
  {
    id: 2,
    name: "Web Dev Workshop",
    sessions: [
      { id: 3, title: "React Basics", speaker: "Ms. Sara", startTime: "10:00", endTime: "12:00", room: "Lab 2", capacity: 30, attendees: [{ id: 3, name: "John", email: "john@example.com", checkedIn: false }] },
    ],
  },
];

export default function SessionManagementPage() {
  const [events, setEvents] = useState(mockEvents);
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingSession, setEditingSession] = useState<Session | null>(null);

  const handleSelectEvent = (event: Event) => {
    setSelectedEvent(event);
    setShowForm(false);
    setEditingSession(null);
  };

  const handleEditSession = (session: Session) => {
    setEditingSession(session);
    setShowForm(true);
  };

  const handleDeleteSession = (sessionId: number) => {
    if (!selectedEvent) return;
    if (confirm("Are you sure you want to delete this session?")) {
      selectedEvent.sessions = selectedEvent.sessions.filter(s => s.id !== sessionId);
      setEvents([...events]);
    }
  };

  const handleFormSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!selectedEvent) return;

    const formData = new FormData(e.currentTarget);
    const newSession: Session = {
      id: editingSession?.id || Math.random(),
      title: formData.get("title") as string,
      speaker: formData.get("speaker") as string,
      startTime: formData.get("startTime") as string,
      endTime: formData.get("endTime") as string,
      room: formData.get("room") as string,
      capacity: Number(formData.get("capacity")),
      attendees: editingSession?.attendees || [],
    };

    // Conflict Detection (mock)
    const conflict = selectedEvent.sessions.some(s => 
      s.id !== newSession.id &&
      s.room === newSession.room &&
      ((newSession.startTime >= s.startTime && newSession.startTime < s.endTime) ||
       (newSession.endTime > s.startTime && newSession.endTime <= s.endTime))
    );

    if (conflict) {
      alert("Conflict detected: another session is scheduled in the same room at this time.");
      return;
    }

    if (editingSession) {
      selectedEvent.sessions = selectedEvent.sessions.map(s => s.id === editingSession.id ? newSession : s);
    } else {
      selectedEvent.sessions.push(newSession);
    }

    setEvents([...events]);
    setShowForm(false);
    setEditingSession(null);
  };

  const toggleCheckIn = (session: Session, attendeeId: number) => {
    session.attendees = session.attendees.map(a => a.id === attendeeId ? { ...a, checkedIn: !a.checkedIn } : a);
    setEvents([...events]);
  };

  return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-800">
      <header className="bg-mcs-red text-mcs-light p-6 shadow-md flex justify-between items-center">
        <h1 className="text-3xl font-bold">Session Management</h1>
      </header>

      <main className="p-6 space-y-6">
        <section className="bg-white p-4 rounded shadow overflow-x-auto">
          <h2 className="text-xl font-bold mb-3 text-mcs-red">Select Event</h2>
          <div className="flex gap-2 flex-wrap">
            {events.map(e => (
              <button key={e.id} onClick={() => handleSelectEvent(e)} className={`px-4 py-2 rounded ${selectedEvent?.id === e.id ? 'bg-mcs-yellow text-mcs-red' : 'bg-gray-200 text-gray-700'} hover:bg-yellow-300`}>
                {e.name}
              </button>
            ))}
          </div>
        </section>

        {selectedEvent && (
          <>
            <section className="bg-white p-4 rounded shadow overflow-x-auto">
              <h2 className="text-xl font-bold mb-3 text-mcs-red">Sessions for {selectedEvent.name}</h2>
              <button onClick={() => { setShowForm(true); setEditingSession(null); }} className="px-3 py-1 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400 mb-3">Add Session</button>
              <table className="w-full table-auto border-collapse">
                <thead>
                  <tr className="bg-gray-200 text-gray-700">
                    <th className="border px-4 py-2">Title</th>
                    <th className="border px-4 py-2">Speaker</th>
                    <th className="border px-4 py-2">Start</th>
                    <th className="border px-4 py-2">End</th>
                    <th className="border px-4 py-2">Room</th>
                    <th className="border px-4 py-2">Capacity</th>
                    <th className="border px-4 py-2">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedEvent.sessions.map(s => (
                    <tr key={s.id} className="hover:bg-gray-100">
                      <td className="border px-4 py-2">{s.title}</td>
                      <td className="border px-4 py-2">{s.speaker}</td>
                      <td className="border px-4 py-2">{s.startTime}</td>
                      <td className="border px-4 py-2">{s.endTime}</td>
                      <td className="border px-4 py-2">{s.room}</td>
                      <td className="border px-4 py-2">{s.capacity}</td>
                      <td className="border px-4 py-2 space-x-2">
                        <button onClick={() => handleEditSession(s)} className="px-2 py-1 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400">Edit</button>
                        <button onClick={() => handleDeleteSession(s.id)} className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-700">Delete</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>

            {showForm && (
              <section className="bg-white p-6 rounded shadow">
                <h2 className="text-xl font-bold mb-4 text-mcs-red">{editingSession ? "Edit Session" : "Add Session"}</h2>
                <form onSubmit={handleFormSubmit} className="space-y-3">
                  <input name="title" placeholder="Session Title" defaultValue={editingSession?.title || ""} className="w-full p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                  <input name="speaker" placeholder="Speaker" defaultValue={editingSession?.speaker || ""} className="w-full p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                  <div className="flex gap-4">
                    <input type="time" name="startTime" defaultValue={editingSession?.startTime || ""} className="p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                    <input type="time" name="endTime" defaultValue={editingSession?.endTime || ""} className="p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                  </div>
                  <input name="room" placeholder="Room" defaultValue={editingSession?.room || ""} className="w-full p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                  <input type="number" name="capacity" placeholder="Capacity" defaultValue={editingSession?.capacity || 30} className="w-full p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                  <div className="flex gap-2">
                    <button type="submit" className="px-4 py-2 bg-mcs-red text-mcs-light rounded hover:bg-red-700">Save</button>
                    <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Cancel</button>
                  </div>
                </form>
              </section>
            )}

            {selectedEvent.sessions.map(session => (
              <section key={session.id} className="bg-white p-4 rounded shadow mt-4 overflow-x-auto">
                <h2 className="text-xl font-bold mb-2 text-mcs-red">{session.title} - Attendees</h2>
                <CSVLink data={session.attendees} filename={`${session.title}-attendees.csv`} className="px-4 py-2 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400 mb-2 inline-block">Export CSV</CSVLink>
                <table className="w-full table-auto border-collapse">
                  <thead>
                    <tr className="bg-gray-200 text-gray-700">
                      <th className="border px-4 py-2">Name</th>
                      <th className="border px-4 py-2">Email</th>
                      <th className="border px-4 py-2">Checked In</th>
                      <th className="border px-4 py-2">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {session.attendees.map(a => (
                      <tr key={a.id} className="hover:bg-gray-100">
                        <td className="border px-4 py-2">{a.name}</td>
                        <td className="border px-4 py-2">{a.email}</td>
                        <td className="border px-4 py-2">{a.checkedIn ? "Yes" : "No"}</td>
                        <td className="border px-4 py-2">
                          <button onClick={() => toggleCheckIn(session, a.id)} className="px-2 py-1 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400">{a.checkedIn ? "Undo Check-In" : "Check-In"}</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </section>
            ))}
          </>
        )}
      </main>
    </div>
  );
}
