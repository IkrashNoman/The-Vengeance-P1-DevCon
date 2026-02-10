"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { CSVLink } from "react-csv";
import { apiService } from "@/lib/apiService";
import { Download, Mail, Search, Filter, Eye } from "lucide-react";

interface Attendee {
  id: number;
  name: string;
  email: string;
  company: string;
  interests: string[];
  registeredSessions: number;
  vipStatus: boolean;
  checkInStatus: boolean;
  aiConnections: number;
}

export default function AttendeesPage() {
  const router = useRouter();
  const [attendees, setAttendees] = useState<Attendee[]>([
    {
      id: 1,
      name: "Akrash Noman",
      email: "akrash@example.com",
      company: "TechCorp",
      interests: ["AI", "ML", "Networking"],
      registeredSessions: 5,
      vipStatus: true,
      checkInStatus: true,
      aiConnections: 12,
    },
    {
      id: 2,
      name: "Ali Khan",
      email: "ali@example.com",
      company: "DataLabs",
      interests: ["Data Science", "Analytics"],
      registeredSessions: 3,
      vipStatus: false,
      checkInStatus: true,
      aiConnections: 8,
    },
  ]);

  const [filteredAttendees, setFilteredAttendees] = useState<Attendee[]>(attendees);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterVIP, setFilterVIP] = useState(false);
  const [filterCheckedIn, setFilterCheckedIn] = useState(false);
  const [selectedAttendee, setSelectedAttendee] = useState<Attendee | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    applyFilters();
  }, [searchTerm, filterVIP, filterCheckedIn, attendees]);

  const applyFilters = () => {
    let filtered = attendees;

    if (searchTerm) {
      filtered = filtered.filter(
        (a) =>
          a.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          a.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
          a.company.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterVIP) {
      filtered = filtered.filter((a) => a.vipStatus);
    }

    if (filterCheckedIn) {
      filtered = filtered.filter((a) => a.checkInStatus);
    }

    setFilteredAttendees(filtered);
  };

  const handleSendMessage = async (attendeeId: number) => {
    setLoading(true);
    try {
      // API call would go here
      alert("Message sent to attendee");
    } catch (error) {
      alert("Failed to send message");
    } finally {
      setLoading(false);
    }
  };

  const csvData = filteredAttendees.map((a) => ({
    Name: a.name,
    Email: a.email,
    Company: a.company,
    Sessions: a.registeredSessions,
    VIP: a.vipStatus ? "Yes" : "No",
    CheckedIn: a.checkInStatus ? "Yes" : "No",
    Interests: a.interests.join("; "),
  }));

  return (
    <div className="p-6 bg-gray-light min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-dark">Attendees Management</h1>
        <CSVLink data={csvData} filename="attendees.csv" className="px-4 py-2 bg-mcs-yellow text-mcs-red font-semibold rounded hover:bg-yellow-400 flex items-center gap-2">
          <Download size={18} /> Export CSV
        </CSVLink>
      </div>

      {/* Search & Filter Section */}
      <div className="bg-white p-4 rounded shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div className="relative">
            <Search size={18} className="absolute left-3 top-3 text-gray-500" />
            <input
              type="text"
              placeholder="Search by name, email, or company..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red"
            />
          </div>
          <button
            onClick={() => setFilterVIP(!filterVIP)}
            className={`px-4 py-2 rounded font-semibold transition ${
              filterVIP ? "bg-mcs-red text-white" : "bg-gray-200 text-gray-dark hover:bg-gray-300"
            }`}
          >
            VIP Only
          </button>
          <button
            onClick={() => setFilterCheckedIn(!filterCheckedIn)}
            className={`px-4 py-2 rounded font-semibold transition ${
              filterCheckedIn ? "bg-mcs-red text-white" : "bg-gray-200 text-gray-dark hover:bg-gray-300"
            }`}
          >
            Checked In Only
          </button>
          <button className="px-4 py-2 bg-nust-blue text-white rounded hover:bg-blue-700 font-semibold">
            Advanced Filters
          </button>
        </div>
        <div className="text-sm text-gray-600">
          Showing {filteredAttendees.length} of {attendees.length} attendees
        </div>
      </div>

      {/* Attendees Table */}
      <div className="bg-white rounded shadow overflow-hidden">
        <table className="w-full border-collapse">
          <thead className="bg-mcs-red text-white">
            <tr>
              <th className="px-4 py-3 text-left">Name</th>
              <th className="px-4 py-3 text-left">Company</th>
              <th className="px-4 py-3 text-center">Sessions</th>
              <th className="px-4 py-3 text-center">VIP</th>
              <th className="px-4 py-3 text-center">Checked In</th>
              <th className="px-4 py-3 text-center">AI Connections</th>
              <th className="px-4 py-3 text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredAttendees.length > 0 ? (
              filteredAttendees.map((attendee, index) => (
                <tr key={attendee.id} className={index % 2 === 0 ? "bg-white" : "bg-gray-50 hover:bg-yellow-50 transition"}>
                  <td className="px-4 py-3 font-semibold">{attendee.name}</td>
                  <td className="px-4 py-3 text-gray-600">{attendee.company}</td>
                  <td className="px-4 py-3 text-center">{attendee.registeredSessions}</td>
                  <td className="px-4 py-3 text-center">
                    <span className={`px-2 py-1 rounded text-sm font-semibold ${attendee.vipStatus ? "bg-mcs-yellow text-mcs-red" : "bg-gray-200 text-gray-600"}`}>
                      {attendee.vipStatus ? "VIP" : "Regular"}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className={`px-2 py-1 rounded text-sm font-semibold ${attendee.checkInStatus ? "bg-green-200 text-green-800" : "bg-red-200 text-red-800"}`}>
                      {attendee.checkInStatus ? "✓" : "✗"}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center font-semibold text-nust-blue">{attendee.aiConnections}</td>
                  <td className="px-4 py-3 text-center">
                    <button
                      onClick={() => {
                        setSelectedAttendee(attendee);
                        setShowModal(true);
                      }}
                      className="px-3 py-1 bg-nust-blue text-white rounded hover:bg-blue-700 text-sm font-semibold mr-2"
                    >
                      View
                    </button>
                    <button onClick={() => handleSendMessage(attendee.id)} className="px-3 py-1 bg-mcs-red text-white rounded hover:bg-red-700 text-sm font-semibold">
                      <Mail size={16} className="inline" />
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={7} className="px-4 py-8 text-center text-gray-500">
                  No attendees found matching your filters
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Attendee Profile Modal */}
      {showModal && selectedAttendee && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="bg-white rounded-lg p-8 w-96 max-h-screen overflow-y-auto relative">
            <button onClick={() => setShowModal(false)} className="absolute top-3 right-3 text-gray-dark font-bold text-2xl">
              ×
            </button>
            <h2 className="text-2xl font-bold text-mcs-red mb-4">{selectedAttendee.name}</h2>
            <div className="space-y-3">
              <div>
                <p className="text-sm text-gray-600">Email</p>
                <p className="font-semibold">{selectedAttendee.email}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Company</p>
                <p className="font-semibold">{selectedAttendee.company}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Interests</p>
                <div className="flex flex-wrap gap-2 mt-1">
                  {selectedAttendee.interests.map((interest, idx) => (
                    <span key={idx} className="px-2 py-1 bg-mcs-yellow text-mcs-red rounded text-xs font-semibold">
                      {interest}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-sm text-gray-600">Sessions Registered</p>
                <p className="font-semibold">{selectedAttendee.registeredSessions}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">AI-Recommended Connections</p>
                <p className="font-semibold text-nust-blue">{selectedAttendee.aiConnections}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Badge Info</p>
                <p className="font-semibold bg-gray-100 p-2 rounded">ID: #{selectedAttendee.id} | {selectedAttendee.vipStatus ? "VIP Badge" : "Standard Badge"}</p>
              </div>
            </div>
            <button
              onClick={() => handleSendMessage(selectedAttendee.id)}
              className="w-full mt-4 px-4 py-2 bg-mcs-red text-white rounded font-semibold hover:bg-red-700"
              disabled={loading}
            >
              {loading ? "Sending..." : "Send Message"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
