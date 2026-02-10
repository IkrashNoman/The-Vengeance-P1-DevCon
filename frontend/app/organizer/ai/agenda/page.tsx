"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { apiService } from "@/lib/apiService";
import { Clock, MapPin, Users, Star, CheckCircle } from "lucide-react";

interface Session {
  id: number;
  title: string;
  speaker: string;
  startTime: string;
  endTime: string;
  room: string;
  capacity: number;
  attendees: number;
  relevanceScore: number;
  tags: string[];
  status: "upcoming" | "ongoing" | "completed";
}

interface PersonalizedAgenda {
  attendeeId: number;
  attendeeName: string;
  interests: string[];
  recommendedSessions: Session[];
  totalScore: number;
  createdAt: string;
}

export default function AIAgendaPage() {
  const router = useRouter();
  const [selectedAttendee, setSelectedAttendee] = useState<string>("attendee1");
  const [agenda, setAgenda] = useState<PersonalizedAgenda>({
    attendeeId: 1,
    attendeeName: "John Doe",
    interests: ["AI", "Machine Learning", "Data Science"],
    recommendedSessions: [
      {
        id: 1,
        title: "AI in Healthcare",
        speaker: "Dr. Smith",
        startTime: "09:00 AM",
        endTime: "10:00 AM",
        room: "Auditorium A",
        capacity: 200,
        attendees: 180,
        relevanceScore: 98,
        tags: ["AI", "Healthcare", "Innovation"],
        status: "upcoming",
      },
      {
        id: 2,
        title: "Machine Learning Workshop",
        speaker: "Prof. Johnson",
        startTime: "10:30 AM",
        endTime: "11:30 AM",
        room: "Lab 1",
        capacity: 50,
        attendees: 45,
        relevanceScore: 95,
        tags: ["ML", "Hands-on", "Python"],
        status: "upcoming",
      },
      {
        id: 3,
        title: "Data Science Trends 2026",
        speaker: "Ms. Williams",
        startTime: "02:00 PM",
        endTime: "03:00 PM",
        room: "Auditorium B",
        capacity: 150,
        attendees: 120,
        relevanceScore: 87,
        tags: ["Data Science", "Trends", "Big Data"],
        status: "upcoming",
      },
      {
        id: 4,
        title: "Ethical AI Debate",
        speaker: "Panel Discussion",
        startTime: "03:30 PM",
        endTime: "04:30 PM",
        room: "Conference Room",
        capacity: 80,
        attendees: 75,
        relevanceScore: 76,
        tags: ["Ethics", "AI", "Discussion"],
        status: "upcoming",
      },
    ],
    totalScore: 89,
    createdAt: new Date().toISOString(),
  });

  const [showRegisterModal, setShowRegisterModal] = useState(false);
  const [registeredSessions, setRegisteredSessions] = useState<number[]>([1, 2]);
  const [loading, setLoading] = useState(false);

  const attendees = [
    { id: "attendee1", name: "John Doe" },
    { id: "attendee2", name: "Jane Smith" },
    { id: "attendee3", name: "Ali Khan" },
  ];

  const handleRegisterSession = async (sessionId: number) => {
    setLoading(true);
    try {
      if (registeredSessions.includes(sessionId)) {
        setRegisteredSessions(registeredSessions.filter((id) => id !== sessionId));
        alert("Unregistered from session");
      } else {
        setRegisteredSessions([...registeredSessions, sessionId]);
        alert("Registered for session");
      }
    } catch (error) {
      alert("Failed to register for session");
    } finally {
      setLoading(false);
    }
  };

  const handleExportAgenda = () => {
    const agendaText = `
Personalized Agenda for ${agenda.attendeeName}
==========================================

Interests: ${agenda.interests.join(", ")}
Overall Match Score: ${agenda.totalScore}%

Recommended Sessions:
${agenda.recommendedSessions
  .map((s) => `- ${s.title} (${s.startTime} - ${s.endTime}) - ${s.speaker} - Relevance: ${s.relevanceScore}%`)
  .join("\n")}
    `.trim();

    const blob = new Blob([agendaText], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `agenda-${agenda.attendeeName}.txt`;
    a.click();
  };

  return (
    <div className="p-6 bg-gray-light min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-dark">AI-Generated Personalized Agendas</h1>
        <button onClick={handleExportAgenda} className="px-4 py-2 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400 font-semibold">
          📥 Export Agenda
        </button>
      </div>

      {/* Attendee Selector */}
      <div className="bg-white p-4 rounded shadow mb-6">
        <label className="block text-sm font-semibold text-gray-700 mb-2">Select Attendee</label>
        <select
          value={selectedAttendee}
          onChange={(e) => setSelectedAttendee(e.target.value)}
          className="w-full md:w-64 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red"
        >
          {attendees.map((attendee) => (
            <option key={attendee.id} value={attendee.id}>
              {attendee.name}
            </option>
          ))}
        </select>
      </div>

      {/* Agenda Header Card */}
      <div className="bg-gradient-to-r from-mcs-red to-nust-blue text-white p-6 rounded shadow mb-6">
        <h2 className="text-2xl font-bold mb-2">{agenda.attendeeName}'s Personalized Agenda</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <p className="opacity-80">Interests</p>
            <p className="font-semibold">{agenda.interests.join(", ")}</p>
          </div>
          <div>
            <p className="opacity-80">Overall Match Score</p>
            <p className="font-bold text-2xl">{agenda.totalScore}%</p>
          </div>
          <div>
            <p className="opacity-80">Registered Sessions</p>
            <p className="font-bold text-2xl">{registeredSessions.length}</p>
          </div>
        </div>
      </div>

      {/* Recommended Sessions */}
      <div className="space-y-4">
        {agenda.recommendedSessions.map((session) => (
          <div key={session.id} className="bg-white rounded shadow overflow-hidden hover:shadow-lg transition">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="text-xl font-bold text-gray-dark">{session.title}</h3>
                    <span
                      className={`px-2 py-1 rounded text-xs font-semibold ${
                        session.status === "ongoing"
                          ? "bg-green-200 text-green-800"
                          : session.status === "completed"
                            ? "bg-gray-200 text-gray-800"
                            : "bg-blue-200 text-blue-800"
                      }`}
                    >
                      {session.status}
                    </span>
                  </div>
                  <p className="text-gray-600">by {session.speaker}</p>
                </div>

                <div className="text-right">
                  <div className="text-3xl font-bold text-mcs-red">{session.relevanceScore}%</div>
                  <p className="text-xs text-gray-600">Match</p>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 text-sm">
                <div className="flex items-center gap-2 text-gray-700">
                  <Clock size={16} />
                  <span>{session.startTime} - {session.endTime}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-700">
                  <MapPin size={16} />
                  <span>{session.room}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-700">
                  <Users size={16} />
                  <span>{session.attendees}/{session.capacity}</span>
                </div>
                <div className="flex items-center gap-2">
                  {registeredSessions.includes(session.id) ? (
                    <CheckCircle size={16} className="text-green-600" />
                  ) : (
                    <Star size={16} className="text-gray-400" />
                  )}
                  <span className="text-gray-700">{registeredSessions.includes(session.id) ? "Registered" : "Not registered"}</span>
                </div>
              </div>

              <div className="flex flex-wrap gap-2 mb-4">
                {session.tags.map((tag) => (
                  <span key={tag} className="px-2 py-1 bg-mcs-yellow text-mcs-red rounded text-xs font-semibold">
                    {tag}
                  </span>
                ))}
              </div>

              <div className="w-full bg-gray-300 rounded overflow-hidden h-2 mb-4">
                <div className="bg-gradient-to-r from-mcs-red to-mcs-yellow h-full" style={{ width: `${session.relevanceScore}%` }}></div>
              </div>

              <button
                onClick={() => handleRegisterSession(session.id)}
                disabled={loading}
                className={`px-6 py-2 rounded font-semibold transition ${
                  registeredSessions.includes(session.id)
                    ? "bg-red-500 text-white hover:bg-red-700"
                    : "bg-mcs-red text-white hover:bg-red-700"
                }`}
              >
                {registeredSessions.includes(session.id) ? "✓ Unregister" : "+ Register"}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Why This Agenda Section */}
      <div className="bg-white p-6 rounded shadow mt-6">
        <h2 className="text-xl font-bold text-gray-dark mb-4">Why These Recommendations?</h2>
        <div className="space-y-3">
          <p className="text-gray-700">
            <strong>Based on profile analysis:</strong> {agenda.attendeeName} has shown strong interest in{" "}
            <span className="font-semibold text-mcs-red">{agenda.interests.join(", ")}</span>.
          </p>
          <p className="text-gray-700">
            <strong>AI algorithm matched:</strong> Sessions were selected using semantic similarity analysis of interests, past attendance patterns, and peer recommendations.
          </p>
          <p className="text-gray-700">
            <strong>Networking potential:</strong> Recommended sessions have high attendance from people with complementary interests, maximizing networking opportunities.
          </p>
        </div>
      </div>
    </div>
  );
}
