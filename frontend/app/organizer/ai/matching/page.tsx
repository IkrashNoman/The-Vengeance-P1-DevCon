"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { apiService } from "@/lib/apiService";
import { Users, Link as LinkIcon, Zap, TrendingUp } from "lucide-react";

interface MatchedProfile {
  id: number;
  name: string;
  company: string;
  interests: string[];
  similarity: number;
  reason: string;
  mutualInterests: string[];
  connectionStatus: "suggested" | "connected" | "pending";
}

interface NetworkGraph {
  nodes: Array<{ id: number; label: string; size: number }>;
  edges: Array<{ from: number; to: number; strength: number }>;
  clusterSize: number;
}

export default function AIMatchingPage() {
  const router = useRouter();
  const [matches, setMatches] = useState<MatchedProfile[]>([
    {
      id: 1,
      name: "Sara Ahmed",
      company: "DataLabs",
      interests: ["AI", "ML", "Analytics"],
      similarity: 92,
      reason: "Both interested in AI and ML with tech background",
      mutualInterests: ["AI", "ML"],
      connectionStatus: "suggested",
    },
    {
      id: 2,
      name: "Ali Khan",
      company: "TechCorp",
      interests: ["Networking", "Innovation", "AI"],
      similarity: 87,
      reason: "Shared interests in innovation and networking",
      mutualInterests: ["Innovation", "Networking"],
      connectionStatus: "pending",
    },
    {
      id: 3,
      name: "Zara Malik",
      company: "InnovateLabs",
      interests: ["AI", "Healthcare", "IoT"],
      similarity: 78,
      reason: "Both interested in AI applications",
      mutualInterests: ["AI"],
      connectionStatus: "suggested",
    },
  ]);

  const [selectedMatch, setSelectedMatch] = useState<MatchedProfile | null>(null);
  const [filterMinSimilarity, setFilterMinSimilarity] = useState(0);
  const [sortBy, setSortBy] = useState<"similarity" | "recent" | "mutual">("similarity");
  const [loading, setLoading] = useState(false);

  const networkGraph: NetworkGraph = {
    nodes: [
      { id: 0, label: "You", size: 50 },
      ...matches.map((m, i) => ({ id: i + 1, label: m.name.split(" ")[0], size: m.similarity / 2 })),
    ],
    edges: matches.map((m, i) => ({ from: 0, to: i + 1, strength: m.similarity })),
    clusterSize: matches.length + 1,
  };

  const filteredMatches = matches
    .filter((m) => m.similarity >= filterMinSimilarity)
    .sort((a, b) => {
      if (sortBy === "similarity") return b.similarity - a.similarity;
      return 0;
    });

  const handleConnect = async (matchId: number) => {
    setLoading(true);
    try {
      const match = matches.find((m) => m.id === matchId);
      if (match) {
        const updatedMatches = matches.map((m) =>
          m.id === matchId ? { ...m, connectionStatus: "connected" as const } : m
        );
        setMatches(updatedMatches);
        setSelectedMatch(null);
      }
      alert("Connection sent! Waiting for acceptance.");
    } catch (error) {
      alert("Failed to send connection request");
    } finally {
      setLoading(false);
    }
  };

  const handleRefreshMatches = async () => {
    setLoading(true);
    try {
      // Call API to regenerate matches
      alert("Refreshing matches based on latest profile data...");
    } catch (error) {
      alert("Failed to refresh matches");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-gray-light min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-dark">AI-Powered Attendee Matching</h1>
        <button
          onClick={handleRefreshMatches}
          disabled={loading}
          className="px-4 py-2 bg-nust-blue text-white rounded hover:bg-blue-700 disabled:bg-gray-400 font-semibold flex items-center gap-2"
        >
          <Zap size={18} /> Refresh Matches
        </button>
      </div>

      {/* Network Graph Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <StatCard icon={<Users size={24} />} label="Total Matches" value={filteredMatches.length} color="mcs-red" />
        <StatCard icon={<LinkIcon size={24} />} label="Connected" value={filteredMatches.filter((m) => m.connectionStatus === "connected").length} color="nust-blue" />
        <StatCard icon={<TrendingUp size={24} />} label="Avg. Similarity" value={`${Math.round(filteredMatches.reduce((sum, m) => sum + m.similarity, 0) / filteredMatches.length)}%`} color="mcs-yellow" />
        <StatCard icon={<LinkIcon size={24} />} label="Network Clusters" value={networkGraph.clusterSize} color="nust-light" />
      </div>

      {/* Filters & Sort */}
      <div className="bg-white p-4 rounded shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Min. Similarity</label>
            <div className="flex items-center gap-2">
              <input
                type="range"
                min="0"
                max="100"
                value={filterMinSimilarity}
                onChange={(e) => setFilterMinSimilarity(Number(e.target.value))}
                className="flex-1"
              />
              <span className="font-semibold text-mcs-red">{filterMinSimilarity}%</span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Sort By</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as "similarity" | "recent" | "mutual")}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red"
            >
              <option value="similarity">Highest Similarity</option>
              <option value="recent">Most Recent</option>
              <option value="mutual">Mutual Interests</option>
            </select>
          </div>

          <div className="flex items-end">
            <button className="w-full px-4 py-2 bg-nust-blue text-white rounded hover:bg-blue-700 font-semibold">Export Network</button>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Matches List */}
        <div className="md:col-span-2 bg-white rounded shadow">
          <h2 className="text-xl font-semibold text-gray-dark p-4 border-b">AI-Suggested Matches</h2>

          <div className="space-y-2 p-4">
            {filteredMatches.length > 0 ? (
              filteredMatches.map((match) => (
                <div
                  key={match.id}
                  onClick={() => setSelectedMatch(match)}
                  className={`p-4 rounded border-2 cursor-pointer transition ${
                    selectedMatch?.id === match.id ? "border-mcs-red bg-red-50" : "border-gray-300 hover:border-mcs-red"
                  }`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="font-semibold text-lg">{match.name}</h3>
                      <p className="text-sm text-gray-600">{match.company}</p>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-mcs-red">{match.similarity}%</div>
                      <span
                        className={`text-xs px-2 py-1 rounded font-semibold ${
                          match.connectionStatus === "connected"
                            ? "bg-green-200 text-green-800"
                            : match.connectionStatus === "pending"
                              ? "bg-yellow-200 text-yellow-800"
                              : "bg-blue-200 text-blue-800"
                        }`}
                      >
                        {match.connectionStatus === "connected" ? "Connected" : match.connectionStatus === "pending" ? "Pending" : "Suggested"}
                      </span>
                    </div>
                  </div>

                  <p className="text-sm text-gray-600 mb-2">{match.reason}</p>

                  <div className="flex flex-wrap gap-1">
                    {match.mutualInterests.map((interest) => (
                      <span key={interest} className="px-2 py-1 bg-mcs-yellow text-mcs-red rounded text-xs font-semibold">
                        {interest}
                      </span>
                    ))}
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">No matches found with current filters</div>
            )}
          </div>
        </div>

        {/* Selected Match Details & Network Graph */}
        <div className="space-y-4">
          {selectedMatch ? (
            <div className="bg-white p-4 rounded shadow">
              <h2 className="text-xl font-semibold text-gray-dark mb-4">Match Details</h2>

              <div className="space-y-3 mb-4">
                <div>
                  <p className="text-sm text-gray-600">Name</p>
                  <p className="font-semibold">{selectedMatch.name}</p>
                </div>

                <div>
                  <p className="text-sm text-gray-600">Company</p>
                  <p className="font-semibold">{selectedMatch.company}</p>
                </div>

                <div>
                  <p className="text-sm text-gray-600">Similarity Score</p>
                  <div className="w-full bg-gray-300 rounded overflow-hidden h-6 mt-1">
                    <div
                      className="bg-gradient-to-r from-mcs-red to-mcs-yellow h-full flex items-center justify-center text-white text-xs font-bold"
                      style={{ width: `${selectedMatch.similarity}%` }}
                    >
                      {selectedMatch.similarity}%
                    </div>
                  </div>
                </div>

                <div>
                  <p className="text-sm text-gray-600">Match Reason</p>
                  <p className="font-semibold text-sm">{selectedMatch.reason}</p>
                </div>

                <div>
                  <p className="text-sm text-gray-600 mb-1">All Interests</p>
                  <div className="flex flex-wrap gap-1">
                    {selectedMatch.interests.map((interest) => (
                      <span key={interest} className="px-2 py-1 bg-gray-200 text-gray-800 rounded text-xs font-semibold">
                        {interest}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {selectedMatch.connectionStatus === "suggested" ? (
                <button
                  onClick={() => handleConnect(selectedMatch.id)}
                  disabled={loading}
                  className="w-full px-4 py-2 bg-mcs-red text-white rounded hover:bg-red-700 disabled:bg-gray-400 font-semibold"
                >
                  {loading ? "Connecting..." : "Send Connection"}
                </button>
              ) : (
                <button className="w-full px-4 py-2 bg-green-600 text-white rounded disabled:bg-gray-400 font-semibold" disabled>
                  {selectedMatch.connectionStatus === "connected" ? "✓ Connected" : "⏳ Pending"}
                </button>
              )}
            </div>
          ) : (
            <div className="bg-white p-4 rounded shadow text-center text-gray-500">
              <p>Select a match to view details</p>
            </div>
          )}

          {/* Network Visualization Preview */}
          <div className="bg-white p-4 rounded shadow">
            <h2 className="text-lg font-semibold text-gray-dark mb-2">Network Overview</h2>
            <div className="bg-gray-100 rounded p-4 text-center">
              <div className="text-3xl mb-2">🔗</div>
              <p className="text-sm text-gray-600">{networkGraph.clusterSize} nodes in network</p>
              <p className="text-xs text-gray-500">{networkGraph.edges.length} connections</p>
              <button className="mt-2 px-3 py-1 bg-nust-blue text-white rounded text-xs hover:bg-blue-700">View Full Graph</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, color }: { icon: React.ReactNode; label: string; value: any; color: string }) {
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
