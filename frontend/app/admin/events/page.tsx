// app/admin/events/page.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { CSVLink } from "react-csv";

const mockEvents = [
  {
    id: 1,
    name: "AI & ML Conference 2026",
    description: "Explore latest in AI and ML",
    startDate: "2026-03-15",
    endDate: "2026-03-17",
    venue: "MCS NUST Auditorium",
    ticketTypes: [
      { type: "Early Bird", price: 20, sold: 50 },
      { type: "Regular", price: 40, sold: 100 },
    ],
    sessions: [
      { id: 1, title: "AI in Healthcare", speaker: "Dr. Ali", time: "10:00 AM" },
      { id: 2, title: "ML Workshop", speaker: "Ms. Sara", time: "1:00 PM" },
    ],
    attendees: [
      { id: 1, name: "Akrash", email: "akrash@example.com", checkedIn: false },
      { id: 2, name: "Ali", email: "ali@example.com", checkedIn: true },
    ],
  },
  {
    id: 2,
    name: "Web Dev Workshop",
    description: "Modern web development practices",
    startDate: "2026-04-01",
    endDate: "2026-04-01",
    venue: "MCS Lab 1",
    ticketTypes: [
      { type: "Regular", price: 15, sold: 30 },
    ],
    sessions: [
      { id: 3, title: "React Basics", speaker: "Ms. Sara", time: "10:00 AM" },
    ],
    attendees: [
      { id: 3, name: "John", email: "john@example.com", checkedIn: false },
    ],
  },
];

export default function EventManagementPage() {
  const router = useRouter();
  const [events, setEvents] = useState(mockEvents);
  const [selectedEvent, setSelectedEvent] = useState<typeof mockEvents[0] | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [role] = useState<"superadmin" | "organizer" | "staff">("superadmin"); // Mock role

  const handleEdit = (event: typeof mockEvents[0]) => {
    setSelectedEvent(event);
    setShowForm(true);
  };

  const handleDelete = (id: number) => {
    if (confirm("Are you sure you want to delete this event?")) {
      setEvents(events.filter(e => e.id !== id));
    }
  };

  const handleFormSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const updatedEvent = {
      id: selectedEvent?.id || Math.random(),
      name: formData.get("name") as string,
      description: formData.get("description") as string,
      startDate: formData.get("startDate") as string,
      endDate: formData.get("endDate") as string,
      venue: formData.get("venue") as string,
      ticketTypes: [
        { type: "Regular", price: Number(formData.get("ticketPrice")), sold: 0 },
      ],
      sessions: [],
      attendees: [],
    };

    if (selectedEvent) {
      setEvents(events.map(e => e.id === selectedEvent.id ? updatedEvent : e));
    } else {
      setEvents([...events, updatedEvent]);
    }

    setShowForm(false);
    setSelectedEvent(null);
  };

  const handleCheckInToggle = (eventId: number, attendeeId: number) => {
    setEvents(events.map(e => {
      if (e.id === eventId) {
        e.attendees = e.attendees.map(a => a.id === attendeeId ? { ...a, checkedIn: !a.checkedIn } : a);
      }
      return e;
    }));
  };

  return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-800">
      <header className="bg-mcs-red text-mcs-light p-6 shadow-md flex justify-between items-center">
        <h1 className="text-3xl font-bold">Event Management</h1>
        <button onClick={() => { setShowForm(true); setSelectedEvent(null); }} className="px-4 py-2 bg-mcs-yellow text-mcs-red font-semibold rounded hover:bg-yellow-400">Create Event</button>
      </header>

      <main className="p-6 space-y-6">
        <section className="bg-white p-4 rounded shadow overflow-x-auto">
          <h2 className="text-xl font-bold mb-3 text-mcs-red">All Events</h2>
          <table className="w-full table-auto border-collapse">
            <thead>
              <tr className="bg-gray-200 text-gray-700">
                <th className="border px-4 py-2">Event Name</th>
                <th className="border px-4 py-2">Dates</th>
                <th className="border px-4 py-2">Venue</th>
                <th className="border px-4 py-2">Attendees</th>
                <th className="border px-4 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {events.map(e => (
                <tr key={e.id} className="hover:bg-gray-100">
                  <td className="border px-4 py-2">{e.name}</td>
                  <td className="border px-4 py-2">{e.startDate} - {e.endDate}</td>
                  <td className="border px-4 py-2">{e.venue}</td>
                  <td className="border px-4 py-2">{e.attendees.length}</td>
                  <td className="border px-4 py-2 space-x-2">
                    {(role === "superadmin" || role === "organizer" || role === "staff") && (
                      <button onClick={() => handleEdit(e)} className="px-2 py-1 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400">Edit</button>
                    )}
                    {role === "superadmin" && (
                      <button onClick={() => handleDelete(e.id)} className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-700">Delete</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        {showForm && (
          <section className="bg-white p-6 rounded shadow">
            <h2 className="text-xl font-bold mb-4 text-mcs-red">{selectedEvent ? "Edit Event" : "Create Event"}</h2>
            <form onSubmit={handleFormSubmit} className="space-y-3">
              <input name="name" placeholder="Event Name" defaultValue={selectedEvent?.name || ""} className="w-full p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
              <input name="description" placeholder="Description" defaultValue={selectedEvent?.description || ""} className="w-full p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
              <div className="flex gap-4">
                <input type="date" name="startDate" defaultValue={selectedEvent?.startDate || ""} className="p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                <input type="date" name="endDate" defaultValue={selectedEvent?.endDate || ""} className="p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
              </div>
              <input name="venue" placeholder="Venue" defaultValue={selectedEvent?.venue || ""} className="w-full p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
              <input type="number" name="ticketPrice" placeholder="Ticket Price" defaultValue={selectedEvent?.ticketTypes[0]?.price || ""} className="w-full p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
              <div className="flex gap-2">
                <button type="submit" className="px-4 py-2 bg-mcs-red text-mcs-light rounded hover:bg-red-700">Save</button>
                <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Cancel</button>
              </div>
            </form>
          </section>
        )}

        {selectedEvent && (
          <section className="bg-white p-4 rounded shadow space-y-4">
            <h2 className="text-xl font-bold mb-2 text-mcs-red">Sessions</h2>
            <table className="w-full table-auto border-collapse">
              <thead>
                <tr className="bg-gray-200 text-gray-700">
                  <th className="border px-4 py-2">Title</th>
                  <th className="border px-4 py-2">Speaker</th>
                  <th className="border px-4 py-2">Time</th>
                </tr>
              </thead>
              <tbody>
                {selectedEvent.sessions.map(s => (
                  <tr key={s.id} className="hover:bg-gray-100">
                    <td className="border px-4 py-2">{s.title}</td>
                    <td className="border px-4 py-2">{s.speaker}</td>
                    <td className="border px-4 py-2">{s.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <h2 className="text-xl font-bold mt-4 mb-2 text-mcs-red">Attendees</h2>
            <CSVLink data={selectedEvent.attendees} filename={`${selectedEvent.name}-attendees.csv`} className="px-4 py-2 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400 mb-2 inline-block">Export CSV</CSVLink>
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
                {selectedEvent.attendees.map(a => (
                  <tr key={a.id} className="hover:bg-gray-100">
                    <td className="border px-4 py-2">{a.name}</td>
                    <td className="border px-4 py-2">{a.email}</td>
                    <td className="border px-4 py-2">{a.checkedIn ? "Yes" : "No"}</td>
                    <td className="border px-4 py-2">
                      <button onClick={() => handleCheckInToggle(selectedEvent.id, a.id)} className="px-2 py-1 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400">{a.checkedIn ? "Undo Check-In" : "Check-In"}</button>
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
