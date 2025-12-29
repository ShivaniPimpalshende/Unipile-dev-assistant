"use client";

import { useState, useRef, useEffect } from "react";

type Message = {
  text: string;
  sender: "user" | "assistant";
  timestamp: string;
};

type Chat = {
  id: number;
  title: string;
  messages: Message[];
};

export default function Home() {
  const [chats, setChats] = useState<Chat[]>([{ id: 1, title: "Chat 1", messages: [] }]);
  const [activeChatId, setActiveChatId] = useState(1);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const activeChat = chats.find((c) => c.id === activeChatId);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeChat?.messages, typing]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      text: input,
      sender: "user",
      timestamp: new Date().toLocaleTimeString(),
    };

    // Add user message to chat
    setChats((prev) =>
      prev.map((chat) =>
        chat.id === activeChatId
          ? { ...chat, messages: [...chat.messages, userMessage] }
          : chat
      )
    );

    setInput("");
    setTyping(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage.text }), // <- Important fix
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      const assistantMessage: Message = {
        text: data.answer,
        sender: "assistant",
        timestamp: new Date().toLocaleTimeString(),
      };

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeChatId
            ? { ...chat, messages: [...chat.messages, assistantMessage] }
            : chat
        )
      );
    } catch (err) {
      const errorMsg: Message = {
        text: "Error connecting to backend.",
        sender: "assistant",
        timestamp: new Date().toLocaleTimeString(),
      };
      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeChatId
            ? { ...chat, messages: [...chat.messages, errorMsg] }
            : chat
        )
      );
      console.error(err);
    } finally {
      setTyping(false);
    }
  };

  const startNewChat = () => {
    const newChat: Chat = {
      id: Date.now(),
      title: `Chat ${chats.length + 1}`,
      messages: [],
    };
    setChats((prev) => [...prev, newChat]);
    setActiveChatId(newChat.id);
  };

  return (
    <div className="min-h-screen flex bg-indigo-50">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-md flex flex-col">
        <div className="p-4 border-b font-bold text-xl">Chats</div>
        <div className="flex-1 overflow-y-auto">
          {chats.map((chat) => (
            <button
              key={chat.id}
              onClick={() => setActiveChatId(chat.id)}
              className={`w-full text-left p-3 border-b hover:bg-indigo-100 ${
                chat.id === activeChatId ? "bg-indigo-200 font-semibold" : ""
              }`}
            >
              {chat.title}
            </button>
          ))}
        </div>
        <button
          onClick={startNewChat}
          className="p-3 bg-indigo-500 text-white m-2 rounded-lg"
        >
          + New Chat
        </button>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col p-6">
        <div className="flex-1 bg-white shadow-xl rounded-3xl p-6 flex flex-col overflow-y-auto">
          {(activeChat?.messages || []).map((msg, idx) => (
            <div
              key={idx}
              className={`flex mb-4 ${
                msg.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`p-4 max-w-xs rounded-2xl ${
                  msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200"
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
          {typing && <div className="text-gray-400">Typing...</div>}
          <div ref={messagesEndRef} />
        </div>
        <div className="flex gap-2 mt-4">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            className="flex-1 border rounded-full p-3"
            placeholder="Type a message..."
          />
          <button
            onClick={sendMessage}
            className="bg-blue-500 text-white px-6 rounded-full"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
