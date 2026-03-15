'use client';
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
