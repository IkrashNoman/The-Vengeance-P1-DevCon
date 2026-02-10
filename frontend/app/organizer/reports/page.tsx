"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Bar, Line, Pie } from "react-chartjs-2";
import "chart.js/auto";
import { apiService } from "@/lib/apiService";
import { Download, Calendar } from "lucide-react";

interface ReportData {
  byTicketType: { labels: string[]; data: number[] };
  revenueByDate: { labels: string[]; data: number[] };
  sessionAttendance: { labels: string[]; data: number[] };
  networkingActivity: { labels: string[]; data: number[] };
  pollParticipation: number;
  qaActivity: number;
  totalRevenue: number;
  totalAttendees: number;
  avgEngagement: number;
}

export default function ReportsPage() {
  const router = useRouter();
  const [dateFrom, setDateFrom] = useState("2026-02-01");
  const [dateTo, setDateTo] = useState("2026-02-28");
  const [selectedReport, setSelectedReport] = useState("overview");
  const [loading, setLoading] = useState(false);

  const reportData: ReportData = {
    byTicketType: {
      labels: ["VIP", "Standard", "Early Bird", "Student"],
      data: [1200, 3500, 2800, 1500],
    },
    revenueByDate: {
      labels: ["Feb 1", "Feb 5", "Feb 10", "Feb 15", "Feb 20", "Feb 25"],
      data: [500, 1200, 2100, 3200, 4500, 5800],
    },
    sessionAttendance: {
      labels: ["AI Workshop", "ML Symposium", "Networking", "Closing", "Opening"],
      data: [156, 142, 189, 98, 203],
    },
    networkingActivity: {
      labels: ["Connections Made", "Chat Messages", "AI Matches", "Direct Intros"],
      data: [342, 1205, 276, 89],
    },
    pollParticipation: 84,
    qaActivity: 342,
    totalRevenue: 9000,
    totalAttendees: 385,
    avgEngagement: 87,
  };

  const revenueChart = {
    labels: reportData.revenueByDate.labels,
    datasets: [
      {
        label: "Revenue ($)",
        data: reportData.revenueByDate.data,
        backgroundColor: "#EE2022",
        borderColor: "#003366",
        borderWidth: 2,
        tension: 0.4,
      },
    ],
  };

  const ticketChart = {
    labels: reportData.byTicketType.labels,
    datasets: [
      {
        label: "Revenue by Ticket Type",
        data: reportData.byTicketType.data,
        backgroundColor: ["#EE2022", "#FED001", "#0072CE", "#003366"],
      },
    ],
  };

  const sessionChart = {
    labels: reportData.sessionAttendance.labels,
    datasets: [
      {
        label: "Session Attendance",
        data: reportData.sessionAttendance.data,
        backgroundColor: ["#EE2022", "#0072CE", "#FED001", "#003366", "#00A550"],
        borderColor: "#999",
        borderWidth: 1,
      },
    ],
  };

  const networkingChart = {
    labels: reportData.networkingActivity.labels,
    datasets: [
      {
        label: "Networking Activity",
        data: reportData.networkingActivity.data,
        backgroundColor: "#0072CE",
        borderColor: "#003366",
        borderWidth: 2,
      },
    ],
  };

  const handleExportPDF = async () => {
    setLoading(true);
    try {
      alert("Exporting PDF report...");
    } catch (error) {
      alert("Failed to export PDF");
    } finally {
      setLoading(false);
    }
  };

  const handleExportExcel = async () => {
    setLoading(true);
    try {
      alert("Exporting Excel report...");
    } catch (error) {
      alert("Failed to export Excel");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-gray-light min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-dark">Reports & Analytics</h1>
        <div className="flex gap-2">
          <button onClick={handleExportPDF} className="px-4 py-2 bg-mcs-red text-white rounded hover:bg-red-700 font-semibold flex items-center gap-2">
            <Download size={18} /> PDF
          </button>
          <button onClick={handleExportExcel} className="px-4 py-2 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400 font-semibold flex items-center gap-2">
            <Download size={18} /> Excel
          </button>
        </div>
      </div>

      {/* Date Range & Report Filter */}
      <div className="bg-white p-4 rounded shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm text-gray-600 mb-2">From Date</label>
            <input
              type="date"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-2">To Date</label>
            <input
              type="date"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-2">Report Type</label>
            <select
              value={selectedReport}
              onChange={(e) => setSelectedReport(e.target.value)}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red"
            >
              <option value="overview">Overview</option>
              <option value="revenue">Revenue</option>
              <option value="engagement">Engagement</option>
              <option value="networking">Networking</option>
              <option value="sessions">Sessions</option>
            </select>
          </div>
          <div className="flex items-end">
            <button className="w-full px-4 py-2 bg-nust-blue text-white rounded hover:bg-blue-700 font-semibold">
              Generate Report
            </button>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <MetricCard title="Total Revenue" value={`$${reportData.totalRevenue.toLocaleString()}`} color="mcs-red" />
        <MetricCard title="Total Attendees" value={reportData.totalAttendees} color="nust-blue" />
        <MetricCard title="Avg Engagement" value={`${reportData.avgEngagement}%`} color="mcs-yellow" />
        <MetricCard title="QA Activity" value={reportData.qaActivity} color="nust-light" />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold text-gray-dark mb-4">Revenue Trend</h2>
          <Line data={revenueChart} />
        </div>

        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold text-gray-dark mb-4">Revenue by Ticket Type</h2>
          <Pie data={ticketChart} />
        </div>

        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold text-gray-dark mb-4">Session Attendance</h2>
          <Pie data={sessionChart} />
        </div>

        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold text-gray-dark mb-4">Networking Activity</h2>
          <Bar data={networkingChart} />
        </div>
      </div>

      {/* Engagement Metrics Table */}
      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-xl font-semibold text-gray-dark mb-4">Engagement Metrics</h2>
        <table className="w-full border-collapse">
          <thead className="bg-mcs-red text-white">
            <tr>
              <th className="px-4 py-3 text-left">Metric</th>
              <th className="px-4 py-3 text-right">Value</th>
              <th className="px-4 py-3 text-right">Change</th>
              <th className="px-4 py-3 text-center">Trend</th>
            </tr>
          </thead>
          <tbody>
            <MetricsRow metric="Poll Participation" value={`${reportData.pollParticipation}%`} change="+5%" trend="up" />
            <MetricsRow metric="Q&A Activity" value={reportData.qaActivity} change="+12%" trend="up" />
            <MetricsRow metric="Session Attendance Rate" value="82%" change="+3%" trend="up" />
            <MetricsRow metric="Networking Connections" value="342" change="+28%" trend="up" />
            <MetricsRow metric="Chat Messages" value="1205" change="+45%" trend="up" />
          </tbody>
        </table>
      </div>
    </div>
  );
}

function MetricCard({ title, value, color }: { title: string; value: any; color: string }) {
  const colorMap: Record<string, string> = {
    "mcs-red": "bg-gradient-to-br from-red-500 to-red-700",
    "nust-blue": "bg-gradient-to-br from-blue-500 to-blue-700",
    "mcs-yellow": "bg-gradient-to-br from-yellow-400 to-yellow-600",
    "nust-light": "bg-gradient-to-br from-gray-400 to-gray-600",
  };

  return (
    <div className={`p-4 rounded shadow text-white ${colorMap[color] || colorMap["mcs-red"]}`}>
      <p className="text-sm opacity-90">{title}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
}

function MetricsRow({ metric, value, change, trend }: { metric: string; value: any; change: string; trend: "up" | "down" }) {
  return (
    <tr className="border-b hover:bg-gray-50">
      <td className="px-4 py-3 font-semibold">{metric}</td>
      <td className="px-4 py-3 text-right">{value}</td>
      <td className={`px-4 py-3 text-right ${trend === "up" ? "text-green-600 font-semibold" : "text-red-600 font-semibold"}`}>
        {change}
      </td>
      <td className="px-4 py-3 text-center">{trend === "up" ? "📈" : "📉"}</td>
    </tr>
  );
}
