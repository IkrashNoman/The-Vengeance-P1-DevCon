"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { apiService } from "@/lib/apiService";
import { MessageSquare, Plus, Edit2, Trash2, RefreshCw, Save } from "lucide-react";

interface ChartbotFAQ {
  id: number;
  question: string;
  answer: string;
  category: string;
  createdAt: string;
  popularity: number;
}

interface ChatbotConfig {
  eventName: string;
  trainingMode: boolean;
  knowledge_base_status: "empty" | "training" | "ready";
  total_faqs: number;
  last_updated: string;
  ai_model: "groq-llama" | "gpt-3.5" | "custom";
}

export default function AIChatbotPage() {
  const router = useRouter();
  const [config, setConfig] = useState<ChatbotConfig>({
    eventName: "AI & ML Conference 2026",
    trainingMode: false,
    knowledge_base_status: "ready",
    total_faqs: 15,
    last_updated: new Date().toISOString(),
    ai_model: "groq-llama",
  });

  const [faqs, setFaqs] = useState<ChartbotFAQ[]>([
    {
      id: 1,
      question: "What is the event schedule?",
      answer: "The event runs from 9:00 AM to 5:00 PM. Check the schedule page for detailed session times.",
      category: "General",
      createdAt: "2026-02-01",
      popularity: 450,
    },
    {
      id: 2,
      question: "How do I register for sessions?",
      answer: "You can register for sessions through the attendee dashboard. Each session shows available slots.",
      category: "Registration",
      createdAt: "2026-02-01",
      popularity: 320,
    },
    {
      id: 3,
      question: "Is food provided at the event?",
      answer: "Yes, lunch and refreshments are provided throughout the day for all registered attendees.",
      category: "Logistics",
      createdAt: "2026-02-02",
      popularity: 280,
    },
  ]);

  const [newFaqQuestion, setNewFaqQuestion] = useState("");
  const [newFaqAnswer, setNewFaqAnswer] = useState("");
  const [newFaqCategory, setNewFaqCategory] = useState("General");
  const [editingId, setEditingId] = useState<number | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [testMessage, setTestMessage] = useState("");
  const [chatHistory, setChatHistory] = useState<Array<{ role: "user" | "bot"; message: string }>>([]);

  const categories = ["General", "Registration", "Sessions", "Logistics", "Technical", "Networking"];

  const handleAddFAQ = async () => {
    if (!newFaqQuestion.trim() || !newFaqAnswer.trim()) {
      alert("Please fill in all fields");
      return;
    }

    setLoading(true);
    try {
      const newFaq: ChartbotFAQ = {
        id: Math.max(...faqs.map((f) => f.id)) + 1,
        question: newFaqQuestion,
        answer: newFaqAnswer,
        category: newFaqCategory,
        createdAt: new Date().toISOString(),
        popularity: 0,
      };

      setFaqs([...faqs, newFaq]);
      setConfig({ ...config, total_faqs: config.total_faqs + 1 });
      setNewFaqQuestion("");
      setNewFaqAnswer("");
      setShowAddForm(false);
      alert("FAQ added successfully!");
    } catch (error) {
      alert("Failed to add FAQ");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteFAQ = async (id: number) => {
    if (confirm("Are you sure you want to delete this FAQ?")) {
      setFaqs(faqs.filter((f) => f.id !== id));
      setConfig({ ...config, total_faqs: config.total_faqs - 1 });
      alert("FAQ deleted successfully");
    }
  };

  const handleRebuildKnowledgeBase = async () => {
    setLoading(true);
    try {
      setConfig({ ...config, knowledge_base_status: "training" });
      // Simulate training
      setTimeout(() => {
        setConfig({ ...config, knowledge_base_status: "ready", last_updated: new Date().toISOString() });
        alert("Knowledge base rebuilt successfully!");
      }, 2000);
    } catch (error) {
      alert("Failed to rebuild knowledge base");
      setConfig({ ...config, knowledge_base_status: "ready" });
    } finally {
      setLoading(false);
    }
  };

  const handleTestChatbot = async () => {
    if (!testMessage.trim()) return;

    setChatHistory([...chatHistory, { role: "user", message: testMessage }]);
    setTestMessage("");
    setLoading(true);

    try {
      // Simulate API call
      setTimeout(() => {
        const responses = [
          "That's a great question! " + testMessage,
          "Based on our knowledge base, " + testMessage,
          "Here's what I found: " + testMessage,
        ];
        const botResponse = responses[Math.floor(Math.random() * responses.length)];
        setChatHistory((prev) => [...prev, { role: "bot", message: botResponse }]);
        setLoading(false);
      }, 500);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-gray-light min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-dark">AI Chatbot Management</h1>
        <button
          onClick={handleRebuildKnowledgeBase}
          disabled={loading || config.knowledge_base_status === "training"}
          className="px-4 py-2 bg-nust-blue text-white rounded hover:bg-blue-700 disabled:bg-gray-400 font-semibold flex items-center gap-2"
        >
          <RefreshCw size={18} /> {config.knowledge_base_status === "training" ? "Training..." : "Rebuild KB"}
        </button>
      </div>

      {/* Chatbot Status Card */}
      <div className="bg-gradient-to-r from-nust-blue to-mcs-red text-white p-6 rounded shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <p className="opacity-80 text-sm">Event</p>
            <p className="font-bold">{config.eventName}</p>
          </div>
          <div>
            <p className="opacity-80 text-sm">Status</p>
            <p className="font-bold">
              {config.knowledge_base_status === "ready" ? "✓ Ready" : config.knowledge_base_status === "training" ? "⏳ Training" : "❌ Empty"}
            </p>
          </div>
          <div>
            <p className="opacity-80 text-sm">FAQs in KB</p>
            <p className="font-bold">{config.total_faqs}</p>
          </div>
          <div>
            <p className="opacity-80 text-sm">Last Updated</p>
            <p className="font-bold text-sm">{new Date(config.last_updated).toLocaleDateString()}</p>
          </div>
        </div>
      </div>

      {/* FAQ Management */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        {/* FAQs List */}
        <div className="md:col-span-2 bg-white rounded shadow">
          <div className="flex justify-between items-center p-4 border-b">
            <h2 className="text-xl font-semibold text-gray-dark">FAQ Database</h2>
            <button
              onClick={() => setShowAddForm(!showAddForm)}
              className="px-3 py-1 bg-mcs-red text-white rounded hover:bg-red-700 text-sm font-semibold flex items-center gap-1"
            >
              <Plus size={16} /> Add FAQ
            </button>
          </div>

          {showAddForm && (
            <div className="p-4 bg-yellow-50 border-b">
              <input
                type="text"
                placeholder="Question..."
                value={newFaqQuestion}
                onChange={(e) => setNewFaqQuestion(e.target.value)}
                className="w-full px-3 py-2 border rounded mb-2 focus:outline-none focus:ring-2 focus:ring-mcs-red"
              />
              <textarea
                placeholder="Answer..."
                value={newFaqAnswer}
                onChange={(e) => setNewFaqAnswer(e.target.value)}
                rows={4}
                className="w-full px-3 py-2 border rounded mb-2 focus:outline-none focus:ring-2 focus:ring-mcs-red"
              />
              <select
                value={newFaqCategory}
                onChange={(e) => setNewFaqCategory(e.target.value)}
                className="w-full px-3 py-2 border rounded mb-2 focus:outline-none focus:ring-2 focus:ring-mcs-red"
              >
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
              <div className="flex gap-2">
                <button
                  onClick={handleAddFAQ}
                  disabled={loading}
                  className="flex-1 px-3 py-2 bg-mcs-red text-white rounded hover:bg-red-700 disabled:bg-gray-400 font-semibold"
                >
                  <Save className="inline mr-1" size={16} /> Save
                </button>
                <button
                  onClick={() => setShowAddForm(false)}
                  className="flex-1 px-3 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400 font-semibold"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          <div className="space-y-0">
            {faqs.map((faq, idx) => (
              <div key={faq.id} className={`p-4 ${idx !== faqs.length - 1 ? "border-b" : ""} hover:bg-gray-50 transition`}>
                <div className="flex justify-between items-start mb-2">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-dark">{faq.question}</h3>
                    <p className="text-sm text-gray-600 mt-1">{faq.answer}</p>
                  </div>
                  <div className="flex gap-1 ml-4">
                    <button className="px-2 py-1 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 text-sm">
                      <Edit2 size={14} />
                    </button>
                    <button onClick={() => handleDeleteFAQ(faq.id)} className="px-2 py-1 bg-red-200 text-red-700 rounded hover:bg-red-300 text-sm">
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>
                <div className="flex justify-between items-end text-xs text-gray-600">
                  <span className="px-2 py-1 bg-mcs-yellow text-mcs-red rounded font-semibold">{faq.category}</span>
                  <span>👥 {faq.popularity} views</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Test Chatbot */}
        <div className="bg-white rounded shadow flex flex-col">
          <h2 className="text-xl font-semibold text-gray-dark p-4 border-b flex items-center gap-2">
            <MessageSquare size={20} /> Test Chatbot
          </h2>

          <div className="flex-1 p-4 bg-gray-50 overflow-y-auto max-h-96 space-y-3 mb-3">
            {chatHistory.length === 0 ? (
              <div className="text-center text-gray-500 text-sm">
                <p>Start a conversation to test the chatbot</p>
              </div>
            ) : (
              chatHistory.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`px-3 py-2 rounded-lg text-sm max-w-xs ${
                      msg.role === "user" ? "bg-mcs-red text-white" : "bg-gray-300 text-gray-800"
                    }`}
                  >
                    {msg.message}
                  </div>
                </div>
              ))
            )}
            {loading && (
              <div className="flex justify-start">
                <div className="px-3 py-2 rounded-lg text-sm bg-gray-300 text-gray-800">⏳ Thinking...</div>
              </div>
            )}
          </div>

          <div className="p-4 border-t">
            <div className="flex gap-2">
              <input
                type="text"
                value={testMessage}
                onChange={(e) => setTestMessage(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleTestChatbot()}
                placeholder="Ask a question..."
                className="flex-1 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red text-sm"
              />
              <button
                onClick={handleTestChatbot}
                disabled={loading || !testMessage.trim()}
                className="px-3 py-2 bg-mcs-red text-white rounded hover:bg-red-700 disabled:bg-gray-400 text-sm font-semibold"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* AI Model Settings */}
      <div className="bg-white p-6 rounded shadow">
        <h2 className="text-xl font-semibold text-gray-dark mb-4">AI Model Configuration</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">AI Model</label>
            <select
              value={config.ai_model}
              onChange={(e) => setConfig({ ...config, ai_model: e.target.value as any })}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red"
            >
              <option value="groq-llama">Groq Llama 3.3 (Default)</option>
              <option value="gpt-3.5">GPT-3.5 Turbo</option>
              <option value="custom">Custom Model</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Training Mode</label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={config.trainingMode}
                onChange={(e) => setConfig({ ...config, trainingMode: e.target.checked })}
                className="w-4 h-4"
              />
              <span className="text-sm">{config.trainingMode ? "Enabled" : "Disabled"} - New conversations will improve the model</span>
            </label>
          </div>
        </div>
      </div>
    </div>
  );
}
