export type Message = {
  text?: string;
  image?: string;
  sender: "user" | "assistant";
  timestamp: string;
};

export type Chat = {
  id: number;
  title: string;
  messages: Message[];
};
