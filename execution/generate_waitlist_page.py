import os

def generate_waitlist_page():
    base_dir = "frontend/src"
    
    # 1. Components
    components = {
        "components/waitlist/WaitlistCounter.tsx": """'use client';
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';
import { motion, useSpring, useTransform } from 'framer-motion';

export const WaitlistCounter = () => {
  const [count, setCount] = useState(0);
  const springCount = useSpring(0, { stiffness: 40, damping: 20 });
  const displayCount = useTransform(springCount, (latest) => Math.floor(latest));

  const fetchCount = async () => {
    const { count: total } = await supabase
      .from('waitlist')
      .select('*', { count: 'exact', head: true });
    setCount(total || 0);
  };

  useEffect(() => {
    fetchCount();
    
    // Realtime subscription
    const channel = supabase
      .channel('waitlist_changes')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'waitlist' }, () => {
        fetchCount();
      })
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  useEffect(() => {
    springCount.set(count);
  }, [count, springCount]);

  return (
    <div className="flex flex-col items-center gap-2">
      <motion.span className="text-6xl font-bold tracking-tighter">
        {displayCount}
      </motion.span>
      <span className="text-white/40 uppercase tracking-widest text-xs">Joined the revolution</span>
    </div>
  );
};
""",
        "components/waitlist/PositionCard.tsx": """'use client';
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
""",
    }

    # 2. Pages
    pages = {
        "app/waitlist/page.tsx": """'use client';
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { WaitlistCounter } from '@/components/waitlist/WaitlistCounter';
import { PositionCard } from '@/components/waitlist/PositionCard';
import { supabase } from '@/lib/supabase';
import { useRouter } from 'next/navigation';

export default function WaitlistPage() {
  const [user, setUser] = useState<any>(null);
  const [positionData, setPositionData] = useState<any>(null);
  const router = useRouter();

  useEffect(() => {
    const checkUser = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        router.push('/auth/login');
        return;
      }
      setUser(user);

      // Check if already in waitlist
      const { data: waitlistEntry } = await supabase
        .from('waitlist')
        .select('*')
        .eq('user_id', user.id)
        .single();

      if (waitlistEntry) {
        setPositionData(waitlistEntry);
      } else {
        // Join waitlist
        const { data: newEntry, error } = await supabase
          .from('waitlist')
          .insert({
            user_id: user.id,
            email: user.email!,
          })
          .select()
          .single();
        
        if (newEntry) setPositionData(newEntry);
      }
    };

    checkUser();
  }, [router]);

  return (
    <div className="min-h-screen bg-[#050505] text-white flex flex-col items-center justify-center p-6 relative overflow-hidden">
      <div className="absolute inset-0 bg-[#0a0a0a] opacity-50 grainy-bg pointer-events-none" />
      
      {/* Background Orbs */}
      <div className="absolute top-1/4 -left-20 w-96 h-96 bg-accent/20 rounded-full blur-[120px] animate-pulse" />
      <div className="absolute bottom-1/4 -right-20 w-96 h-96 bg-blue-500/10 rounded-full blur-[120px]" />

      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="z-10 text-center max-w-4xl"
      >
        {!positionData ? (
          <>
            <h1 className="text-7xl font-bold mb-6 tracking-tighter bg-gradient-to-r from-white to-white/40 bg-clip-text text-transparent">
              Be the first to know.
            </h1>
            <p className="text-xl text-white/60 mb-12">
              Join the waitlist and get early access to NexCore Studio.
            </p>
            <WaitlistCounter />
          </>
        ) : (
          <div className="flex flex-col items-center gap-12">
            <h2 className="text-5xl font-bold tracking-tight">Access Granted.</h2>
            <PositionCard position={positionData.position} email={positionData.email} />
            <WaitlistCounter />
          </div>
        )}
      </motion.div>

      {/* Footer link */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="absolute bottom-8 text-white/20 text-sm"
      >
        © 2024 NexCore Studio. All rights reserved.
      </motion.div>
    </div>
  );
}
"""
    }

    # Write all files
    all_files = {**components, **pages}
    for path, content in all_files.items():
        full_path = os.path.join(base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding='utf-8') as f:
            f.write(content)
        print(f"Generated: {full_path}")

if __name__ == "__main__":
    generate_waitlist_page()
