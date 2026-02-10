"use client";

import { useState } from "react";
import { CSVLink } from "react-csv";
import { Line, Pie } from "react-chartjs-2";
import "chart.js/auto";

const events = [
  {
    id: "e1",
    name: "AI & ML Conference 2026",
    tickets: [
      { type: "VIP", price: 250 },
      { type: "Standard", price: 120 },
      { type: "Student", price: 50 },
    ],
  },
  {
    id: "e2",
    name: "Cyber Security Summit",
    tickets: [
      { type: "VIP", price: 200 },
      { type: "Standard", price: 100 },
    ],
  },
];

const attendeeBase = {
  name: "Akrash Noman",
  seatType: "-",
  seatNumber: "-",
  agenda: [
    { title: "AI in Healthcare", time: "10:00 AM", status: "Booked" },
    { title: "ML Workshop", time: "1:00 PM", status: "Available" },
  ],
  networking: [
    { name: "Ali Khan", company: "TechCorp", similarity: 92 },
    { name: "Sara Ahmed", company: "DataLabs", similarity: 85 },
  ],
  trends: {
    labels: ["Day 1", "Day 2", "Day 3"],
    data: [50, 80, 120],
  },
};

export default function AttendeePage() {
  const [agenda, setAgenda] = useState(attendeeBase.agenda);
  const [pollOpen, setPollOpen] = useState(false);
  const [qaText, setQaText] = useState("");
  const [selectedEvent, setSelectedEvent] = useState<any>(null);
  const [selectedTicket, setSelectedTicket] = useState<any>(null);
  const [paymentProof, setPaymentProof] = useState<File | null>(null);
  const [tickets, setTickets] = useState<any[]>([]);

  const toggleSession = (i: number) => {
    const copy = [...agenda];
    copy[i].status = copy[i].status === "Booked" ? "Available" : "Booked";
    setAgenda(copy);
  };

  const exportCalendar = () => {
    const content = `
BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:AI in Healthcare
DTSTART:20260301T100000
DTEND:20260301T110000
END:VEVENT
END:VCALENDAR`;
    const blob = new Blob([content], { type: "text/calendar" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "agenda.ics";
    link.click();
  };

  const submitBooking = () => {
    if (!selectedEvent || !selectedTicket || !paymentProof) {
      alert("Please select event, ticket type and upload payment proof");
      return;
    }

    setTickets([
      ...tickets,
      {
        event: selectedEvent.name,
        type: selectedTicket.type,
        price: selectedTicket.price,
        status: "Pending Verification",
        qr: "-",
      },
    ]);

    setSelectedEvent(null);
    setSelectedTicket(null);
    setPaymentProof(null);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 text-gray-800">
      <h1 className="text-3xl font-bold mb-6">
        Welcome, {attendeeBase.name}
      </h1>

      <div className="grid md:grid-cols-4 gap-4 mb-6">
        <Card title="Seat Type" value={attendeeBase.seatType} />
        <Card title="Seat Number" value={attendeeBase.seatNumber} />
        <Card title="Tickets" value={tickets.length} />
        <Card
          title="Sessions Booked"
          value={agenda.filter(a => a.status === "Booked").length}
        />
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white p-4 rounded shadow">
          <Line
            data={{
              labels: attendeeBase.trends.labels,
              datasets: [
                {
                  label: "Registrations",
                  data: attendeeBase.trends.data,
                },
              ],
            }}
          />
        </div>
        <div className="bg-white p-4 rounded shadow">
          <Pie
            data={{
              labels: ["VIP", "Standard", "Student"],
              datasets: [{ data: [30, 50, 20] }],
            }}
          />
        </div>
      </div>

      <section className="bg-white p-4 rounded shadow mb-6">
        <h2 className="text-xl font-bold mb-4">Book Ticket</h2>

        <div className="mb-4">
          <p className="font-semibold mb-2">Select Event</p>
          {events.map(event => (
            <button
              key={event.id}
              onClick={() => {
                setSelectedEvent(event);
                setSelectedTicket(null);
              }}
              className={`w-full text-left p-3 mb-2 rounded border ${
                selectedEvent?.id === event.id
                  ? "bg-yellow-100 border-yellow-400"
                  : "bg-gray-50"
              }`}
            >
              {event.name}
            </button>
          ))}
        </div>

        {selectedEvent && (
          <div className="mb-4">
            <p className="font-semibold mb-2">Select Ticket Type</p>
            {selectedEvent.tickets.map((ticket: any, i: number) => (
              <button
                key={i}
                onClick={() => setSelectedTicket(ticket)}
                className={`w-full text-left p-3 mb-2 rounded border ${
                  selectedTicket?.type === ticket.type
                    ? "bg-green-100 border-green-400"
                    : "bg-gray-50"
                }`}
              >
                {ticket.type} — ${ticket.price}
              </button>
            ))}
          </div>
        )}

        {selectedTicket && (
          <div className="mb-4">
            <p className="mb-2">
              Pay <strong>${selectedTicket.price}</strong> to
            </p>
            <p className="font-mono bg-gray-100 p-2 rounded mb-3">
              JazzCash / EasyPaisa: 0300-1234567
            </p>
            <input
              type="file"
              accept="image/*"
              onChange={e =>
                setPaymentProof(e.target.files?.[0] || null)
              }
            />
          </div>
        )}

        {selectedTicket && (
          <button
            onClick={submitBooking}
            className="w-full bg-red-600 text-white py-3 rounded font-bold"
          >
            Submit Booking
          </button>
        )}
      </section>

      <section className="bg-white p-4 rounded shadow mb-6">
        <h2 className="text-xl font-bold mb-3">My Tickets</h2>
        {tickets.length === 0 && <p>No tickets booked</p>}
        {tickets.map((t, i) => (
          <div key={i} className="border p-3 rounded mb-2 bg-gray-50">
            <p>{t.event}</p>
            <p>Type: {t.type}</p>
            <p>Price: ${t.price}</p>
            <p className="text-yellow-600 font-semibold">
              Status: {t.status}
            </p>
          </div>
        ))}
      </section>

      <section className="bg-white p-4 rounded shadow mb-6">
        <h2 className="text-xl font-bold mb-3">My Agenda</h2>
        {agenda.map((s, i) => (
          <div key={i} className="flex justify-between border-b py-2">
            <span>
              {s.title} ({s.time})
            </span>
            <button
              onClick={() => toggleSession(i)}
              className="px-3 py-1 bg-yellow-400 rounded"
            >
              {s.status}
            </button>
          </div>
        ))}
      </section>

      <section className="bg-white p-4 rounded shadow mb-6">
        <h2 className="text-xl font-bold mb-3">People You Should Meet</h2>
        {attendeeBase.networking.map((n, i) => (
          <div key={i} className="border p-3 rounded mb-2">
            <p>
              {n.name} — {n.company}
            </p>
            <p>Match: {n.similarity}%</p>
          </div>
        ))}
      </section>

      <section className="bg-white p-4 rounded shadow flex gap-4 flex-wrap mb-6">
        <button
          onClick={() => setPollOpen(true)}
          className="px-4 py-2 bg-red-600 text-white rounded"
        >
          Live Poll
        </button>
        <button
          onClick={() => alert(qaText || "Question submitted")}
          className="px-4 py-2 bg-red-600 text-white rounded"
        >
          Q&A
        </button>
        <button
          onClick={exportCalendar}
          className="px-4 py-2 bg-red-600 text-white rounded"
        >
          Export Calendar
        </button>
        <CSVLink
          data={tickets}
          filename="attendee.csv"
          className="px-4 py-2 bg-yellow-400 rounded"
        >
          Export CSV
        </CSVLink>
      </section>

      {pollOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
          <div className="bg-white p-6 rounded w-full max-w-md">
            <h3 className="font-bold mb-3">Live Poll</h3>
            <button
              onClick={() => setPollOpen(false)}
              className="w-full bg-red-600 text-white py-2 rounded"
            >
              Submit Vote
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function Card({
  title,
  value,
}: {
  title: string;
  value: string | number;
}) {
  return (
    <div className="bg-white p-4 rounded shadow">
      <p className="text-sm">{title}</p>
      <p className="text-xl font-bold">{value}</p>
    </div>
  );
}
