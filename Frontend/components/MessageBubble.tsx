"use client";
import { Message } from "@/types/chat";
import { motion } from "framer-motion";

export default function MessageBubble({ msg }: { msg: Message }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ type: "spring", stiffness: 120 }}
      className={`flex mb-4 ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`p-4 max-w-[70%] rounded-2xl text-sm ${
          msg.sender === "user"
            ? "bg-blue-600 text-white rounded-br-none"
            : "bg-gray-700 text-gray-100 rounded-bl-none"
        }`}
      >
        {msg.text && <p className="mb-2 whitespace-pre-wrap">{msg.text}</p>}

        {msg.image && (
          <motion.img
            src={msg.image}
            alt="uploaded"
            className="rounded-lg max-h-60 border"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          />
        )}

        <span className="block text-xs opacity-70 mt-2 text-right">
          {msg.timestamp}
        </span>
      </div>
    </motion.div>
  );
}
