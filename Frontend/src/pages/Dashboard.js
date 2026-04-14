import Upload from "../components/Upload";
import WebcamDetect from "../components/WebcamDetect";
import { useNavigate } from "react-router-dom";

export default function Dashboard({ setAuth }) {
  const navigate = useNavigate();

  // 🔐 Logout function
  const handleLogout = () => {
    localStorage.removeItem("token");
    setAuth(null);   // 🔥 important
    navigate("/");
  };

  // 📜 History page navigation
  const goToHistory = () => {
    navigate("/history");
  };

  return (
    <div>
      <div className="navbar">
        <h2>AI Detection</h2>

        <div>
          <button className="btn" onClick={handleLogout}>
            Logout
          </button>

          <button
            className="btn"
            style={{ marginLeft: "10px" }}
            onClick={goToHistory}
          >
            History
          </button>
        </div>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "20px",
          padding: "20px"
        }}
      >
        <div className="card">
          <h3>Upload Detection</h3>
          <Upload />
        </div>

        <div className="card">
          <h3>Live Webcam</h3>
          <WebcamDetect />
        </div>
      </div>
    </div>
  );
}