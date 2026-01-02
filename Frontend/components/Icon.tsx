"use client";
import { motion } from "framer-motion";

export default function Logo({ size = 64 }: { size?: number }) {
  return (
    <motion.svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      animate={{ rotate: [0, 15, -15, 0] }}
      transition={{ repeat: Infinity, duration: 3, ease: "easeInOut" }}
      className="drop-shadow-lg"
    >
      {/* Outer Circle */}
      <motion.circle
        cx="50"
        cy="50"
        r="45"
        stroke="url(#gradient)"
        strokeWidth="10"
        initial={{ opacity: 0.5 }}
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ repeat: Infinity, duration: 2 }}
      />

      {/* Inner “U” shape for Unipile */}
      <motion.path
        d="M30 70 V30 H50 V70 H30 Z"
        fill="url(#gradient)"
        animate={{ scale: [1, 1.1, 1] }}
        transition={{ repeat: Infinity, duration: 1.5, ease: "easeInOut" }}
      />

      {/* Gradient Definition */}
      <defs>
        <linearGradient id="gradient" x1="0" y1="0" x2="100%" y2="100%">
          <stop stopColor="#00f" />
          <stop offset="50%" stopColor="#a0f" />
          <stop offset="100%" stopColor="#f0f" />
        </linearGradient>
      </defs>
    </motion.svg>
  );
}
