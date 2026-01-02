export async function sendChatMessage({
  message,
  image,
}: {
  message: string;
  image?: string;
}) {
  await new Promise((r) => setTimeout(r, 1000)); // simulate delay
  return {
    answer: `Assistant: I received your message -> "${message}"`,
    timestamp: new Date().toLocaleTimeString(),
  };
}
