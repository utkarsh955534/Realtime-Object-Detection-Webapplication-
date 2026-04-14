import { useEffect, useRef, useState } from "react";
import axios from "axios";

export default function WebcamDetect() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const [detections, setDetections] = useState([]);
  const [error, setError] = useState("");

  // 🎥 Start webcam
  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
      })
      .catch(() => {
        setError("❌ Camera permission denied");
      });
  }, []);

  // 📸 Capture + Send to backend
  const capture = async () => {
    try {
      const token = localStorage.getItem("token");

      if (!token) {
        setError("❌ Please login again");
        return;
      }

      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");

      ctx.drawImage(videoRef.current, 0, 0, 320, 240);
      const img = canvas.toDataURL("image/jpeg");

      const res = await axios.post(
        `${process.env.REACT_APP_API}/api/detect/webcam`,
        { image: img },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setDetections(res.data.detections);
      setError("");

    } catch (err) {
      console.log("WEBCAM ERROR:", err.response?.data || err.message);

      if (err.response?.status === 401) {
        setError("❌ Unauthorized! Please login again");
      } else {
        setError("❌ Detection failed");
      }
    }
  };

  // 🔁 Run detection every 1.5 sec
  useEffect(() => {
    const interval = setInterval(() => {
      if (videoRef.current) {
        capture();
      }
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="card">
      <h3>Live Detection</h3>

      {/* Video */}
      <video
        ref={videoRef}
        autoPlay
        width="100%"
        style={{ borderRadius: "10px" }}
      />

      {/* Hidden canvas */}
      <canvas
        ref={canvasRef}
        width="640"
        height="480"
        hidden
      />

      {/* Error */}
      {error && (
        <p style={{ color: "red", marginTop: "10px" }}>
          {error}
        </p>
      )}

      {/* Results */}
      {detections.length > 0 && (
        <div style={{ marginTop: "10px" }}>
          <h4>Detected:</h4>

          {detections.map((d, i) => (
            <p key={i}>
              🧠 <b>{d.class}</b> → {(d.confidence * 100).toFixed(1)}%
            </p>
          ))}
        </div>
      )}
    </div>
  );
}
