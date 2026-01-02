"use client";

import { motion } from "framer-motion";
import { FiCpu } from "react-icons/fi";
import Icon from "./Icon"

export default function CenteredHeader({ active }: { active: boolean }) {
  if (active) return null;


  return (
    <div className="flex flex-col items-center justify-center h-full">
       
      <motion.div
        className="flex items-center gap-3"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, type: "spring", stiffness: 100 }}
      >
        {/* Animated Icon */}
        <motion.div
          animate={{ rotate: [0, 15, -15, 0] }}
          transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
        >
          <FiCpu className="text-6xl bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500" />
        </motion.div>

        {/* Animated Text */}
        <motion.h1
          className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500"
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ repeat: Infinity, duration: 2 }}
        >
          Unipile Dev Assistant
        </motion.h1>
      </motion.div>
      <Icon size={40} />

      <p className="text-gray-400 mt-4 text-center">
        Ask anything. Build faster.
      </p>
    </div>
  );
}
