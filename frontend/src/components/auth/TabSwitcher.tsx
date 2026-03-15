'use client';
import { motion } from 'framer-motion';
import React from 'react';

export const TabSwitcher = ({ active, onChange }: { active: 'login' | 'signup', onChange: (t: 'login' | 'signup') => void }) => {
  return (
    <div className="flex gap-8 mb-10 border-b border-white/5 relative">
      <button 
        onClick={() => onChange('login')}
        className={`pb-4 text-sm uppercase tracking-widest transition-colors ${active === 'login' ? 'text-white' : 'text-white/40 hover:text-white/60'}`}
      >
        Sign In
      </button>
      <button 
        onClick={() => onChange('signup')}
        className={`pb-4 text-sm uppercase tracking-widest transition-colors ${active === 'signup' ? 'text-white' : 'text-white/40 hover:text-white/60'}`}
      >
        Sign Up
      </button>
      <motion.div 
        layoutId="tab-underline"
        className="absolute bottom-0 h-[2px] bg-accent"
        initial={false}
        animate={{ 
          left: active === 'login' ? 0 : '88px',
          width: active === 'login' ? '54px' : '62px'
        }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      />
    </div>
  );
};
