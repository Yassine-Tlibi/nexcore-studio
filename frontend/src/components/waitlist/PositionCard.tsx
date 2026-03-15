'use client';
import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import confetti from 'canvas-confetti';

interface PositionCardProps {
  position: number;
  email: string;
}

export const PositionCard = ({ position, email }: PositionCardProps) => {
  useEffect(() => {
    const duration = 3 * 1000;
    const animationEnd = Date.now() + duration;
    const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

    const randomInRange = (min: number, max: number) => Math.random() * (max - min) + min;

    const interval: any = setInterval(function() {
      const timeLeft = animationEnd - Date.now();

      if (timeLeft <= 0) {
        return clearInterval(interval);
      }

      const particleCount = 50 * (timeLeft / duration);
      confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } });
      confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } });
    }, 250);

    return () => clearInterval(interval);
  }, []);

  const shareUrl = `${typeof window !== 'undefined' ? window.location.origin : ''}?ref=${email}`;

  const copyRef = () => {
    navigator.clipboard.writeText(shareUrl);
    alert('Referral link copied!');
  };

  return (
    <motion.div 
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className="p-10 rounded-3xl bg-accent text-white relative overflow-hidden group shadow-2xl"
    >
      <div className="relative z-10">
        <h3 className="text-xl font-medium opacity-80 mb-2">You're on the list!</h3>
        <div className="text-7xl font-bold mb-6 tracking-tight">#{position}</div>
        <p className="mb-8 opacity-70">Share with friends to move up the list.</p>
        <button 
          onClick={copyRef}
          className="w-full bg-white text-black py-4 rounded-full font-bold hover:bg-white/90 transition-all flex items-center justify-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6a3 3 0 100-2.684l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
          </svg>
          Copy Referral Link
        </button>
      </div>
      <div className="absolute top-0 right-0 -mr-10 -mt-10 w-40 h-40 bg-white/10 rounded-full blur-3xl group-hover:scale-110 transition-transform duration-700" />
    </motion.div>
  );
};
