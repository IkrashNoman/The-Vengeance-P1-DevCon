// app/admin/attendees/page.tsx
"use client";

import { useState } from "react";
import { CSVLink } from "react-csv";

type Attendee = { id: number; name: string; email: string; session: string; checkedIn: boolean };
type Event = { id: number; name: string; attendees: Attendee[] };

const mockEvents: Event[] = [
  {
    id: 1,
    name: "AI & ML Conference 2026",
    attendees: [
      { id: 1, name: "Akrash Noman", email: "akrash@example.com", session: "AI in Healthcare", checkedIn: false },
      { id: 2, name: "Ali Khan", email: "ali@example.com", session: "ML Workshop", checkedIn: true },
      { id: 3, name: "Sara Ahmed", email: "sara@example.com", session: "AI in Healthcare", checkedIn: false },
    ],
  },
  {
    id: 2,
    name: "Web Dev Workshop",
    attendees: [
      { id: 4, name: "John Doe", email: "john@example.com", session: "React Basics", checkedIn: true },
    ],
  },
];

export default function AttendeeManagementPage() {
  const [events, setEvents] = useState(mockEvents);
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [search, setSearch] = useState("");

  const handleSelectEvent = (event: Event) => {
    setSelectedEvent(event);
    setSearch("");
  };

  const toggleCheckIn = (attendeeId: number) => {
    if (!selectedEvent) return;
    selectedEvent.attendees = selectedEvent.attendees.map(a => a.id === attendeeId ? { ...a, checkedIn: !a.checkedIn } : a);
    setEvents([...events]);
  };

  const filteredAttendees = selectedEvent?.attendees.filter(a =>
    a.name.toLowerCase().includes(search.toLowerCase()) ||
    a.email.toLowerCase().includes(search.toLowerCase()) ||
    a.session.toLowerCase().includes(search.toLowerCase())
  ) || [];

  return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-800">
      <header className="bg-mcs-red text-mcs-light p-6 shadow-md flex justify-between items-center">
        <h1 className="text-3xl font-bold">Attendee Management</h1>
      </header>

      <main className="p-6 space-y-6">
        <section className="bg-white p-4 rounded shadow overflow-x-auto">
          <h2 className="text-xl font-bold mb-3 text-mcs-red">Select Event</h2>
          <div className="flex gap-2 flex-wrap">
            {events.map(e => (
              <button key={e.id} onClick={() => handleSelectEvent(e)}
                className={`px-4 py-2 rounded ${selectedEvent?.id === e.id ? 'bg-mcs-yellow text-mcs-red' : 'bg-gray-200 text-gray-700'} hover:bg-yellow-300`}>
                {e.name}
              </button>
            ))}
          </div>
        </section>

        {selectedEvent && (
          <section className="bg-white p-4 rounded shadow overflow-x-auto">
            <div className="flex justify-between items-center mb-3">
              <h2 className="text-xl font-bold text-mcs-red">Attendees for {selectedEvent.name}</h2>
              <CSVLink data={selectedEvent.attendees} filename={`${selectedEvent.name}-attendees.csv`}
                className="px-4 py-2 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400">
                Export CSV
              </CSVLink>
            </div>

            <input
              type="text"
              placeholder="Search by name, email, or session"
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="w-full mb-3 p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red"
            />

            <table className="w-full table-auto border-collapse">
              <thead>
                <tr className="bg-gray-200 text-gray-700">
                  <th className="border px-4 py-2">Name</th>
                  <th className="border px-4 py-2">Email</th>
                  <th className="border px-4 py-2">Session</th>
                  <th className="border px-4 py-2">Checked In</th>
                  <th className="border px-4 py-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredAttendees.map(a => (
                  <tr key={a.id} className="hover:bg-gray-100">
                    <td className="border px-4 py-2">{a.name}</td>
                    <td className="border px-4 py-2">{a.email}</td>
                    <td className="border px-4 py-2">{a.session}</td>
                    <td className="border px-4 py-2">{a.checkedIn ? "Yes" : "No"}</td>
                    <td className="border px-4 py-2 space-x-2">
                      <button onClick={() => toggleCheckIn(a.id)}
                        className="px-2 py-1 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400">
                        {a.checkedIn ? "Undo Check-In" : "Check-In"}
                      </button>
                      <button className="px-2 py-1 bg-gray-300 rounded hover:bg-gray-400">QR Code</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        )}
      </main>
    </div>
  );
}
