'use client';
import { motion } from 'framer-motion';
import React from 'react';

export const AuthCard = ({ children }: { children: React.ReactNode }) => {
  return (
    <motion.div 
      initial={{ y: 40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
      className="p-8 rounded-3xl border border-white/10 bg-white/5 backdrop-blur-2xl shadow-2xl relative group w-full max-w-md"
    >
      <div className="absolute -inset-[1px] bg-gradient-to-r from-accent/30 to-transparent rounded-[24px] opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none" />
      {children}
    </motion.div>
  );
};
