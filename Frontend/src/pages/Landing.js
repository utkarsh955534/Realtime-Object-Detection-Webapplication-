import { useNavigate } from "react-router-dom";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: "40px", textAlign: "center" }}>
      
      {/* Hero Section */}
      <h1 style={{ fontSize: "40px", marginBottom: "10px" }}>
        AI Object Detection 🚀
      </h1>

      <p style={{ opacity: 0.8, marginBottom: "30px" }}>
        Detect objects in real-time using YOLO with live webcam and image upload
      </p>

      {/* Buttons */}
      <div>
        <button
          className="btn"
          onClick={() => navigate("/login")}
          style={{ marginRight: "10px" }}
        >
          Get Started
        </button>

        <button
          className="btn"
          onClick={() => navigate("/register")}
        >
          Register
        </button>
      </div>

      {/* Features Section */}
      <div
        style={{
          marginTop: "60px",
          display: "grid",
          gridTemplateColumns: "1fr 1fr 1fr",
          gap: "20px"
        }}
      >
        <div className="card">
          <h3>📸 Upload Detection</h3>
          <p>Upload images and detect objects instantly</p>
        </div>

        <div className="card">
          <h3>🎥 Live Webcam</h3>
          <p>Real-time detection using your camera</p>
        </div>

        <div className="card">
          <h3>📊 History</h3>
          <p>Track your previous detections</p>
        </div>
      </div>
    </div>
  );
}