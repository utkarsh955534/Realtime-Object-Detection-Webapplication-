import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const register = async () => {
    try {
      const res = await axios.post(
        `${process.env.REACT_APP_API}/api/auth/register`,
        { email, password }
      );

      setMessage("✅ Registered successfully!");

      // 🔥 redirect after 1 sec
      setTimeout(() => {
        navigate("/login");
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
        <h2>Register</h2>

        <input
          className="input"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          className="input"
          placeholder="Password"
          type="password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="btn" onClick={register}>
          Register
        </button>

        {message && (
          <p style={{ marginTop: "10px", color: "yellow" }}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
}
