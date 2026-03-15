'use client';
import { motion } from 'framer-motion';

const items = ["STRATÉGIE", "DESIGN", "DÉVELOPPEMENT", "MARKETING", "AI SOLUTIONS", "TRANSFORMATION DIGITALE"];

/**
 * Marquee Component
 * Infinite horizontal scrolling text with gradient highlight.
 */
export default function Marquee() {
  return (
    <div className="overflow-hidden whitespace-nowrap bg-accent py-12 flex relative">
      <motion.div
        animate={{ x: [0, -1000] }}
        transition={{
          repeat: Infinity,
          duration: 20,
          ease: "linear",
        }}
        className="flex space-x-12 px-6 items-center"
      >
        {[...items, ...items].map((item, i) => (
          <span 
            key={i} 
            className="text-4xl md:text-6xl font-syne font-bold text-background uppercase tracking-tighter"
          >
            {item}
            <span className="mx-12 opacity-20">/</span>
          </span>
        ))}
      </motion.div>
    </div>
  );
}
