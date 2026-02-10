"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { CSVLink } from "react-csv";

type TicketType = { type: string; price: number; sold: number };
type Session = { id: number; title: string; speaker: string; time: string };
type Attendee = { id: number; name: string; email: string; checkedIn: boolean };

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
    ],
    attendees: [
      { id: 1, name: "Akrash", email: "akrash@example.com", checkedIn: false },
    ],
  },
];

export default function EventManagementPage() {
  const router = useRouter();
  const [events, setEvents] = useState(mockEvents);
  const [selectedEvent, setSelectedEvent] = useState<typeof mockEvents[0] | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [role] = useState<"superadmin" | "organizer" | "staff">("superadmin");

  // Form states for dynamic tickets and sessions
  const [tickets, setTickets] = useState<TicketType[]>([{ type: "", price: 0, sold: 0 }]);
  const [sessions, setSessions] = useState<Session[]>([{ id: Date.now(), title: "", speaker: "", time: "" }]);

  const handleEdit = (event: typeof mockEvents[0]) => {
    setSelectedEvent(event);
    setTickets(event.ticketTypes);
    setSessions(event.sessions);
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

    const newEvent = {
      id: selectedEvent?.id || Date.now(),
      name: formData.get("name") as string,
      description: formData.get("description") as string,
      startDate: formData.get("startDate") as string,
      endDate: formData.get("endDate") as string,
      venue: formData.get("venue") as string,
      ticketTypes: tickets,
      sessions: sessions.filter(s => s.title && s.speaker),
      attendees: selectedEvent?.attendees || [],
    };

    if (selectedEvent) {
      setEvents(events.map(e => (e.id === selectedEvent.id ? newEvent : e)));
    } else {
      setEvents([...events, newEvent]);
    }

    setShowForm(false);
    setSelectedEvent(null);
    setTickets([{ type: "", price: 0, sold: 0 }]);
    setSessions([{ id: Date.now(), title: "", speaker: "", time: "" }]);
  };

  const handleCheckInToggle = (eventId: number, attendeeId: number) => {
    setEvents(events.map(e => {
      if (e.id === eventId) {
        e.attendees = e.attendees.map(a => a.id === attendeeId ? { ...a, checkedIn: !a.checkedIn } : a);
      }
      return e;
    }));
  };

  const addTicket = () => setTickets([...tickets, { type: "", price: 0, sold: 0 }]);
  const removeTicket = (index: number) => setTickets(tickets.filter((_, i) => i !== index));

  const addSession = () => setSessions([...sessions, { id: Date.now(), title: "", speaker: "", time: "" }]);
  const removeSession = (id: number) => setSessions(sessions.filter(s => s.id !== id));

  return (
    <div className="min-h-screen bg-gray-light font-sans text-gray-dark">
      <header className="bg-mcs-red text-mcs-light p-6 shadow-md flex justify-between items-center">
        <h1 className="text-3xl font-bold">Event Management</h1>
        <button onClick={() => { setShowForm(true); setSelectedEvent(null); }} className="px-4 py-2 bg-mcs-yellow text-mcs-red font-semibold rounded hover:bg-yellow-400">Create Event</button>
      </header>

      <main className="p-6 space-y-6">

        {/* Events Table */}
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
                    <button onClick={() => handleEdit(e)} className="px-2 py-1 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400">Edit</button>
                    {role === "superadmin" && <button onClick={() => handleDelete(e.id)} className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-700">Delete</button>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        {/* Event Form */}
        {showForm && (
          <section className="bg-white p-6 rounded shadow">
            <h2 className="text-xl font-bold mb-4 text-mcs-red">{selectedEvent ? "Edit Event" : "Create Event"}</h2>
            <form onSubmit={handleFormSubmit} className="space-y-4">

              <input name="name" placeholder="Event Name" defaultValue={selectedEvent?.name || ""} className="w-full p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
              <input name="description" placeholder="Description" defaultValue={selectedEvent?.description || ""} className="w-full p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
              <div className="flex gap-4">
                <input type="date" name="startDate" defaultValue={selectedEvent?.startDate || ""} className="p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                <input type="date" name="endDate" defaultValue={selectedEvent?.endDate || ""} className="p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />
              </div>
              <input name="venue" placeholder="Venue" defaultValue={selectedEvent?.venue || ""} className="w-full p-3 rounded border focus:outline-none focus:ring-2 focus:ring-mcs-red" />

              {/* Ticket Types */}
              <div className="space-y-2">
                <h3 className="font-semibold text-gray-dark">Ticket Types</h3>
                {tickets.map((t, i) => (
  <div key={i} className="flex gap-2">
    <input
      type="text"
      placeholder="Type (e.g., Early Bird)"
      value={t.type}
      onChange={e => { tickets[i].type = e.target.value; setTickets([...tickets]); }}
      className="p-2 rounded border w-1/3 focus:outline-none focus:ring-2 focus:ring-mcs-red"
    />
    <input
      type="number"
      placeholder="Price"
      value={t.price}
      onChange={e => { tickets[i].price = Number(e.target.value); setTickets([...tickets]); }}
      className="p-2 rounded border w-1/6 focus:outline-none focus:ring-2 focus:ring-mcs-red"
    />
    <input
      type="date"
      placeholder="Early Bird Start"
      value={t.startDate || ""}
      onChange={e => { tickets[i].startDate = e.target.value; setTickets([...tickets]); }}
      className="p-2 rounded border w-1/6 focus:outline-none focus:ring-2 focus:ring-mcs-red"
    />
    <input
      type="date"
      placeholder="Early Bird End"
      value={t.endDate || ""}
      onChange={e => { tickets[i].endDate = e.target.value; setTickets([...tickets]); }}
      className="p-2 rounded border w-1/6 focus:outline-none focus:ring-2 focus:ring-mcs-red"
    />
    <button type="button" onClick={() => removeTicket(i)} className="px-2 bg-red-500 text-white rounded hover:bg-red-700">Remove</button>
  </div>
))}

                <button type="button" onClick={addTicket} className="px-3 py-1 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400">Add Ticket Type</button>
              </div>

              {/* Sessions */}
              <div className="space-y-2">
                <h3 className="font-semibold text-gray-dark">Sessions</h3>
                {sessions.map((s, i) => (
                  <div key={s.id} className="flex gap-2">
                    <input type="text" placeholder="Title" value={s.title} onChange={e => { sessions[i].title = e.target.value; setSessions([...sessions]); }} className="p-2 rounded border w-1/3 focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                    <input type="text" placeholder="Speaker" value={s.speaker} onChange={e => { sessions[i].speaker = e.target.value; setSessions([...sessions]); }} className="p-2 rounded border w-1/3 focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                    <input type="time" placeholder="Time" value={s.time} onChange={e => { sessions[i].time = e.target.value; setSessions([...sessions]); }} className="p-2 rounded border w-1/6 focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                    <button type="button" onClick={() => removeSession(s.id)} className="px-2 bg-red-500 text-white rounded hover:bg-red-700">Remove</button>
                  </div>
                ))}
                <button type="button" onClick={addSession} className="px-3 py-1 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400">Add Session</button>
              </div>

              <div className="flex gap-2 mt-4">
                <button type="submit" className="px-4 py-2 bg-mcs-red text-mcs-light rounded hover:bg-red-700">Save</button>
                <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Cancel</button>
              </div>
            </form>
          </section>
        )}

        {/* Selected Event Details */}
        {selectedEvent && (
          <section className="bg-white p-4 rounded shadow space-y-4">
            <h2 className="text-xl font-bold mb-2 text-mcs-red">Attendees</h2>
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
