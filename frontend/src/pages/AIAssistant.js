import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import "./AI.css";

function AIAssistant({ setPage }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const token = localStorage.getItem("token");

  const logout = () => {
    localStorage.removeItem("token");
    setPage("login");
  };

  // =========================
  // SEND MESSAGE
  // =========================
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { type: "user", text: input };
    setMessages(prev => [...prev, userMsg]);

    try {
      const res = await fetch("http://127.0.0.1:8000/ai", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: token
        },
        body: JSON.stringify({ message: input })
      });

      const data = await res.json();

      const botMsg = {
        type: "bot",
        text: data.response || "No response"
      };

      setMessages(prev => [...prev, botMsg]);

    } catch (err) {
      setMessages(prev => [
        ...prev,
        { type: "bot", text: "❌ Server error" }
      ]);
    }

    setInput("");
  };

  return (
    <div className="layout">

      {/* SIDEBAR */}
      <Sidebar setPage={setPage} />

      <div className="content">

        {/* NAVBAR */}
        <Navbar onLogout={logout} />

        {/* HEADER */}
        <h1>🤖 AI Assistant</h1>

        {/* CHAT BOX */}
        <div className="chat-container">

          <div className="chat-box">

            {messages.length === 0 && (
              <div className="empty-chat">
                💬 Ask anything about AWS  
                <br />
                <span>Try: "show instances", "cost issues", "unused resources"</span>
              </div>
            )}

            {messages.map((msg, i) => (
              <div
                key={i}
                className={
                  msg.type === "user"
                    ? "chat-message user"
                    : "chat-message bot"
                }
              >
                {msg.text}
              </div>
            ))}

          </div>

          {/* INPUT */}
          <div className="chat-input">
            <input
              placeholder="Ask about AWS..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />

            <button onClick={sendMessage}>Send</button>
          </div>

        </div>

      </div>
    </div>
  );
}

export default AIAssistant;