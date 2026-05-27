import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [message, setMessage] = useState("");
  const [botResponse, setBotResponse] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [uploadStatus, setUploadStatus] = useState("");

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

  const fetchDocuments = async () => {
    const response = await fetch("http://127.0.0.1:8000/documents");
    const data = await response.json();
    setDocuments(data);
  }

  useEffect(() => {
    fetchDocuments();
  }, []);

  const uploadDocument = async() => {
    if (!selectedFile) {
      setUploadStatus("Please choose a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    const response = await fetch("http://127.0.0.1:8000/documents/upload", {
      method: "POST",
      body: formData,
    });
    
    if(!response.ok) {
      const error = await response.json();
      setUploadStatus(error.detail || "Upload failed.");
      return;
    }

    setUploadStatus("Upload successful.");
    setSelectedFile(null);
    fetchDocuments();
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

        <div className="upload-section">
          <h2>Upload Document</h2>

          <input
          type="file"
          accept=".txt"
          onChange={(e) => setSelectedFile(e.target.files[0])}
          />
          
          <button onClick={uploadDocument}>Upload</button>

          {uploadStatus && <p>{uploadStatus}</p>}

          <h3>Uploaded Documents</h3>

          {documents.length === 0 ? (
            <p>No documents uploaded yet.</p>
          ) : (
            <ul>
              {documents.map((doc) => (
                <li key={doc.id}>{doc.filename}</li>
              ))}
            </ul>
          )}
          </div>
    </div>
  );
}

export default App;