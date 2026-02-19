"use client";

import { Chat } from "@/types/chat";

interface SidebarProps {
  chats: Chat[];
  activeId: number;
  onSelect: (id: number) => void;
  onNewChat: () => void;
}

export default function Sidebar({ chats, activeId, onSelect, onNewChat }: SidebarProps) {
  return (
    <div className="w-72 bg-gray-900 border-r border-gray-700 flex flex-col">
      {/* Header */}
      <div className="p-4 text-lg font-bold text-white border-b border-gray-700">
        💬 Chat History
      </div>

      {/* Chat List */}
      <div className="flex-1 overflow-y-auto">
        {chats.map((chat) => (
          <button
            key={chat.id}
            onClick={() => onSelect(chat.id)}
            className={`w-full px-4 py-3 text-left transition-all ${
              chat.id === activeId
                ? "bg-gradient-to-r from-blue-600/30 to-purple-600/30 text-white"
                : "hover:bg-gray-800 text-gray-300"
            }`}
          >
            🧠 {chat.title}
          </button>
        ))}
      </div>

      {/* New Chat Button */}
      <button
        onClick={onNewChat}
        className="m-3 p-3 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold hover:opacity-90"
      >
        + New Chat
      </button>
    </div>
  );
}
