// app/admin/dashboard/page.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend } from "recharts";

const mockEvents = [
  { id: 1, name: "AI & ML Conference 2026", date: "2026-03-15", attendees: 150, revenue: 4500, status: "Ongoing" },
  { id: 2, name: "Web Dev Workshop", date: "2026-04-01", attendees: 80, revenue: 1200, status: "Upcoming" },
  { id: 3, name: "Cybersecurity Summit", date: "2026-02-20", attendees: 200, revenue: 8000, status: "Ongoing" },
];

const mockNotifications = [
  { id: 1, msg: "Event 'Web Dev Workshop' has 5 sessions exceeding capacity." },
  { id: 2, msg: "AI & ML Conference early bird tickets end tomorrow." },
  { id: 3, msg: "New attendee registrations pending approval." },
];

const attendanceData = [
  { date: "2026-02-01", attendees: 50 },
  { date: "2026-02-05", attendees: 120 },
  { date: "2026-02-10", attendees: 180 },
  { date: "2026-02-15", attendees: 220 },
  { date: "2026-02-20", attendees: 250 },
];

const revenueData = [
  { event: "AI & ML Conference", revenue: 4500 },
  { event: "Web Dev Workshop", revenue: 1200 },
  { event: "Cybersecurity Summit", revenue: 8000 },
];

export default function AdminDashboard() {
  const router = useRouter();

  const handleEventClick = (id: number) => router.push(`/admin/events/${id}`);

  return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-800">
      <header className="bg-mcs-red text-mcs-light p-6 shadow-md flex justify-between items-center">
        <h1 className="text-3xl font-bold">Admin Dashboard</h1>
        <button className="px-4 py-2 bg-mcs-yellow text-mcs-red font-semibold rounded hover:bg-yellow-400">Logout</button>
      </header>

      <main className="p-6">
        <section className="mb-6 grid grid-cols-1 md:grid-cols-4 gap-4">
          <button className="p-4 bg-mcs-light rounded shadow hover:shadow-lg font-semibold" onClick={() => router.push('/admin/events')}>Event Management</button>
            <button className="p-4 bg-mcs-light rounded shadow hover:shadow-lg font-semibold">Manage Sessions</button>
          <button className="p-4 bg-mcs-light rounded shadow hover:shadow-lg font-semibold">Manage Attendees</button>
          <button className="p-4 bg-mcs-light rounded shadow hover:shadow-lg font-semibold">Generate Reports</button>
        </section>

        <section className="mb-6 bg-white p-4 rounded shadow">
          <h2 className="text-xl font-bold mb-3 text-mcs-red">Notifications</h2>
          <ul className="list-disc list-inside space-y-2 text-gray-dark">
            {mockNotifications.map(n => <li key={n.id}>{n.msg}</li>)}
          </ul>
        </section>

        <section className="mb-6 bg-white p-4 rounded shadow overflow-x-auto">
          <h2 className="text-xl font-bold mb-3 text-mcs-red">Events Overview</h2>
          <table className="w-full table-auto border-collapse">
            <thead>
              <tr className="bg-gray-200 text-gray-700">
                <th className="border px-4 py-2">Event Name</th>
                <th className="border px-4 py-2">Date</th>
                <th className="border px-4 py-2">Attendees</th>
                <th className="border px-4 py-2">Revenue ($)</th>
                <th className="border px-4 py-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {mockEvents.map(e => (
                <tr key={e.id} className="cursor-pointer hover:bg-gray-100" onClick={() => handleEventClick(e.id)}>
                  <td className="border px-4 py-2">{e.name}</td>
                  <td className="border px-4 py-2">{e.date}</td>
                  <td className="border px-4 py-2">{e.attendees}</td>
                  <td className="border px-4 py-2">{e.revenue}</td>
                  <td className="border px-4 py-2">{e.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="grid md:grid-cols-2 gap-6">
          <div className="bg-white p-4 rounded shadow">
            <h2 className="text-xl font-bold mb-3 text-mcs-red">Attendance Trend</h2>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={attendanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="attendees" stroke="#E3342F" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-white p-4 rounded shadow">
            <h2 className="text-xl font-bold mb-3 text-mcs-red">Revenue per Event</h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={revenueData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="event" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="revenue" fill="#E3342F" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>
      </main>
    </div>
  );
}
