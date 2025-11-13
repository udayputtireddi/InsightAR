"use client";

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [caption, setCaption] = useState("");
  const [loading, setLoading] = useState(false);

  const upload = async () => {
    if (!file) {
      alert("Please select an image first!");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/analyze-image/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setCaption(res.data.caption);
    } catch {
      alert("Something went wrong. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto mt-6">
      <h1 className="text-3xl font-bold mb-6">🖼 InsightAR – Image Analyzer</h1>

      <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] || null)} className="mb-4" />

      <button onClick={upload} disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded">
        {loading ? "Analyzing..." : "Analyze Image"}
      </button>

      {caption && (
        <div className="mt-8 bg-white p-6 rounded shadow">
          <h2 className="text-xl font-semibold mb-3">Caption</h2>
          <p>{caption}</p>
        </div>
      )}
    </div>
  );
}
