import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Login({ setAuth }) {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");   // 🔥 message state

  const login = async () => {
    try {
      const res = await axios.post(
        "http://localhost:5000/api/auth/login",
        { email, password }
      );

      // ✅ store token
      localStorage.setItem("token", res.data.token);

      // ✅ update auth state (important if using App state)
      if (setAuth) setAuth(res.data.token);

      setMessage("✅ Login successful!");

      // 🔥 redirect after short delay
      setTimeout(() => {
        navigate("/dashboard");
      }, 1000);

    } catch (err) {
      if (err.response) {
        setMessage("❌ " + err.response.data.error);
      } else {
        setMessage("❌ Server error");
      }
    }
  };

  return (
    <div className="center-container">
      <div className="card">
        <h2>Login</h2>

        <input
          className="input"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          className="input"
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="btn" onClick={login}>
          Login
        </button>

        <button
          className="btn"
          onClick={() => navigate("/register")}
          style={{ marginLeft: "20px" }}
        >
          Register
        </button>

        {/* 🔥 Show message */}
        {message && (
          <p style={{ marginTop: "10px", color: "yellow" }}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
}