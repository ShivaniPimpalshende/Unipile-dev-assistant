import { Message } from "@/types/chat";

export default function ChatMessage({ msg }: { msg: Message }) {
  return (
    <div
      className={`fade-in flex ${
        msg.sender === "user" ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-lg p-4 rounded-xl ${
          msg.sender === "user"
            ? "bg-indigo-500 text-white"
            : "bg-gray-800"
        }`}
      >
        {msg.image && (
          <img
            src={msg.image}
            className="mb-2 rounded-lg max-h-60"
          />
        )}
        {msg.text}
      </div>
    </div>
  );
}
