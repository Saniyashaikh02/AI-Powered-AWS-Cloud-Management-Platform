import React, { useState } from "react";
import "./Auth.css";

function Login({ setPage }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username: username,
          password: password
        })
      });

      const data = await res.json();

      if (res.status === 200) {
        // ✅ save token
        localStorage.setItem("token", data.access_token);

        // 🚀 DIRECT redirect (NO ALERT)
        setPage("dashboard");

      } else {
        alert(data.detail || "Login failed ❌");
      }

    } catch (err) {
      alert("Server error ❌");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2>Welcome Back 👋</h2>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleLogin}>Login</button>

        <p>
          Don’t have an account?{" "}
          <span onClick={() => setPage("register")}>
            Register
          </span>
        </p>
      </div>
    </div>
  );
}

export default Login;