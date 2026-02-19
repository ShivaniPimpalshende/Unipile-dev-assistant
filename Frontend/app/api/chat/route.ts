// // app/api/chat/route.ts
// import { NextRequest, NextResponse } from "next/server";

// export async function POST(req: NextRequest) {
//   const body = await req.json();

//   // Forward request to FastAPI backend
//   const res = await fetch("http://127.0.0.1:8000/chat", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify(body),
//   });

//   const data = await res.json();
//   return NextResponse.json(data);
// }
