// app/attendee/page.tsx
"use client";

import { useState } from "react";
import { CSVLink } from "react-csv";
import { Line, Pie } from "react-chartjs-2";
import "chart.js/auto";

// ---------------- Mock Data ----------------
const attendee = {
  name: "Akrash Noman",
  seatType: "VIP",
  seatNumber: "A-12",
  tickets: [
    {
      event: "AI & ML Conference 2026",
      type: "VIP",
      price: 250,
      qr: "QR123ABC",
    },
  ],
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

// ---------------- Page ----------------
export default function AttendeePage() {
  const [agenda, setAgenda] = useState(attendee.agenda);
  const [pollOpen, setPollOpen] = useState(false);
  const [question, setQuestion] = useState("");

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

  return (
    <div className="min-h-screen bg-gray-100 p-6 text-gray-800">
      <h1 className="text-3xl font-bold mb-6">Welcome, {attendee.name}</h1>

      {/* Summary */}
      <div className="grid md:grid-cols-4 gap-4 mb-6">
        <Card title="Seat Type" value={attendee.seatType} />
        <Card title="Seat Number" value={attendee.seatNumber} />
        <Card title="Tickets" value={attendee.tickets.length} />
        <Card title="Sessions Booked" value={agenda.filter(a => a.status === "Booked").length} />
      </div>

      {/* Charts */}
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white p-4 rounded shadow">
          <Line
            data={{
              labels: attendee.trends.labels,
              datasets: [{ label: "Registrations", data: attendee.trends.data }],
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

      {/* Tickets */}
      <section className="bg-white p-4 rounded shadow mb-6">
        <h2 className="text-xl font-bold mb-3">My Ticket</h2>
        {attendee.tickets.map((t, i) => (
          <div key={i} className="border p-3 rounded bg-gray-50">
            <p>{t.event}</p>
            <p>Type: {t.type}</p>
            <p>Seat: {attendee.seatNumber}</p>
            <p>QR: {t.qr}</p>
          </div>
        ))}
      </section>

      {/* Agenda */}
      <section className="bg-white p-4 rounded shadow mb-6">
        <h2 className="text-xl font-bold mb-3">My Agenda</h2>
        {agenda.map((s, i) => (
          <div key={i} className="flex justify-between border-b py-2">
            <span>{s.title} ({s.time})</span>
            <button
              onClick={() => toggleSession(i)}
              className="px-3 py-1 bg-yellow-400 rounded"
            >
              {s.status}
            </button>
          </div>
        ))}
      </section>

      {/* Networking */}
      <section className="bg-white p-4 rounded shadow mb-6">
        <h2 className="text-xl font-bold mb-3">People You Should Meet</h2>
        {attendee.networking.map((n, i) => (
          <div key={i} className="border p-3 rounded mb-2">
            <p>{n.name} — {n.company}</p>
            <p>Match: {n.similarity}%</p>
          </div>
        ))}
      </section>

      {/* Actions */}
      <section className="bg-white p-4 rounded shadow flex gap-4 flex-wrap">
        <button onClick={() => setPollOpen(true)} className="btn-red">Live Poll</button>
        <button onClick={() => alert("Q&A submitted")} className="btn-red">Q&A</button>
        <button onClick={exportCalendar} className="btn-red">Export Calendar</button>
        <CSVLink data={attendee.tickets} filename="attendee.csv" className="btn-yellow">
          Export CSV
        </CSVLink>
      </section>

      {/* Poll Modal */}
      {pollOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
          <div className="bg-white p-6 rounded">
            <h3 className="font-bold mb-2">Live Poll</h3>
            <button onClick={() => setPollOpen(false)} className="btn-red">Vote</button>
          </div>
        </div>
      )}
    </div>
  );
}

// ---------------- Card ----------------
function Card({ title, value }: { title: string; value: string | number }) {
  return (
    <div className="bg-white p-4 rounded shadow">
      <p className="text-sm">{title}</p>
      <p className="text-xl font-bold">{value}</p>
    </div>
  );
}
