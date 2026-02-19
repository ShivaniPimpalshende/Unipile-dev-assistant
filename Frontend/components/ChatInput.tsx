"use client";
import { useState } from "react";
import { FiImage } from "react-icons/fi";
import { fileToBase64 } from "@/utils/image";

export default function ChatInput({ onSend }: any) {
  const [text, setText] = useState("");
  const [image, setImage] = useState<File | null>(null);

  async function handleSend() {
    if (!text && !image) return;

    const img = image ? await fileToBase64(image) : null;
    onSend(text, img);

    setText("");
    setImage(null);
  }

  return (
    <div className="flex gap-3 p-4 bg-[#020617] border-t border-gray-700">
      <label className="cursor-pointer text-indigo-400 text-2xl flex items-center justify-center hover:text-indigo-300 transition-colors">
        <FiImage />
        <input
          type="file"
          hidden
          accept="image/*"
          onChange={(e) => setImage(e.target.files?.[0] || null)}
        />
      </label>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
        placeholder="Ask Unipile Dev Assistant..."
        className="flex-1 bg-gray-800 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
      />
      <button
        onClick={handleSend}
        className="bg-indigo-500 px-6 rounded-lg hover:bg-indigo-600 transition-colors"
      >
        Send
      </button>
    </div>
  );
}
