'use client';
import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';

export default function Preloader() {
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress((prev) => (prev >= 100 ? 100 : prev + 2));
    }, 30);
    
    const timeout = setTimeout(() => {
      setLoading(false);
    }, 2800);

    return () => {
      clearInterval(timer);
      clearTimeout(timeout);
    };
  }, []);

  return (
    <AnimatePresence>
      {loading && (
        <motion.div
          exit={{ y: '-100%' }}
          transition={{ duration: 0.8, ease: [0.76, 0, 0.24, 1] }}
          className="fixed inset-0 z-[100] bg-[#08080f] flex flex-col items-center justify-center"
        >
          <div className="relative w-32 h-32 mb-8">
            <svg viewBox="0 0 100 100" className="w-full h-full">
              <motion.circle
                cx="50" cy="50" r="45"
                fill="none"
                stroke="#4f8ef7"
                strokeWidth="2"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 2, ease: "easeInOut" }}
              />
              <motion.path
                d="M30 50 L45 65 L70 35"
                fill="none"
                stroke="#4f8ef7"
                strokeWidth="4"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 1.5, delay: 0.5 }}
              />
            </svg>
          </div>
          <div className="w-64 h-[2px] bg-white/10 relative overflow-hidden">
            <motion.div 
              className="absolute inset-0 bg-accent"
              initial={{ scaleX: 0 }}
              animate={{ scaleX: progress / 100 }}
              style={{ originX: 0 }}
            />
          </div>
          <span className="mt-4 font-mono text-secondary text-xs tracking-widest">{progress}%</span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
