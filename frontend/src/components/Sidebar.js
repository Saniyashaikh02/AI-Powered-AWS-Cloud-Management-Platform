import React, { useState } from "react";
import "./Sidebar.css";

function Sidebar({ setPage }) {
  const [active, setActive] = useState("dashboard");

  const change = (page) => {
    setActive(page);
    setPage(page);
  };

  return (
    <div className="sidebar">
      <h2>⚡ AWS AI</h2>

      <div 
        className={active==="dashboard" ? "active" : ""} 
        onClick={() => change("dashboard")}
      >
        📊 Dashboard
      </div>

      <div 
        className={active==="ai" ? "active" : ""} 
        onClick={() => change("ai")}
      >
        🤖 AI Assistant
      </div>

      <div>🪣 S3</div>
      <div>💰 Cost</div>
    </div>
  );
}

export default Sidebar;