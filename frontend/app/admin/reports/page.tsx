"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { CSVLink } from "react-csv";
import * as XLSX from "xlsx";

const mockEvents = [
  {
    id: 1,
    name: "AI & ML Conference 2026",
    date: "2026-03-15",
    attendees: 150,
    revenue: 4500,
    tickets: [
      { type: "Regular", price: 30, sold: 100 },
      { type: "VIP", price: 50, sold: 50 },
    ],
  },
  {
    id: 2,
    name: "Web Dev Workshop",
    date: "2026-04-01",
    attendees: 80,
    revenue: 1200,
    tickets: [
      { type: "Standard", price: 15, sold: 80 },
    ],
  },
  {
    id: 3,
    name: "Cybersecurity Summit",
    date: "2026-02-20",
    attendees: 200,
    revenue: 8000,
    tickets: [
      { type: "Early Bird", price: 25, sold: 150 },
      { type: "Regular", price: 50, sold: 50 },
    ],
  },
];

export default function GenerateReports() {
  const router = useRouter();
  const [selectedEvent, setSelectedEvent] = useState<number | null>(null);

  const handleExcelExport = () => {
    if (!selectedEvent) return;
    const event = mockEvents.find(e => e.id === selectedEvent);
    if (!event) return;

    const data: any[] = [];
    event.tickets.forEach(t => {
      for (let i = 0; i < t.sold; i++) {
        data.push({
          Event: event.name,
          Date: event.date,
          TicketType: t.type,
          Price: t.price,
        });
      }
    });

    const worksheet = XLSX.utils.json_to_sheet(data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Report");
    XLSX.writeFile(workbook, `${event.name}-report.xlsx`);
  };

  const csvData = selectedEvent
    ? (() => {
        const event = mockEvents.find(e => e.id === selectedEvent);
        if (!event) return [];
        const rows: any[] = [];
        event.tickets.forEach(t =>
          rows.push({
            Event: event.name,
            Date: event.date,
            TicketType: t.type,
            Price: t.price,
            Sold: t.sold,
            Revenue: t.price * t.sold,
          })
        );
        return rows;
      })()
    : [];

  return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-800">
      <header className="bg-mcs-red text-mcs-light p-6 shadow-md flex justify-between items-center">
        <h1 className="text-3xl font-bold">Generate Reports</h1>
        <button className="px-4 py-2 bg-mcs-yellow text-mcs-red font-semibold rounded hover:bg-yellow-400" onClick={() => router.push("/admin/dashboard")}>
          Back to Dashboard
        </button>
      </header>

      <main className="p-6">
        <div className="mb-6">
          <h2 className="text-xl font-bold mb-3 text-mcs-red">Select Event</h2>
          <select
            className="p-3 rounded border border-gray-dark focus:outline-none focus:ring-2 focus:ring-mcs-red"
            value={selectedEvent ?? ""}
            onChange={e => setSelectedEvent(Number(e.target.value))}
          >
            <option value="">-- Select Event --</option>
            {mockEvents.map(e => (
              <option key={e.id} value={e.id}>{e.name}</option>
            ))}
          </select>
        </div>

        {selectedEvent && (
          <div className="bg-white p-4 rounded shadow">
            <h2 className="text-lg font-semibold mb-3 text-mcs-red">Event Report</h2>
            <table className="w-full table-auto border-collapse mb-4">
              <thead>
                <tr className="bg-gray-200 text-gray-700">
                  <th className="border px-4 py-2">Ticket Type</th>
                  <th className="border px-4 py-2">Price</th>
                  <th className="border px-4 py-2">Sold</th>
                  <th className="border px-4 py-2">Revenue</th>
                </tr>
              </thead>
              <tbody>
                {mockEvents.find(e => e.id === selectedEvent)?.tickets.map((t, idx) => (
                  <tr key={idx}>
                    <td className="border px-4 py-2">{t.type}</td>
                    <td className="border px-4 py-2">{t.price}</td>
                    <td className="border px-4 py-2">{t.sold}</td>
                    <td className="border px-4 py-2">{t.price * t.sold}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="flex gap-4">
              <CSVLink
                data={csvData}
                filename={`${mockEvents.find(e => e.id === selectedEvent)?.name}-report.csv`}
                className="px-6 py-3 bg-mcs-red text-mcs-light rounded font-semibold hover:bg-red-700"
              >
                Export CSV
              </CSVLink>

              <button onClick={handleExcelExport} className="px-6 py-3 bg-mcs-yellow text-mcs-red rounded font-semibold hover:bg-yellow-400">
                Export Excel
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
