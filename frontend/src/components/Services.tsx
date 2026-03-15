'use client';
import { motion } from 'framer-motion';
import { useRef, useState } from 'react';
import gsap from 'gsap';

const services = [
  { id: '01', title: 'Consulting', desc: 'Audit stratégique et vision IA.', img: 'strategy_consulting_service_1773581169128.png' },
  { id: '02', title: 'Design UX', desc: 'Interfaces premium et intuitives.', img: 'ui_ux_design_service_1773581192338.png' },
  { id: '03', title: 'Web Development', desc: 'Applications Next.js ultra-rapides.', img: 'web_development_service_1773581214461.png' },
];

function ServiceCard({ svc }: { svc: any }) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [rotation, setRotation] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const card = cardRef.current;
    if (!card) return;
    const { left, top, width, height } = card.getBoundingClientRect();
    const x = e.clientX - left;
    const y = e.clientY - top;
    const rotateY = ((x - width / 2) / (width / 2)) * 12;
    const rotateX = ((y - height / 2) / (height / 2)) * -12;
    setRotation({ x: rotateX, y: rotateY });
  };

  const handleMouseLeave = () => setRotation({ x: 0, y: 0 });

  return (
    <motion.div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      animate={{ rotateX: rotation.x, rotateY: rotation.y }}
      transition={{ type: 'spring', stiffness: 150, damping: 20 }}
      className="perspective-1000 group cursor-pointer"
    >
      <div className="glass preserve-3d p-8 rounded-3xl h-full flex flex-col justify-between hover:border-accent/40 transition-colors duration-500">
        <div className="relative h-64 mb-8 overflow-hidden rounded-2xl">
           <motion.img 
              src={`/${svc.img}`}
              className="w-full h-full object-cover grayscale brightness-75 group-hover:scale-110 transition-transform duration-700" 
              whileHover={{ scale: 1.15 }}
           />
           <div className="absolute inset-0 bg-accent/20 mix-blend-overlay group-hover:opacity-100 opacity-0 transition-opacity duration-500" />
        </div>
        <div className="space-y-4">
          <span className="font-syne text-accent text-sm tracking-widest uppercase">{svc.id} / EXPERTISE</span>
          <h3 className="font-syne text-4xl uppercase">{svc.title}</h3>
          <p className="text-secondary leading-relaxed">{svc.desc}</p>
        </div>
        <div className="mt-8 pt-6 border-t border-white/5 flex justify-between items-center">
            <span className="text-xs uppercase tracking-tighter text-secondary">Ready for launch</span>
            <div className="w-10 h-10 rounded-full border border-accent flex items-center justify-center group-hover:bg-accent transition-all">
                <span className="text-accent group-hover:text-background font-bold">→</span>
            </div>
        </div>
      </div>
    </motion.div>
  );
}

export default function Services() {
  return (
    <section id="services" className="py-32 px-6 bg-[#08080f]">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-end mb-24">
          <h2 className="font-syne text-6xl md:text-8xl uppercase leading-none">Nos <br/><span className="text-accent">Services</span></h2>
          <p className="max-w-xs text-secondary text-sm uppercase tracking-widest mb-2">Architectes de votre futur numérique.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {services.map((svc) => (
            <ServiceCard key={svc.id} svc={svc} />
          ))}
        </div>
      </div>
    </section>
  );
}
