"use client";

import { useState } from "react";
import axios from "axios";

export default function DocumentAnalyzer() {
  const [file, setFile] = useState<File | null>(null);
  const [summary, setSummary] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState<"summary" | "qa">("summary");

  const handleSubmit = async () => {
    if (!file) {
      alert("Please upload a PDF first!");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      if (mode === "summary") {
        const res = await axios.post("http://127.0.0.1:8000/analyze-doc/", formData);
        setSummary(res.data.summary);
        setAnswer("");
      } else {
        formData.append("question", question);
        const res = await axios.post("http://127.0.0.1:8000/ask-doc/", formData);
        setAnswer(res.data.answer);
        setSummary("");
      }
    } catch {
      alert("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto mt-6">
      <h1 className="text-3xl font-bold mb-6">📄 InsightAR – Document Analyzer</h1>

      <input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files?.[0] || null)} className="mb-4" />

      <div className="flex gap-4 mb-4">
        <button className={`px-4 py-2 rounded ${mode === "summary" ? "bg-blue-600 text-white" : "bg-gray-200"}`}
          onClick={() => setMode("summary")}>
          Summarize
        </button>

        <button className={`px-4 py-2 rounded ${mode === "qa" ? "bg-blue-600 text-white" : "bg-gray-200"}`}
          onClick={() => setMode("qa")}>
          Ask Question
        </button>
      </div>

      {mode === "qa" && (
        <input type="text" placeholder="Type your question…" className="border p-2 rounded w-full mb-4"
          value={question} onChange={(e) => setQuestion(e.target.value)} />
      )}

      <button onClick={handleSubmit} disabled={loading} className="bg-green-600 text-white px-4 py-2 rounded">
        {loading ? "Processing…" : mode === "summary" ? "Summarize Document" : "Get Answer"}
      </button>

      {summary && (
        <div className="mt-8 bg-white p-6 rounded shadow">
          <h2 className="text-xl font-semibold mb-2">📝 Summary</h2>
          <p>{summary}</p>
        </div>
      )}

      {answer && (
        <div className="mt-8 bg-white p-6 rounded shadow">
          <h2 className="text-xl font-semibold mb-2">💬 Answer</h2>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}
