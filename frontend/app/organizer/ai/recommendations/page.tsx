"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Bar, Line, Pie } from "react-chartjs-2";
import "chart.js/auto";
import { apiService } from "@/lib/apiService";
import { Zap, TrendingUp, Users, Award } from "lucide-react";

interface Recommendation {
  id: number;
  sessionTitle: string;
  sessionId: number;
  recommendationCount: number;
  engagementRate: number;
  avgRating: number;
  trending: boolean;
  category: string;
}

interface EngagementMetric {
  sessionId: number;
  sessionTitle: string;
  attendees: number;
  pollParticipation: number;
  qnaActivity: number;
  avgRating: number;
  trend: "up" | "down" | "stable";
}

export default function AIRecommendationsPage() {
  const router = useRouter();

  const [recommendations, setRecommendations] = useState<Recommendation[]>([
    {
      id: 1,
      sessionTitle: "AI in Healthcare",
      sessionId: 1,
      recommendationCount: 234,
      engagementRate: 92,
      avgRating: 4.8,
      trending: true,
      category: "AI",
    },
    {
      id: 2,
      sessionTitle: "Machine Learning Workshop",
      sessionId: 2,
      recommendationCount: 198,
      engagementRate: 87,
      avgRating: 4.6,
      trending: true,
      category: "ML",
    },
    {
      id: 3,
      sessionTitle: "Data Science Trends",
      sessionId: 3,
      recommendationCount: 156,
      engagementRate: 78,
      avgRating: 4.4,
      trending: false,
      category: "Data Science",
    },
  ]);

  const [engagementMetrics, setEngagementMetrics] = useState<EngagementMetric[]>([
    {
      sessionId: 1,
      sessionTitle: "AI in Healthcare",
      attendees: 180,
      pollParticipation: 142,
      qnaActivity: 67,
      avgRating: 4.8,
      trend: "up",
    },
    {
      sessionId: 2,
      sessionTitle: "ML Workshop",
      attendees: 45,
      pollParticipation: 39,
      qnaActivity: 28,
      avgRating: 4.6,
      trend: "up",
    },
    {
      sessionId: 3,
      sessionTitle: "Data Science Trends",
      attendees: 120,
      pollParticipation: 93,
      qnaActivity: 45,
      avgRating: 4.4,
      trend: "stable",
    },
  ]);

  const [selectedSession, setSelectedSession] = useState<Recommendation | null>(null);
  const [filterCategory, setFilterCategory] = useState("all");
  const [loading, setLoading] = useState(false);

  const recommendationChart = {
    labels: recommendations.map((r) => r.sessionTitle),
    datasets: [
      {
        label: "Recommendation Count",
        data: recommendations.map((r) => r.recommendationCount),
        backgroundColor: ["#EE2022", "#FED001", "#0072CE"],
        borderColor: "#003366",
        borderWidth: 1,
      },
    ],
  };

  const engagementChart = {
    labels: engagementMetrics.map((m) => m.sessionTitle),
    datasets: [
      {
        label: "Poll Participation",
        data: engagementMetrics.map((m) => m.pollParticipation),
        backgroundColor: "#EE2022",
        borderColor: "#003366",
      },
      {
        label: "Q&A Activity",
        data: engagementMetrics.map((m) => m.qnaActivity),
        backgroundColor: "#FED001",
        borderColor: "#003366",
      },
    ],
  };

  const ratingChart = {
    labels: recommendations.map((r) => r.sessionTitle),
    datasets: [
      {
        label: "Average Rating",
        data: recommendations.map((r) => r.avgRating),
        borderColor: "#0072CE",
        backgroundColor: "rgba(0, 114, 206, 0.1)",
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const handleApplyRecommendation = async (id: number) => {
    setLoading(true);
    try {
      alert("Recommendation will be sent to all eligible attendees");
    } catch (error) {
      alert("Failed to apply recommendation");
    } finally {
      setLoading(false);
    }
  };

  const filteredRecommendations =
    filterCategory === "all" ? recommendations : recommendations.filter((r) => r.category === filterCategory);

  return (
    <div className="p-6 bg-gray-light min-h-screen">
      <h1 className="text-3xl font-bold text-gray-dark mb-6">AI Session Recommendations & Trending</h1>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <MetricCard
          icon={<Zap size={24} />}
          label="Total Recommendations"
          value={recommendations.reduce((sum, r) => sum + r.recommendationCount, 0)}
          color="mcs-red"
        />
        <MetricCard
          icon={<TrendingUp size={24} />}
          label="Trending Sessions"
          value={recommendations.filter((r) => r.trending).length}
          color="nust-blue"
        />
        <MetricCard
          icon={<Users size={24} />}
          label="Total Engagement"
          value={`${Math.round(
            engagementMetrics.reduce((sum, m) => sum + m.pollParticipation + m.qnaActivity, 0) / engagementMetrics.length
          )}%`}
          color="mcs-yellow"
        />
        <MetricCard
          icon={<Award size={24} />}
          label="Average Rating"
          value={`${(recommendations.reduce((sum, r) => sum + r.avgRating, 0) / recommendations.length).toFixed(1)}/5`}
          color="nust-light"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold text-gray-dark mb-4">Recommendations by Session</h2>
          <Bar data={recommendationChart} />
        </div>

        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold text-gray-dark mb-4">Engagement Activity</h2>
          <Bar data={engagementChart} />
        </div>

        <div className="bg-white p-4 rounded shadow md:col-span-2">
          <h2 className="text-xl font-semibold text-gray-dark mb-4">Session Ratings Trend</h2>
          <Line data={ratingChart} />
        </div>
      </div>

      {/* Recommendations List */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Main List */}
        <div className="md:col-span-2">
          <div className="bg-white rounded shadow">
            <div className="p-4 border-b">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold text-gray-dark">AI-Recommended Sessions</h2>
                <select
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                  className="px-3 py-1 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-mcs-red"
                >
                  <option value="all">All Categories</option>
                  <option value="AI">AI</option>
                  <option value="ML">Machine Learning</option>
                  <option value="Data Science">Data Science</option>
                </select>
              </div>
            </div>

            <div className="space-y-0">
              {filteredRecommendations.map((rec, idx) => (
                <div
                  key={rec.id}
                  onClick={() => setSelectedSession(rec)}
                  className={`p-4 ${idx !== filteredRecommendations.length - 1 ? "border-b" : ""} cursor-pointer transition ${
                    selectedSession?.id === rec.id ? "bg-red-50 border-l-4 border-l-mcs-red" : "hover:bg-gray-50"
                  }`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex-1">
                      <h3 className="font-bold text-gray-dark">{rec.sessionTitle}</h3>
                      <p className="text-sm text-gray-600">{rec.category}</p>
                    </div>
                    <div className="text-right">
                      {rec.trending && <span className="px-2 py-1 bg-red-200 text-red-800 rounded text-xs font-bold">🔥 TRENDING</span>}
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-2 text-sm mb-2">
                    <div>
                      <p className="text-gray-600">Recommendations</p>
                      <p className="font-bold text-mcs-red">{rec.recommendationCount}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Engagement</p>
                      <p className="font-bold text-nust-blue">{rec.engagementRate}%</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Rating</p>
                      <p className="font-bold">⭐ {rec.avgRating}</p>
                    </div>
                  </div>

                  <div className="w-full bg-gray-300 rounded overflow-hidden h-2">
                    <div className="bg-mcs-red h-full" style={{ width: `${rec.engagementRate}%` }}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Details Panel */}
        <div>
          {selectedSession ? (
            <div className="bg-white rounded shadow p-4 space-y-4">
              <h2 className="text-xl font-bold text-gray-dark">{selectedSession.sessionTitle}</h2>

              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-600">Category</p>
                  <p className="font-bold">{selectedSession.category}</p>
                </div>

                <div>
                  <p className="text-sm text-gray-600">Recommendation Count</p>
                  <p className="font-bold text-2xl text-mcs-red">{selectedSession.recommendationCount}</p>
                </div>

                <div>
                  <p className="text-sm text-gray-600">Engagement Rate</p>
                  <div className="w-full bg-gray-300 rounded overflow-hidden h-3">
                    <div
                      className="bg-gradient-to-r from-mcs-red to-mcs-yellow h-full"
                      style={{ width: `${selectedSession.engagementRate}%` }}
                    ></div>
                  </div>
                  <p className="text-sm font-bold mt-1">{selectedSession.engagementRate}% attendee engagement</p>
                </div>

                <div>
                  <p className="text-sm text-gray-600">Rating</p>
                  <p className="font-bold text-2xl">⭐ {selectedSession.avgRating}/5</p>
                </div>

                <div>
                  <p className="text-sm text-gray-600">Status</p>
                  <p className={`font-bold ${selectedSession.trending ? "text-red-600" : "text-gray-600"}`}>
                    {selectedSession.trending ? "🔥 Trending" : "Regular"}
                  </p>
                </div>
              </div>

              <button
                onClick={() => handleApplyRecommendation(selectedSession.id)}
                disabled={loading}
                className="w-full px-4 py-2 bg-mcs-red text-white rounded hover:bg-red-700 disabled:bg-gray-400 font-semibold"
              >
                {loading ? "Applying..." : "Apply Recommendation"}
              </button>

              <button className="w-full px-4 py-2 bg-nust-blue text-white rounded hover:bg-blue-700 font-semibold">
                View Analytics
              </button>
            </div>
          ) : (
            <div className="bg-white rounded shadow p-4 text-center text-gray-500">
              <p>Select a session to view details</p>
            </div>
          )}
        </div>
      </div>

      {/* Engagement Breakdown Table */}
      <div className="bg-white rounded shadow mt-6">
        <h2 className="text-xl font-semibold text-gray-dark p-4 border-b">Engagement Breakdown by Session</h2>
        <table className="w-full border-collapse">
          <thead className="bg-mcs-red text-white">
            <tr>
              <th className="px-4 py-3 text-left">Session</th>
              <th className="px-4 py-3 text-center">Attendees</th>
              <th className="px-4 py-3 text-center">Polls</th>
              <th className="px-4 py-3 text-center">Q&A</th>
              <th className="px-4 py-3 text-center">Rating</th>
              <th className="px-4 py-3 text-center">Trend</th>
            </tr>
          </thead>
          <tbody>
            {engagementMetrics.map((metric, idx) => (
              <tr key={metric.sessionId} className={idx % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                <td className="px-4 py-3 font-semibold">{metric.sessionTitle}</td>
                <td className="px-4 py-3 text-center">{metric.attendees}</td>
                <td className="px-4 py-3 text-center">{metric.pollParticipation}</td>
                <td className="px-4 py-3 text-center">{metric.qnaActivity}</td>
                <td className="px-4 py-3 text-center">⭐ {metric.avgRating}</td>
                <td className="px-4 py-3 text-center">{metric.trend === "up" ? "📈" : metric.trend === "down" ? "📉" : "➡️"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function MetricCard({ icon, label, value, color }: { icon: React.ReactNode; label: string; value: any; color: string }) {
  const colorMap: Record<string, string> = {
    "mcs-red": "from-red-500 to-red-700",
    "nust-blue": "from-blue-500 to-blue-700",
    "mcs-yellow": "from-yellow-400 to-yellow-600",
    "nust-light": "from-gray-400 to-gray-600",
  };

  return (
    <div className={`bg-gradient-to-br ${colorMap[color] || colorMap["mcs-red"]} p-4 rounded shadow text-white`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm opacity-90">{label}</p>
          <p className="text-2xl font-bold">{value}</p>
        </div>
        <div className="opacity-50">{icon}</div>
      </div>
    </div>
  );
}
