'use client';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { useInView } from 'react-intersection-observer';

const stats = [
  { label: 'Projets Terminés', value: 120, suffix: '+' },
  { label: 'Experts IA', value: 25, suffix: '' },
  { label: 'Satisfaction', value: 99, suffix: '%' },
  { label: 'Taux de Conversion', value: 45, suffix: '%' },
];

function Counter({ value, suffix }: { value: number; suffix: string }) {
  const [count, setCount] = useState(0);
  const { ref, inView } = useInView({ triggerOnce: true });

  useEffect(() => {
    if (inView) {
      let start = 0;
      const end = value;
      const duration = 2000;
      const increment = end / (duration / 16);
      
      const timer = setInterval(() => {
        start += increment;
        if (start >= end) {
          setCount(end);
          clearInterval(timer);
        } else {
          setCount(Math.floor(start));
        }
      }, 16);
      return () => clearInterval(timer);
    }
  }, [inView, value]);

  return (
    <div ref={ref} className="text-6xl md:text-7xl font-syne font-bold flex items-center justify-center perspective-1000">
      <motion.div
        initial={{ rotateX: 90, opacity: 0 }}
        animate={inView ? { rotateX: 0, opacity: 1 } : {}}
        transition={{ duration: 1, ease: 'easeOut' }}
        className="flex items-center"
      >
        <motion.span
          animate={inView ? { filter: ['drop-shadow(0 0 0px transparent)', 'drop-shadow(0 0 15px rgba(79,142,247,0.5))', 'drop-shadow(0 0 5px rgba(79,142,247,0.2))'] } : {}}
          transition={{ delay: 2, duration: 2, repeat: Infinity }}
        >
          {count}
        </motion.span>
        <span className="text-accent">{suffix}</span>
      </motion.div>
    </div>
  );
}

export default function Stats() {
  return (
    <section className="py-40 relative overflow-hidden bg-[#08080f]">
       {/* 18. Stats background mesh gradient */}
      <motion.div 
        animate={{ 
          background: [
            'radial-gradient(circle at 20% 20%, #4f8ef7 0%, transparent 40%)',
            'radial-gradient(circle at 80% 80%, #4f8ef7 0%, transparent 40%)',
            'radial-gradient(circle at 20% 20%, #4f8ef7 0%, transparent 40%)',
          ]
        }}
        transition={{ duration: 8, repeat: Infinity }}
        className="absolute inset-0 opacity-[0.03]"
      />
      
      <div className="max-w-7xl mx-auto px-6 grid grid-cols-2 lg:grid-cols-4 gap-12 relative z-10">
        {stats.map((stat, i) => (
          <motion.div 
            key={i}
            initial={{ scale: 0.8, opacity: 0 }}
            whileInView={{ scale: 1, opacity: 1 }}
            transition={{ delay: i * 0.1 }}
            className="text-center space-y-4"
          >
            <Counter value={stat.value} suffix={stat.suffix} />
            <p className="text-secondary text-xs uppercase tracking-[0.3em] font-bold">{stat.label}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
