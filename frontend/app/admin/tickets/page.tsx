"use client";

import { useState } from "react";
import { CSVLink } from "react-csv";

type Ticket = {
  id: number;
  type: string;
  price: number;
  earlyBirdPrice?: number;
  groupDiscount?: string;
  sold: number;
  revenue: number;
};

type Event = {
  id: number;
  name: string;
  tickets: Ticket[];
};

const mockEvents: Event[] = [
  {
    id: 1,
    name: "AI & ML Conference 2026",
    tickets: [
      { id: 1, type: "Standard", price: 100, earlyBirdPrice: 80, groupDiscount: "10% for 5+", sold: 50, revenue: 5000 },
      { id: 2, type: "VIP", price: 250, earlyBirdPrice: 200, groupDiscount: "15% for 3+", sold: 20, revenue: 5000 },
      { id: 3, type: "Student", price: 50, earlyBirdPrice: 40, groupDiscount: "10% for 5+", sold: 30, revenue: 1500 },
    ],
  },
  {
    id: 2,
    name: "Web Dev Workshop",
    tickets: [
      { id: 4, type: "General", price: 75, earlyBirdPrice: 60, groupDiscount: "10% for 3+", sold: 40, revenue: 3000 },
    ],
  },
];

export default function TicketManagementPage() {
  const [events, setEvents] = useState(mockEvents);
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [isEditMode, setIsEditMode] = useState(false);

  const handleSelectEvent = (event: Event) => {
    setSelectedEvent(event);
    setIsEditMode(false);
  };

  const handleTicketChange = (ticketId: number, field: string, value: string | number) => {
    if (!selectedEvent) return;
    const updatedTickets = selectedEvent.tickets.map(t =>
      t.id === ticketId ? { ...t, [field]: value } : t
    );
    setSelectedEvent({ ...selectedEvent, tickets: updatedTickets });
  };

  const handleAddTicket = () => {
    if (!selectedEvent) return;
    const newId = Math.max(...selectedEvent.tickets.map(t => t.id)) + 1;
    const newTicket: Ticket = { id: newId, type: "", price: 0, earlyBirdPrice: 0, groupDiscount: "", sold: 0, revenue: 0 };
    setSelectedEvent({ ...selectedEvent, tickets: [...selectedEvent.tickets, newTicket] });
  };

  const handleSaveChanges = async () => {
    if (!selectedEvent) return;

    // Update the global events state
    setEvents(events.map(e => e.id === selectedEvent.id ? selectedEvent : e));
    setIsEditMode(false);

    // MOCK API CALL
    try {
      const res = await fetch(`/api/events/${selectedEvent.id}/tickets`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(selectedEvent.tickets),
      });
      if (!res.ok) throw new Error("Failed to save tickets");
      alert("Tickets saved successfully!");
    } catch (err) {
      console.error(err);
      alert("Error saving tickets.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-800">
      <header className="bg-mcs-red text-mcs-light p-6 shadow-md flex justify-between items-center">
        <h1 className="text-3xl font-bold">Ticket & Payment Management</h1>
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
              <h2 className="text-xl font-bold text-mcs-red">Tickets for {selectedEvent.name}</h2>
              <div className="flex gap-2">
                <CSVLink
                  data={selectedEvent.tickets.map(t => ({
                    type: t.type,
                    price: t.price,
                    earlyBirdPrice: t.earlyBirdPrice,
                    groupDiscount: t.groupDiscount,
                    sold: t.sold,
                    revenue: t.revenue
                  }))}
                  filename={`${selectedEvent.name}-tickets.csv`}
                  className="px-4 py-2 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400"
                >
                  Export CSV
                </CSVLink>

                {!isEditMode ? (
                  <button onClick={() => setIsEditMode(true)}
                    className="px-4 py-2 bg-mcs-red text-mcs-light rounded hover:bg-red-700">
                    Edit Tickets
                  </button>
                ) : (
                  <button onClick={handleSaveChanges}
                    className="px-4 py-2 bg-mcs-red text-mcs-light rounded hover:bg-red-700">
                    Save Changes
                  </button>
                )}

                {isEditMode && (
                  <button onClick={handleAddTicket}
                    className="px-4 py-2 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400">
                    Add Ticket Type
                  </button>
                )}
              </div>
            </div>

            <table className="w-full table-auto border-collapse">
              <thead>
                <tr className="bg-gray-200 text-gray-700">
                  <th className="border px-4 py-2">Ticket Type</th>
                  <th className="border px-4 py-2">Price ($)</th>
                  <th className="border px-4 py-2">Early Bird Price ($)</th>
                  <th className="border px-4 py-2">Group Discount</th>
                  <th className="border px-4 py-2">Sold</th>
                  <th className="border px-4 py-2">Revenue ($)</th>
                </tr>
              </thead>
              <tbody>
                {selectedEvent.tickets.map(t => (
                  <tr key={t.id} className="hover:bg-gray-100">
                    <td className="border px-4 py-2">
                      {isEditMode ? (
                        <input type="text" value={t.type} onChange={e => handleTicketChange(t.id, 'type', e.target.value)}
                          className="w-32 p-1 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                      ) : t.type}
                    </td>
                    <td className="border px-4 py-2">
                      {isEditMode ? (
                        <input type="number" value={t.price} onChange={e => handleTicketChange(t.id, 'price', Number(e.target.value))}
                          className="w-20 p-1 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                      ) : t.price}
                    </td>
                    <td className="border px-4 py-2">
                      {isEditMode ? (
                        <input type="number" value={t.earlyBirdPrice} onChange={e => handleTicketChange(t.id, 'earlyBirdPrice', Number(e.target.value))}
                          className="w-20 p-1 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                      ) : t.earlyBirdPrice}
                    </td>
                    <td className="border px-4 py-2">
                      {isEditMode ? (
                        <input type="text" value={t.groupDiscount} onChange={e => handleTicketChange(t.id, 'groupDiscount', e.target.value)}
                          className="w-32 p-1 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red" />
                      ) : t.groupDiscount}
                    </td>
                    <td className="border px-4 py-2">{t.sold}</td>
                    <td className="border px-4 py-2">{t.revenue}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="mt-4">
              <button className="px-4 py-2 bg-mcs-red text-mcs-light rounded hover:bg-red-700">Mock Payment Integration</button>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}
