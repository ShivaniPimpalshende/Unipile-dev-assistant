import ChatMessage from "./ChatMessage";
import CenterHeader from "./CenterHeader";

export default function ChatWindow({ messages }: any) {
  return (
    <div className="flex-1 p-6 overflow-y-auto">
      <CenterHeader active={messages.length > 0} />

      <div className="space-y-4">
        {messages.map((m: any, i: number) => (
          <ChatMessage key={i} msg={m} />
        ))}
      </div>
    </div>
  );
}
