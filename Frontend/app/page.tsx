"use client";

import { useState, useEffect, useRef } from "react";
import CenterHeader from "@/components/CenterHeader";
import MessageBubble from "@/components/MessageBubble";
import ChatInput from "@/components/ChatInput";
import TypingIndicator from "@/components/TypingIndicator";

type Message = {
  text?: string;
  image?: string;
  sender: "user" | "assistant";
  timestamp: string;
};

type Chat = {
  id: number;
  title: string;
  messages: Message[];
};

export default function Home() {
  

useEffect(() => {
  const fetchHistory = async () => {
    const res = await fetch(`http://127.0.0.1:8000/user_history/user123`);
    const data = await res.json();
    setChats(data.chats); // overwrite initial chat state with history
  };

  fetchHistory();
}, []);

  const [chats, setChats] = useState<Chat[]>([
    { id: 1, title: "Chat 1", messages: [] },
  ]);
  const [activeChatId, setActiveChatId] = useState<number>(1);
  const [typing, setTyping] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const activeChat = chats.find((c) => c.id === activeChatId);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeChat?.messages, typing]);

  // ---------------- SEND MESSAGE ----------------
  const sendMessage = async (text: string, image?: string) => {
    const userMessage: Message = {
      text,
      image,
      sender: "user",
      timestamp: new Date().toLocaleTimeString(),
    };

    setChats((prev) =>
      prev.map((chat) =>
        chat.id === activeChatId
          ? { ...chat, messages: [...chat.messages, userMessage] }
          : chat
      )
    );

    setTyping(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, image, user_id: "user123"  }),
      });

      const data = await res.json();

      const assistantMessage: Message = {
        text: data.answer || "No response from server.",
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
    } catch (error) {
      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeChatId
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    text: "⚠️ Error connecting to backend",
                    sender: "assistant",
                    timestamp: new Date().toLocaleTimeString(),
                  },
                ],
              }
            : chat
        )
      );
    } finally {
      setTyping(false);
    }
  };

  // ---------------- NEW CHAT ----------------
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
    <div className="min-h-screen flex bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900">

      {/* ================= SIDEBAR ================= */}
      <div className="w-72 bg-gray-900 border-r border-gray-700 flex flex-col">
        <div className="p-4 text-lg font-bold text-white border-b border-gray-700">
          💬 Chat History
        </div>

        <div className="flex-1 overflow-y-auto">
          {chats.map((chat) => (
            <button
              key={chat.id}
              onClick={() => setActiveChatId(chat.id)}
              className={`w-full px-4 py-3 text-left transition-all
                ${
                  chat.id === activeChatId
                    ? "bg-gradient-to-r from-blue-600/30 to-purple-600/30 text-white"
                    : "hover:bg-gray-800 text-gray-300"
                }`}
            >
              🧠 {chat.title}
            </button>
          ))}
        </div>

        <button
          onClick={startNewChat}
          className="m-3 p-3 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold hover:opacity-90"
        >
          + New Chat
        </button>
      </div>

      {/* ================= MAIN CHAT ================= */}
      <div className="flex-1 flex flex-col p-6 relative">

        {/* ⭐ CENTERED / MOVING HEADER */}
        <CenterHeader active={!!activeChat?.messages.length} />

        {/* CHAT MESSAGES */}
        <div className="flex-1 bg-gray-800 rounded-3xl shadow-xl p-6 overflow-y-auto mt-6">
          {(activeChat?.messages || []).map((msg, idx) => (
            <MessageBubble key={idx} msg={msg} />
          ))}

          {typing && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>

        {/* INPUT */}
        <ChatInput onSend={sendMessage} />
      </div>
    </div>
  );
}