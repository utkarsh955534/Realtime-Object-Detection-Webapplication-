import axios from "axios";
import { useState } from "react";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const upload = async () => {
    // ❌ No file selected
    if (!file) {
      setMessage("❌ Please select a file first");
      return;
    }

    // 🔍 Debug token
    const token = localStorage.getItem("token");
    console.log("TOKEN:", token);

    if (!token) {
      setMessage("❌ Please login first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setMessage("");

      const res = await axios.post(
        `${process.env.REACT_APP_API}/api/detect/upload`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data"
          }
        }
      );

      setResult(res.data.detections);
      setMessage("✅ Detection successful!");

    } catch (err) {
      console.log("ERROR:", err.response?.data || err.message);

      if (err.response) {
        if (err.response.status === 401) {
          setMessage("❌ Unauthorized! Please login again");
        } else {
          setMessage("❌ " + (err.response.data.error || "Error occurred"));
        }
      } else {
        setMessage("❌ Server not reachable");
      }

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3>Upload Detection</h3>

      {/* File Input */}
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      {/* Button */}
      <button
        className="btn"
        onClick={upload}
        disabled={loading}
        style={{ marginTop: "10px" }}
      >
        {loading ? "Detecting..." : "Detect"}
      </button>

      {/* Message */}
      {message && (
        <p style={{ marginTop: "10px", color: "yellow" }}>
          {message}
        </p>
      )}

      {/* Results */}
      {result.length > 0 && (
        <div style={{ marginTop: "15px" }}>
          <h4>Results:</h4>

          {result.map((r, i) => (
            <p key={i}>
              🧠 <b>{r.class}</b> → {(r.confidence * 100).toFixed(1)}%
            </p>
          ))}
        </div>
      )}
    </div>
  );
}
