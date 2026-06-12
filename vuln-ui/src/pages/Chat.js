import { useState } from "react";
import axios from "axios";
import "../styles.css";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const newChat = () => {
    setMessages([]);
    setInput("");
  };

  // 🔥 HANDLE FILE UPLOAD
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();

    reader.onload = (event) => {
      setInput(event.target.result);
    };

    reader.readAsText(file);
  };

  const send = async () => {
    if (!input.trim()) return;

    setMessages(prev => [...prev, { role: "user", text: input }]);
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:5000/predict", {
        code: input
      });

      setMessages(prev => [
        ...prev,
        { role: "bot", text: res.data.result }
      ]);

    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: "bot", text: "❌ Backend error. Check server." }
      ]);
    }

    setLoading(false);
    setInput("");
  };

  return (
    <div className="layout">

      {/* SIDEBAR */}
      <div className="sidebar">
        <h3 className="new-chat" onClick={newChat}>
          + New chat
        </h3>
        <div className="history">VulnScanner</div>
      </div>

      {/* MAIN */}
      <div className="main">

        <h2 className="title">VulnScanner</h2>

        {/* MESSAGES */}
        <div className="messages">
          {messages.map((m, i) => (
            <div key={i} className={`msg ${m.role}`}>

              {m.role === "user" && (
                <pre className="code">{m.text}</pre>
              )}

              {m.role === "bot" && (
                <div className="result">
                  {formatResponse(m.text)}
                </div>
              )}

            </div>
          ))}

          {loading && (
            <div className="msg bot">
              <div className="loading">
                🔄 Analyzing C Code for Vulnerabilities...
              </div>
            </div>
          )}
        </div>

        {/* INPUT BAR */}
        <div className="input-bar">

          {/* FILE UPLOAD BUTTON */}
          <label className="upload-btn">
            📁 Upload
            <input
              type="file"
              accept=".c,.txt"
              onChange={handleFileUpload}
              hidden
            />
          </label>

          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Paste C code or upload file..."
          />

          <button onClick={send}>⬆</button>
        </div>

      </div>
    </div>
  );
}


// 🔥 FORMAT RESPONSE
function formatResponse(text) {
  if (!text) return null;

  const isVuln = text.includes("Vulnerable");
  const parts = text.split("🧠 Explanation:");

  return (
    <>
      <div className={`status ${isVuln ? "danger" : "safe"}`}>
        {isVuln ? "⚠️ Vulnerable Code" : "✅ Safe Code"}
      </div>

      <pre className="prob">{parts[0]}</pre>

      {parts[1] && (
        <div className="explanation">
          <h3>Detected Vulnerabilities</h3>
          <pre>{parts[1]}</pre>
        </div>
      )}
    </>
  );
}