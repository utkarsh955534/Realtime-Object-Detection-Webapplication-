import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import Landing from "./pages/Landing";

function App() {
  const [auth, setAuth] = useState(localStorage.getItem("token"));

  return (
    <BrowserRouter>
      <Routes>

        {/* 🔥 Landing Page */}
        <Route path="/" element={<Landing />} />

        {/* 🔐 Login */}
        <Route
          path="/login"
          element={auth ? <Navigate to="/dashboard" /> : <Login setAuth={setAuth} />}
        />

        {/* 📝 Register */}
        <Route path="/register" element={<Register />} />

        {/* 📊 Dashboard */}
        <Route
          path="/dashboard"
          element={auth ? <Dashboard setAuth={setAuth} /> : <Navigate to="/login" />}
        />

        {/* 📜 History */}
        <Route
          path="/history"
          element={auth ? <History /> : <Navigate to="/login" />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;