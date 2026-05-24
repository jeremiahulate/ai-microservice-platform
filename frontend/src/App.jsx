import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [message, setMessage] = useState("");
  const [botResponse, setBotResponse] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/health")
      .then((res) => res.json())
      .then((data) => setBackendStatus(data.status))
      .catch(() => setBackendStatus("Backend not connected"));
  }, []);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    setBotResponse(data.bot_response);
  };

  return (
    <div className="app">
      <h1>AI Microservice Platform</h1>

      <p>
        Backend status: <strong>{backendStatus}</strong>
      </p>

      <div className="chat-box">
        <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message..."
        />

        <button onClick={sendMessage}>Send</button>
      </div>

      {botResponse && (
        <div className="response">
          <h3>Bot Response</h3>
          <p>{botResponse}</p>
          </div>
      )}
    </div>
  );
}

export default App;