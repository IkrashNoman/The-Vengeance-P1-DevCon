// app/organizer/dashboard/page.tsx
"use client";

import { useEffect, useState } from "react";
import { Line, Pie } from "react-chartjs-2";
import "chart.js/auto";
import { useRouter } from "next/navigation";

// Mock Data (Replace with API fetch)
const mockDashboardData = {
  events: 5,
  registrations: 120,
  revenue: 4500,
  sessions: 20,
  engagementScore: 87,
  registrationTrends: {
    labels: ["Jan", "Feb", "Mar", "Apr", "May"],
    data: [10, 25, 40, 35, 50],
  },
  ticketSales: {
    labels: ["VIP", "Standard", "Early Bird"],
    data: [30, 70, 20],
  },
  sessionAttendance: [
    [5, 10, 8, 12],
    [7, 9, 14, 10],
    [10, 12, 9, 15],
    [8, 6, 11, 12],
  ],
  notifications: [
    { id: 1, type: "warning", message: "Session 'AI Networking' is full" },
    { id: 2, type: "info", message: "5 attendees on waitlist for VIP tickets" },
  ],
};

export default function OrganizerDashboard() {
  const router = useRouter();
  const [dashboardData, setDashboardData] = useState(mockDashboardData);

  // Chart Data
  const lineChartData = {
    labels: dashboardData.registrationTrends.labels,
    datasets: [
      {
        label: "Registrations",
        data: dashboardData.registrationTrends.data,
        backgroundColor: "#EE2022",
        borderColor: "#003366",
        tension: 0.4,
      },
    ],
  };

  const pieChartData = {
    labels: dashboardData.ticketSales.labels,
    datasets: [
      {
        label: "Ticket Sales",
        data: dashboardData.ticketSales.data,
        backgroundColor: ["#EE2022", "#FED001", "#0072CE"],
      },
    ],
  };

  return (
    <div className="p-6 bg-gray-light min-h-screen">
      <h1 className="text-3xl font-bold text-gray-dark mb-6">Organizer Dashboard</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
        <Card title="Total Events" value={dashboardData.events} color="mcs-red" />
        <Card title="Registrations" value={dashboardData.registrations} color="nust-blue" />
        <Card title="Revenue ($)" value={dashboardData.revenue} color="mcs-yellow" />
        <Card title="Sessions" value={dashboardData.sessions} color="nust-light" />
        <Card title="Engagement Score" value={`${dashboardData.engagementScore}%`} color="mcs-red" />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold text-gray-dark mb-2">Registrations Over Time</h2>
          <Line data={lineChartData} />
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold text-gray-dark mb-2">Ticket Type Sales</h2>
          <Pie data={pieChartData} />
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white p-4 rounded shadow mb-6">
        <h2 className="text-xl font-semibold text-gray-dark mb-4">Quick Actions</h2>
        <div className="flex flex-wrap gap-4">
          <button
            className="px-4 py-2 bg-mcs-red text-mcs-light rounded hover:bg-red-700"
            onClick={() => router.push("/organizer/events")}
          >
            Events Management
          </button>
          <button
            className="px-4 py-2 bg-nust-blue text-white rounded hover:bg-nust-light"
            onClick={() => router.push("/organizer/sessions")}
          >
            Sessions & Speakers
          </button>
          <button
            className="px-4 py-2 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400"
            onClick={() => router.push("/organizer/tickets")}
          >
            Tickets & Registration
          </button>
          <button
            className="px-4 py-2 bg-mcs-red text-mcs-light rounded hover:bg-red-700"
            onClick={() => router.push("/organizer/venue")}
          >
            Venue Floor Plan
          </button>
          <button
            className="px-4 py-2 bg-nust-light text-white rounded hover:bg-nust-blue"
            onClick={() => router.push("/organizer/reports")}
          >
            Reports
          </button>
        </div>
      </div>

      {/* Notifications Panel */}
      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-xl font-semibold text-gray-dark mb-4">Notifications</h2>
        <ul className="space-y-2">
          {dashboardData.notifications.map((n) => (
            <li
              key={n.id}
              className={`p-2 rounded ${
                n.type === "warning" ? "bg-mcs-red/20 text-mcs-red" : "bg-nust-light/20 text-nust-blue"
              }`}
            >
              {n.message}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

// Summary Card Component
function Card({ title, value, color }: { title: string; value: number | string; color: string }) {
  return (
    <div className={`bg-${color} text-white p-4 rounded shadow flex flex-col justify-between`}>
      <span className="text-sm font-medium">{title}</span>
      <span className="text-2xl font-bold">{value}</span>
    </div>
  );
}
