import { useState, useEffect } from "react";

interface ChatItem {
  question: string;
  answer: string;
  timestamp: string;
}

export default function ChatApp() {
  const [history, setHistory] = useState<ChatItem[]>([]);
  const [message, setMessage] = useState("");

  // Load history
  const fetchHistory = () => {
    fetch("http://127.0.0.1:8000/history?limit=50")
      .then((res) => res.json())
      .then((data) => setHistory(data.history))
      .catch((err) => console.error(err));
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const sendMessage = () => {
    if (!message.trim()) return;
    fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    })
      .then((res) => res.json())
      .then((data) => {
        setHistory((prev) => [data, ...prev]);
        setMessage("");
      });
  };

  return (
    <div className="max-w-xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Unipile Dev Assistant</h1>

      <div className="space-y-4 mb-4 max-h-[60vh] overflow-y-auto">
        {history.map((chat, idx) => (
          <div key={idx} className="p-3 border rounded shadow-sm">
            <p>
              <strong>User:</strong> {chat.question}
            </p>
            <p>
              <strong>Assistant:</strong> {chat.answer}
            </p>
            <p className="text-xs text-gray-400">
              {new Date(chat.timestamp).toLocaleString()}
            </p>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 p-2 border rounded"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask a question..."
        />
        <button
          className="bg-indigo-500 text-white px-4 rounded"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}
