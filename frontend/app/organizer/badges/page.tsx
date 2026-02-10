"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { QRCodeSVG as QRCode } from "qrcode.react";
import { apiService } from "@/lib/apiService";
import { Download, Copy, Play, Save } from "lucide-react";

interface BadgeTemplate {
  id: string;
  name: string;
  layout: "vertical" | "horizontal";
  fields: string[];
  colors: { bg: string; text: string; accent: string };
}

interface BadgePreview {
  name: string;
  company: string;
  qrCode: string;
  badgeType: "VIP" | "Standard" | "Speaker";
}

const BADGE_TEMPLATES: BadgeTemplate[] = [
  {
    id: "template1",
    name: "Classic Vertical",
    layout: "vertical",
    fields: ["Name", "Company", "QR Code"],
    colors: { bg: "#FFFFFF", text: "#003366", accent: "#EE2022" },
  },
  {
    id: "template2",
    name: "Modern Horizontal",
    layout: "horizontal",
    fields: ["Name", "Title", "Company", "QR Code"],
    colors: { bg: "#003366", text: "#FFFFFF", accent: "#FED001" },
  },
  {
    id: "template3",
    name: "Minimal Design",
    layout: "vertical",
    fields: ["Name", "QR Code"],
    colors: { bg: "#F5F5F5", text: "#333333", accent: "#0072CE" },
  },
];

export default function BadgeDesignerPage() {
  const router = useRouter();
  const [selectedTemplate, setSelectedTemplate] = useState<BadgeTemplate>(BADGE_TEMPLATES[0]);
  const [customName, setCustomName] = useState("John Doe");
  const [customCompany, setCustomCompany] = useState("TechCorp Inc");
  const [customBadgeType, setCustomBadgeType] = useState<"VIP" | "Standard" | "Speaker">("Standard");
  const [showBulkPrint, setShowBulkPrint] = useState(false);
  const [loading, setLoading] = useState(false);
  const [qrValue, setQrValue] = useState("https://event.com/attendee/1");

  const handleTemplateSelect = (template: BadgeTemplate) => {
    setSelectedTemplate(template);
  };

  const handleGenerateQR = () => {
    const qr = `https://event.com/attendee/${Math.random().toString(36).substr(2, 9)}`;
    setQrValue(qr);
  };

  const handleDownloadPDF = async () => {
    setLoading(true);
    try {
      alert("Downloading badge as PDF...");
    } catch (error) {
      alert("Failed to download PDF");
    } finally {
      setLoading(false);
    }
  };

  const handlePrintMultiple = async () => {
    setLoading(true);
    try {
      alert("Preparing batch print preview...");
      setShowBulkPrint(true);
    } catch (error) {
      alert("Failed to prepare batch print");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-gray-light min-h-screen">
      <h1 className="text-3xl font-bold text-gray-dark mb-6">Badge Designer</h1>

      {/* Templates Section */}
      <div className="bg-white p-6 rounded shadow mb-6">
        <h2 className="text-xl font-semibold text-gray-dark mb-4">Pre-Designed Templates</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {BADGE_TEMPLATES.map((template) => (
            <div
              key={template.id}
              onClick={() => handleTemplateSelect(template)}
              className={`p-4 rounded border-2 cursor-pointer transition ${
                selectedTemplate.id === template.id ? "border-mcs-red bg-red-50" : "border-gray-300 hover:border-mcs-red"
              }`}
            >
              <h3 className="font-semibold text-gray-dark mb-2">{template.name}</h3>
              <div className={`p-4 rounded mb-2 text-center ${template.layout === "vertical" ? "h-32" : "h-20"}`} style={{ backgroundColor: template.colors.bg }}>
                <p style={{ color: template.colors.text }} className="text-sm font-semibold">
                  Sample Badge
                </p>
              </div>
              <p className="text-xs text-gray-600">Layout: {template.layout}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Badge Customization & Preview */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Customization Panel */}
        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-xl font-semibold text-gray-dark mb-4">Customize Badge</h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Attendee Name</label>
              <input
                type="text"
                value={customName}
                onChange={(e) => setCustomName(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Company</label>
              <input
                type="text"
                value={customCompany}
                onChange={(e) => setCustomCompany(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Badge Type</label>
              <select
                value={customBadgeType}
                onChange={(e) => setCustomBadgeType(e.target.value as "VIP" | "Standard" | "Speaker")}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-mcs-red"
              >
                <option value="Standard">Standard</option>
                <option value="VIP">VIP</option>
                <option value="Speaker">Speaker</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">QR Code Value</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={qrValue}
                  readOnly
                  className="flex-1 px-3 py-2 border rounded bg-gray-100 focus:outline-none"
                />
                <button onClick={handleGenerateQR} className="px-4 py-2 bg-nust-blue text-white rounded hover:bg-blue-700 font-semibold">
                  Generate
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Background Color</label>
              <div className="flex gap-2">
                <input
                  type="color"
                  defaultValue={selectedTemplate.colors.bg}
                  className="w-12 h-10 rounded cursor-pointer"
                />
                <input
                  type="text"
                  defaultValue={selectedTemplate.colors.bg}
                  readOnly
                  className="flex-1 px-3 py-2 border rounded bg-gray-100"
                />
              </div>
            </div>
          </div>

          <div className="mt-6 space-y-2">
            <button
              onClick={handleDownloadPDF}
              disabled={loading}
              className="w-full px-4 py-2 bg-mcs-red text-white rounded hover:bg-red-700 disabled:bg-gray-400 font-semibold flex items-center justify-center gap-2"
            >
              <Download size={18} /> {loading ? "Downloading..." : "Download Single Badge"}
            </button>
            <button
              onClick={handlePrintMultiple}
              disabled={loading}
              className="w-full px-4 py-2 bg-nust-blue text-white rounded hover:bg-blue-700 disabled:bg-gray-400 font-semibold flex items-center justify-center gap-2"
            >
              <Copy size={18} /> {loading ? "Preparing..." : "Batch Print Preview"}
            </button>
          </div>
        </div>

        {/* Badge Preview */}
        <div className="bg-white p-6 rounded shadow flex flex-col items-center justify-center">
          <h2 className="text-xl font-semibold text-gray-dark mb-4">Badge Preview</h2>

          <div
            className={`p-6 rounded shadow-lg border-4 flex flex-col items-center justify-center ${
              selectedTemplate.layout === "vertical" ? "w-64 h-96" : "w-96 h-48"
            }`}
            style={{
              backgroundColor: selectedTemplate.colors.bg,
              borderColor: selectedTemplate.colors.accent,
            }}
          >
            <div style={{ color: selectedTemplate.colors.text }} className="text-center">
              <h3 className="text-2xl font-bold mb-1">{customName}</h3>
              <p className="text-sm opacity-80 mb-3">{customCompany}</p>

              <div className="my-4 p-4 bg-white rounded inline-block">
                <QRCode value={qrValue} size={120} level="H" includeMargin={true} />
              </div>

              <div className="mt-4 flex items-center justify-center gap-2">
                <span
                  className={`px-4 py-1 rounded font-semibold text-white text-sm ${
                    customBadgeType === "VIP"
                      ? "bg-mcs-yellow text-mcs-red"
                      : customBadgeType === "Speaker"
                        ? "bg-nust-blue"
                        : "bg-gray-600"
                  }`}
                >
                  {customBadgeType}
                </span>
              </div>
            </div>
          </div>

          <p className="text-xs text-gray-600 mt-4 text-center">
            Template: {selectedTemplate.name} • Layout: {selectedTemplate.layout}
          </p>
        </div>
      </div>

      {/* Bulk Print Section */}
      {showBulkPrint && (
        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-xl font-semibold text-gray-dark mb-4">Batch Print Preview</h2>
          <p className="text-gray-600 mb-4">Select which badges to print from the list below:</p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
              <label key={i} className="flex items-center gap-2 p-3 border rounded hover:bg-gray-50 cursor-pointer">
                <input type="checkbox" defaultChecked className="w-4 h-4" />
                <span className="text-sm">Badge {i}</span>
              </label>
            ))}
          </div>

          <div className="flex gap-2">
            <button className="flex-1 px-4 py-2 bg-mcs-red text-white rounded hover:bg-red-700 font-semibold" onClick={() => window.print()}>
              Print Selected
            </button>
            <button className="flex-1 px-4 py-2 bg-mcs-yellow text-mcs-red rounded hover:bg-yellow-400 font-semibold">
              <Download className="inline mr-2" size={18} /> Export PDF
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
