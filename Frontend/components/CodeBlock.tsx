"use client";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

export default function CodeBlock({ code }: { code: string }) {
  return (
    <SyntaxHighlighter language="javascript" style={oneDark} customStyle={{ background: "#0f111a" }}>
      {code}
    </SyntaxHighlighter>
  );
}
