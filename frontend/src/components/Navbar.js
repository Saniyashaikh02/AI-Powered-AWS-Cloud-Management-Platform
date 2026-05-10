import React from "react";
import "./Navbar.css";

function Navbar({ onLogout }) {
  return (
    <div className="navbar">
      <h2>🚀 AWS AI Dashboard</h2>

      <button onClick={onLogout}>Logout</button>
    </div>
  );
}

export default Navbar;