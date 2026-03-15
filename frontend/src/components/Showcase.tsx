'use client';
import { motion } from 'framer-motion';
import { useRef, useState, useEffect } from 'react';

const projects = [
  { title: 'AI Automation Hub', category: 'Product Strategy', img: '/ai_automation_hub.png' },
  { title: 'NexCore Design System', category: 'Visual Identity', img: '/nexcore_design.png' },
  { title: 'Global Fintech Platform', category: 'Web Ecosystem', img: '/global_fintech.png' },
  { title: 'Neural Creative Engine', category: 'AI Integration', img: '/api/placeholder/800/600' },
];

export default function Showcase() {
  const scrollRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(0);

  useEffect(() => {
    if (!scrollRef.current || !containerRef.current) return;
    const scrollWidth = scrollRef.current.scrollWidth;
    const containerWidth = containerRef.current.offsetWidth;
    setWidth(scrollWidth - containerWidth);
  }, []);

  return (
    <section id="showcase" className="py-40 bg-[#08080f] overflow-hidden" ref={containerRef}>
      <div className="max-w-7xl mx-auto px-6 mb-20 flex justify-between items-end">
        <h2 className="font-syne text-6xl md:text-8xl uppercase">Selected <br/><span className="italic">Works.</span></h2>
        <div className="hidden md:flex items-center space-x-4 text-xs tracking-widest uppercase text-secondary">
          <span>Scroll to explore</span>
          <div className="w-12 h-[1px] bg-white/20" />
        </div>
      </div>

      <motion.div 
        ref={scrollRef}
        className="flex space-x-8 px-6 cursor-grab active:cursor-grabbing"
        drag="x"
        dragConstraints={{ left: -width, right: 0 }}
      >
        {projects.map((proj, i) => (
          <motion.div 
            key={i}
            className="min-w-[350px] md:min-w-[500px] aspect-[4/5] relative group rounded-3xl overflow-hidden perspective-1000"
          >
            <div className="absolute inset-0 bg-accent/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500 z-10" />
            <motion.img 
              src={proj.img}
              alt={proj.title}
              className="w-full h-full object-cover grayscale brightness-50 group-hover:scale-110 group-hover:grayscale-0 transition-all duration-1000"
            />
            <div className="absolute inset-0 p-12 flex flex-col justify-end z-20 translate-y-8 group-hover:translate-y-0 transition-transform duration-500">
              <span className="text-accent text-xs uppercase tracking-widest mb-2">{proj.category}</span>
              <h3 className="font-syne text-3xl uppercase text-white">{proj.title}</h3>
              <motion.button 
                className="mt-6 opacity-0 group-hover:opacity-100 transition-opacity flex items-center space-x-4"
              >
                 <span className="text-xs uppercase tracking-widest font-bold">View Case Study</span>
                 <div className="w-8 h-[1px] bg-accent" />
              </motion.button>
            </div>
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
}
