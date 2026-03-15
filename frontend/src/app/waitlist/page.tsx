'use client';
import React, { useEffect, useState } from 'react';
import { motion, useSpring, useTransform } from 'framer-motion';
import MagneticButton from '@/components/MagneticButton';
import { useRouter } from 'next/navigation';
import { supabase } from '@/lib/supabase';

export default function WaitlistPage() {
  const [count, setCount] = useState(0);
  const router = useRouter();
  const springCount = useSpring(0, { stiffness: 40, damping: 20 });
  const displayCount = useTransform(springCount, (latest) => Math.floor(latest));

  useEffect(() => {
    const fetchCount = async () => {
      const { count: total } = await supabase
        .from('waitlist')
        .select('*', { count: 'exact', head: true });
      setCount(total || 0);
    };
    fetchCount();
  }, []);

  useEffect(() => {
    springCount.set(count);
  }, [count, springCount]);

  return (
    <div className="min-h-screen bg-[#050505] text-white flex flex-col items-center justify-center p-6 relative overflow-hidden">
      <div className="absolute inset-0 grainy-bg opacity-30 pointer-events-none" />
      
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
        className="text-center z-10"
      >
        <h1 className="text-7xl md:text-9xl font-bold tracking-tighter mb-8 italic">
          Be the first<br/>to know.
        </h1>
        <p className="text-xl text-white/40 mb-12 max-w-xl mx-auto uppercase tracking-widest font-light">
          Join the waitlist and get early access to NexCore Studio.
        </p>
        
        <div className="flex flex-col items-center gap-12">
          <MagneticButton onClick={() => router.push('/auth/login')}>
            <span className="px-12 py-5 bg-accent text-white rounded-full font-bold text-lg hover:scale-105 transition-transform block">
              Get Early Access
            </span>
          </MagneticButton>

          <div className="flex flex-col items-center">
            <motion.span className="text-6xl font-bold italic text-accent line-height-none mb-2">
              {displayCount}
            </motion.span>
            <span className="text-[10px] uppercase tracking-[0.3em] font-bold text-white/20">Users in queue</span>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
