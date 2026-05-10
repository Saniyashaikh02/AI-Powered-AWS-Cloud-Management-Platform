import React, { useState } from "react";
import "./Chatbot.css";

function Chatbot() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input) return;

    const userMsg = { user: input };
    setMessages(prev => [...prev, userMsg]);

    const res = await fetch("http://127.0.0.1:8000/ai", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: input })
    });

    const data = await res.json();

    const botMsg = { bot: data.response };
    setMessages(prev => [...prev, botMsg]);

    setInput("");
  };

  return (
    <div className="chatbot">

      <button className="chat-toggle" onClick={() => setOpen(!open)}>
        💬
      </button>

      {open && (
        <div className="chat-box">
          <div className="chat-header">🤖 AWS AI Assistant</div>

          <div className="chat-body">
            {messages.map((m, i) => (
              <div key={i} className={m.user ? "user" : "bot"}>
                {m.user || m.bot}
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Ask about AWS..."
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Chatbot;