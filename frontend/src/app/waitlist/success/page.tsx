'use client';
import React, { useEffect, useState } from 'react';
import { motion, useSpring, useTransform } from 'framer-motion';
import confetti from 'canvas-confetti';
import Link from 'next/link';
import { supabase } from '@/lib/supabase';
import { ArrowLeft } from 'lucide-react';

export default function SuccessPage() {
  const [position, setPosition] = useState(0);
  const springPos = useSpring(0, { stiffness: 40, damping: 20 });
  const displayPos = useTransform(springPos, (latest) => Math.floor(latest));

  useEffect(() => {
    confetti({
      particleCount: 150,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#000000', '#ffffff', '#6366f1']
    });

    const fetchPosition = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      if (user) {
        const { data } = await supabase
          .from('waitlist')
          .select('position')
          .eq('user_id', user.id)
          .single();
        if (data) setPosition(data.position);
      }
    };
    fetchPosition();
  }, []);

  useEffect(() => {
    springPos.set(position);
  }, [position, springPos]);

  const share = () => {
    navigator.clipboard.writeText(`${window.location.origin}/waitlist?ref=${position}`);
    alert('Referral link copied!');
  };

  return (
    <div className="min-h-screen bg-[#050505] text-white flex flex-col items-center justify-center p-6 relative overflow-hidden text-center">
      <div className="absolute inset-0 grainy-bg opacity-30 pointer-events-none" />
      
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
        className="z-10"
      >
        <h1 className="text-4xl md:text-5xl font-bold mb-4 tracking-tighter">You're on the list!</h1>
        <p className="text-white/40 uppercase tracking-[0.3em] text-[10px] mb-12">Queue position</p>
        
        <div className="mb-16">
          <motion.div className="text-[12rem] md:text-[16rem] font-bold line-height-none tracking-tighter italic text-accent">
            #{displayPos}
          </motion.div>
        </div>

        <div className="flex flex-col items-center gap-6">
          <button 
            onClick={share}
            className="px-10 py-4 border border-white/10 rounded-full text-xs uppercase tracking-widest font-bold hover:bg-white/5 transition-colors"
          >
            Share referral link
          </button>
          
          <Link href="/" className="flex items-center gap-2 text-white/40 hover:text-white transition-colors text-xs uppercase tracking-widest">
            <ArrowLeft size={14} /> Back to Home
          </Link>
        </div>
      </motion.div>
    </div>
  );
}
