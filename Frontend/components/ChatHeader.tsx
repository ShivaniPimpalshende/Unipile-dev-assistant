"use client";

import { FiCpu } from "react-icons/fi";

export default function ChatHeader() {
  return (
    <div className="flex items-center justify-center p-4 bg-[#1b1f2d] border-b border-gray-700 shadow-md">
      <FiCpu className="text-blue-400 mr-3 text-3xl animate-bounce" />
      <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 animate-gradient-x">
        Unipile Dev Assistant
      </h1>
    </div>
  );
}
