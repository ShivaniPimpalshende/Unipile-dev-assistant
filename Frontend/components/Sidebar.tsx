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
    <div className="w-64 bg-[#151926] flex flex-col">
      <div className="p-4 text-xl font-bold border-b border-gray-700">Chats</div>
      <div className="flex-1 overflow-y-auto">
        {chats.map((chat) => (
          <button
            key={chat.id}
            onClick={() => onSelect(chat.id)}
            className={`w-full text-left p-3 border-b border-gray-700 hover:bg-[#1f2233] ${
              chat.id === activeId ? "bg-[#2a2f45] font-semibold" : ""
            }`}
          >
            {chat.title}
          </button>
        ))}
      </div>
      <button
        onClick={onNewChat}
        className="p-3 bg-blue-600 text-white m-2 rounded-lg hover:bg-blue-700"
      >
        + New Chat
      </button>
    </div>
  );
}
