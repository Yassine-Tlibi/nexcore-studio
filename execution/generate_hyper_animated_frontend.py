import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_frontend():
    # 1. Update globals.css with Grain, Mesh Gradients, and Typography
    globals_css = """@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Syne:wght@800&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: 8 8 15;
  --primary: 240 240 245;
  --secondary: 102 102 128;
  --accent: 79 142 247;
  --accent-rgb: 79, 142, 247;
}

body {
  background-color: rgb(var(--background));
  color: rgb(var(--primary));
  font-family: 'Inter', sans-serif;
  overflow-x: hidden;
}

.font-serif { font-family: 'Playfair Display', serif; }
.font-syne { font-family: 'Syne', sans-serif; }

/* 7. Entire page grain texture */
.grain::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.04;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  animation: noise 0.2s infinite;
}

@keyframes noise {
  0% { transform: translate(0,0) }
  10% { transform: translate(-1%,-1%) }
  20% { transform: translate(1%,1%) }
  30% { transform: translate(-2%,1%) }
  40% { transform: translate(2%,-1%) }
  50% { transform: translate(-1%,2%) }
  60% { transform: translate(1%,-2%) }
  70% { transform: translate(-1%,-1%) }
  80% { transform: translate(1%,1%) }
  90% { transform: translate(-2%,1%) }
  100% { transform: translate(0,0) }
}

/* 20. 3D Web Perspective */
.perspective-1000 {
  perspective: 1000px;
  transform-style: preserve-3d;
}

.preserve-3d {
  transform-style: preserve-3d;
}

/* 17. Glassmorphism */
.glass {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.rounded-blob {
  border-radius: 42% 58% 70% 30% / 45% 45% 55% 55%;
}
"""
    write_file('frontend/app/globals.css', globals_css)

    # 2. Rebuild layout.tsx (Preloader, Cursor, Lenis GSAP sync)
    layout_tsx = """import type { Metadata } from "next";
import "./globals.css";
import React from "react";
import SmoothScroll from "../components/hooks/SmoothScroll";
import Preloader from "../components/Preloader";
import CustomCursor from "../components/CustomCursor";

export const metadata: Metadata = {
  title: "NexCore Studio | Next-Gen Web & AI Strategy",
  description: "Excellence in digital transformation through motion and performance.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-background text-primary antialiased selection:bg-accent selection:text-background grain overflow-x-hidden">
        <Preloader />
        <CustomCursor />
        <SmoothScroll>
          {children}
        </SmoothScroll>
      </body>
    </html>
  );
}
"""
    write_file('frontend/app/layout.tsx', layout_tsx)

    # 3. Create Preloader.tsx (SVG Drawing)
    preloader_tsx = """'use client';
import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';

export default function Preloader() {
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress((prev) => (prev >= 100 ? 100 : prev + 2));
    }, 30);
    
    const timeout = setTimeout(() => {
      setLoading(false);
    }, 2800);

    return () => {
      clearInterval(timer);
      clearTimeout(timeout);
    };
  }, []);

  return (
    <AnimatePresence>
      {loading && (
        <motion.div
          exit={{ y: '-100%' }}
          transition={{ duration: 0.8, ease: [0.76, 0, 0.24, 1] }}
          className="fixed inset-0 z-[100] bg-[#08080f] flex flex-col items-center justify-center"
        >
          <div className="relative w-32 h-32 mb-8">
            <svg viewBox="0 0 100 100" className="w-full h-full">
              <motion.circle
                cx="50" cy="50" r="45"
                fill="none"
                stroke="#4f8ef7"
                strokeWidth="2"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 2, ease: "easeInOut" }}
              />
              <motion.path
                d="M30 50 L45 65 L70 35"
                fill="none"
                stroke="#4f8ef7"
                strokeWidth="4"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 1.5, delay: 0.5 }}
              />
            </svg>
          </div>
          <div className="w-64 h-[2px] bg-white/10 relative overflow-hidden">
            <motion.div 
              className="absolute inset-0 bg-accent"
              initial={{ scaleX: 0 }}
              animate={{ scaleX: progress / 100 }}
              style={{ originX: 0 }}
            />
          </div>
          <span className="mt-4 font-mono text-secondary text-xs tracking-widest">{progress}%</span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
"""
    write_file('frontend/components/Preloader.tsx', preloader_tsx)

    # 4. Create CustomCursor.tsx (Dot + Ghost Ring)
    cursor_tsx = """'use client';
import { useEffect, useRef, useState } from 'react';
import gsap from 'gsap';

export default function CustomCursor() {
  const dot = useRef<HTMLDivElement>(null);
  const ring = useRef<HTMLDivElement>(null);
  const [isClickable, setIsClickable] = useState(false);
  const [isImage, setIsImage] = useState(false);

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const moveCursor = (e: MouseEvent) => {
      gsap.to(dot.current, {
        x: e.clientX,
        y: e.clientY,
        duration: 0.1,
      });
      gsap.to(ring.current, {
        x: e.clientX,
        y: e.clientY,
        duration: 0.4,
        ease: 'power2.out',
      });

      const target = e.target as HTMLElement;
      setIsClickable(!!target.closest('button, a, input, textarea'));
      setIsImage(!!target.closest('img'));
    };

    window.addEventListener('mousemove', moveCursor);
    return () => window.removeEventListener('mousemove', moveCursor);
  }, []);

  return (
    <>
      <div 
        ref={dot} 
        className={`fixed top-0 left-0 w-2.5 h-2.5 bg-accent rounded-full pointer-events-none z-[9999] -translate-x-1/2 -translate-y-1/2 mix-blend-difference transition-opacity duration-300 ${isClickable ? 'opacity-0' : 'opacity-100'}`} 
      />
      <div 
        ref={ring} 
        className={`fixed top-0 left-0 w-9 h-9 border border-accent rounded-full pointer-events-none z-[9998] -translate-x-1/2 -translate-y-1/2 transition-all duration-300 ${isClickable ? 'w-14 h-14 bg-accent/20' : ''} ${isImage ? 'border-dashed' : ''}`} 
      />
    </>
  );
}
"""
    write_file('frontend/components/CustomCursor.tsx', cursor_tsx)

    # 5. Rebuild Hero.tsx (Splitting text, Particle Background, Ken Burns)
    hero_tsx = """'use client';
import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import gsap from 'gsap';
import MagneticButton from './MagneticButton';

export default function Hero() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let particles: any[] = [];
    const particleCount = 80;
    let w = window.innerWidth;
    let h = window.innerHeight;

    const resize = () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    };

    class Particle {
      x = Math.random() * w;
      y = Math.random() * h;
      vx = (Math.random() - 0.5) * 0.5;
      vy = (Math.random() - 0.5) * 0.5;

      update() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < 0 || this.x > w) this.vx *= -1;
        if (this.y < 0 || this.y > h) this.vy *= -1;
      }

      draw() {
        if (!ctx) return;
        ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.beginPath();
        ctx.arc(this.x, this.y, 1, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    for (let i = 0; i < particleCount; i++) particles.push(new Particle());

    const animate = () => {
      ctx.clearRect(0, 0, w, h);
      particles.forEach((p, i) => {
        p.update();
        p.draw();
        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
          if (dist < 120) {
            ctx.strokeStyle = `rgba(255, 255, 255, ${0.1 - dist / 1200})`;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
        }
      });
      requestAnimationFrame(animate);
    };

    resize();
    animate();
    window.addEventListener('resize', resize);
    return () => window.removeEventListener('resize', resize);
  }, []);

  const headline = "Stratégie Digitale & Solutions IA";
  const words = headline.split(" ");

  return (
    <section className="relative h-screen flex items-center justify-center overflow-hidden">
      <div className="absolute inset-0 bg-accent/5 overflow-hidden">
        <motion.div 
          animate={{ scale: [1, 1.08, 1] }}
          transition={{ duration: 12, repeat: Infinity, ease: "easeInOut" }}
          className="absolute inset-0 bg-[url('/hero-bg-dark.jpg')] bg-cover bg-center opacity-20"
        />
      </div>
      <canvas ref={canvasRef} className="absolute inset-0 pointer-events-none" />
      
      <div className="relative z-10 max-w-7xl px-6 text-center">
        <div className="overflow-hidden mb-6">
          <div className="flex flex-wrap justify-center gap-x-4">
            {words.map((word, i) => (
              <motion.span
                key={i}
                initial={{ y: 100, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ 
                  duration: 0.8, 
                  delay: i * 0.08,
                  ease: [0.33, 1, 0.68, 1]
                }}
                className="font-syne text-5xl md:text-8xl lg:text-9xl uppercase leading-none block"
              >
                {word}
              </motion.span>
            ))}
          </div>
        </div>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1, duration: 1 }}
          className="text-secondary text-lg md:text-xl max-w-2xl mx-auto mb-12 uppercase tracking-[0.2em] font-medium"
        >
          Nous créons des expériences numériques immersives qui transforment votre business.
        </motion.p>

        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 1.2, duration: 0.5, type: 'spring' }}
        >
          <MagneticButton>
            <button className="bg-accent text-background px-12 py-6 rounded-full font-bold uppercase tracking-widest text-sm hover:shadow-[0_0_30px_rgba(79,142,247,0.5)] transition-shadow">
              Démarrer un projet
            </button>
          </MagneticButton>
        </motion.div>
      </div>

      {/* Floating Shapes */}
      <motion.div 
        animate={{ y: [0, -40, 0] }}
        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-1/4 left-10 w-20 h-20 border border-accent/20 rounded-full"
      />
      <motion.div 
        animate={{ y: [0, 50, 0], rotate: 360 }}
        transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
        className="absolute bottom-1/4 right-20 w-32 h-32 border-2 border-accent/10 rounded-blob"
      />
    </section>
  );
}
"""
    write_file('frontend/components/Hero.tsx', hero_tsx)

    # 6. Create MagneticButton.tsx
    magnetic_tsx = """'use client';
import { useRef, useEffect } from 'react';
import gsap from 'gsap';

export default function MagneticButton({ children }: { children: React.ReactElement }) {
  const container = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const xTo = gsap.quickTo(container.current, "x", {duration: 1, ease: "elastic.out(1, 0.3)"});
    const yTo = gsap.quickTo(container.current, "y", {duration: 1, ease: "elastic.out(1, 0.3)"});

    const handleMouseMove = (e: MouseEvent) => {
      const { clientX, clientY } = e;
      const { left, top, width, height } = container.current!.getBoundingClientRect();
      const x = clientX - (left + width / 2);
      const y = clientY - (top + height / 2);
      
      const distance = Math.hypot(x, y);
      if (distance < 80) {
        xTo(x * 0.35);
        yTo(y * 0.35);
      } else {
        xTo(0);
        yTo(0);
      }
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return <div ref={container}>{children}</div>;
}
"""
    write_file('frontend/components/MagneticButton.tsx', magnetic_tsx)

    # 7. Rebuild Services.tsx (3D Tilt & Parallax Cards)
    services_tsx = """'use client';
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
"""
    write_file('frontend/components/Services.tsx', services_tsx)

    # 8. Create Page.tsx (Combine everything)
    page_tsx = """'use client';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import Marquee from '../components/Marquee';
import Services from '../components/Services';
import Methodology from '../components/Methodology';
import Contact from '../components/Contact';
import Footer from '../components/Footer';

export default function Home() {
  return (
    <main className="min-h-screen">
      <Navbar />
      <Hero />
      <Marquee />
      <Services />
      <Methodology />
      <Contact />
      <Footer />
    </main>
  );
}
"""
    write_file('frontend/app/page.tsx', page_tsx)

    print("Hyper-animated frontend successfully generated.")

if __name__ == "__main__":
    generate_frontend()
