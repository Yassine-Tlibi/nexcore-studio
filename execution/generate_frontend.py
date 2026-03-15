import os
import argparse
import subprocess

def create_files(root: str):
    files = {
        "frontend/package.json": """{
  "name": "agency-website",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "react": "^18",
    "react-dom": "^18",
    "next": "^14.2.0",
    "framer-motion": "^11.0.0",
    "gsap": "^3.12.5",
    "@studio-freight/lenis": "^1.0.42",
    "lucide-react": "^0.368.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.2"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "postcss": "^8",
    "autoprefixer": "^10.4.19",
    "tailwindcss": "^3.4.1",
    "eslint": "^8",
    "eslint-config-next": "14.2.0"
  }
}
""",
        "frontend/tsconfig.json": """{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
""",
        "frontend/tailwind.config.ts": """import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#08080f",
        primary: "#f0f0f5",
        secondary: "#666680",
        accent: "#4f8ef7",
        teal: "#1d9e75",
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
      }
    },
  },
  plugins: [],
};
export default config;
""",
        "frontend/postcss.config.js": """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""",
        "frontend/app/globals.css": """@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300;1,400;1,500&family=Syne:wght@400..800&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: #08080f;
  --foreground: #f0f0f5;
}

body {
  color: var(--foreground);
  background: var(--background);
  font-family: 'DM Mono', monospace;
  overflow-x: hidden;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Syne', sans-serif;
}

/* Grain texture overlay */
body::before {
  content: "";
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.05;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}

/* Hide scrollbar for cleaner look */
::-webkit-scrollbar {
  display: none;
}
""",
        "frontend/app/layout.tsx": """import type { Metadata } from "next";
import "./globals.css";
import React from "react";
import LoadingScreen from "../components/LoadingScreen";
import CustomCursor from "../components/CustomCursor";
import ScrollProgressBar from "../components/ScrollProgressBar";
import SmoothScroll from "../components/hooks/SmoothScroll";

export const metadata: Metadata = {
  title: "NexCore Studio | Web & AI Agency",
  description: "Premium Digital Agency",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-background text-primary antialiased selection:bg-accent selection:text-white">
        <LoadingScreen />
        <CustomCursor />
        <ScrollProgressBar />
        <SmoothScroll>
          {children}
        </SmoothScroll>
      </body>
    </html>
  );
}
""",
        "frontend/components/hooks/SmoothScroll.tsx": """'use client';
import { useEffect } from 'react';
import Lenis from '@studio-freight/lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export default function SmoothScroll({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 1,
      touchMultiplier: 2,
    });

    lenis.on('scroll', ScrollTrigger.update);

    gsap.ticker.add((time) => {
      lenis.raf(time * 1000);
    });

    gsap.ticker.lagSmoothing(0);

    return () => {
      lenis.destroy();
    };
  }, []);

  return <>{children}</>;
}
""",
        "frontend/components/CustomCursor.tsx": """'use client';
import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export default function CustomCursor() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    const updateMousePosition = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    const handleMouseOver = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (target.closest('a') || target.closest('button') || target.tagName.toLowerCase() === 'a' || target.tagName.toLowerCase() === 'button') {
        setIsHovered(true);
      } else {
        setIsHovered(false);
      }
    };

    window.addEventListener('mousemove', updateMousePosition);
    window.addEventListener('mouseover', handleMouseOver);

    return () => {
      window.removeEventListener('mousemove', updateMousePosition);
      window.removeEventListener('mouseover', handleMouseOver);
    };
  }, []);

  return (
    <>
      <motion.div
        className="fixed top-0 left-0 w-3 h-3 bg-white rounded-full pointer-events-none z-[9999] mix-blend-difference"
        animate={{
          x: mousePosition.x - 6,
          y: mousePosition.y - 6,
        }}
        transition={{ type: 'tween', ease: 'backOut', duration: 0.1 }}
      />
      <motion.div
        className="fixed top-0 left-0 border border-secondary rounded-full pointer-events-none z-[9998]"
        animate={{
          x: mousePosition.x - 20,
          y: mousePosition.y - 20,
          width: isHovered ? 60 : 40,
          height: isHovered ? 60 : 40,
          x: isHovered ? mousePosition.x - 30 : mousePosition.x - 20,
          y: isHovered ? mousePosition.y - 30 : mousePosition.y - 20,
          backgroundColor: isHovered ? 'rgba(79, 142, 247, 0.2)' : 'transparent',
          borderColor: isHovered ? '#4f8ef7' : '#666680'
        }}
        transition={{ type: 'spring', stiffness: 150, damping: 15, mass: 0.5 }}
      />
    </>
  );
}
""",
        "frontend/components/ScrollProgressBar.tsx": """'use client';
import { motion, useScroll, useSpring } from 'framer-motion';

export default function ScrollProgressBar() {
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001
  });

  return (
    <motion.div
      className="fixed top-0 left-0 right-0 h-[2px] bg-accent z-[10000] origin-left"
      style={{ scaleX }}
    />
  );
}
""",
        "frontend/components/LoadingScreen.tsx": """'use client';
import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useState } from 'react';

export default function LoadingScreen() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setIsLoading(false), 800);
    return () => clearTimeout(timer);
  }, []);

  return (
    <AnimatePresence>
      {isLoading && (
        <motion.div
          initial={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5, ease: 'easeInOut' }}
          className="fixed inset-0 z-[10001] bg-background flex items-center justify-center"
        >
          <motion.h1 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.4 }}
            className="text-4xl font-syne font-bold text-white tracking-widest"
          >
            NEXCORE
          </motion.h1>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
""",
        "frontend/components/Navbar.tsx": """'use client';
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const links = [
  { name: 'Services', href: '#services' },
  { name: 'Work', href: '#work' },
  { name: 'Process', href: '#process' },
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [active, setActive] = useState('');

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 80);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`fixed top-0 w-full z-50 transition-all duration-300 ${scrolled ? 'py-4 backdrop-blur-md bg-background/70 border-b border-white/5' : 'py-8 bg-transparent'}`}>
      <div className="max-w-7xl mx-auto px-6 flex justify-between items-center">
        <div className="font-syne font-bold text-xl tracking-wider text-white">NEXCORE</div>
        
        <div className="hidden md:flex items-center gap-8">
          {links.map((link) => (
            <a 
              key={link.name} 
              href={link.href}
              onMouseEnter={() => setActive(link.name)}
              onMouseLeave={() => setActive('')}
              className="relative text-sm font-medium text-primary hover:text-white transition-colors"
            >
              {link.name}
              {active === link.name && (
                <motion.div
                  layoutId="underline"
                  className="absolute left-0 right-0 h-[1px] -bottom-1 bg-accent"
                />
              )}
            </a>
          ))}
          <a href="#contact" className="ml-4 px-6 py-2.5 rounded-full bg-white text-background font-medium text-sm hover:bg-accent hover:text-white transition-colors">
            Let's Talk
          </a>
        </div>
      </div>
    </nav>
  );
}
""",
        "frontend/components/Hero.tsx": """'use client';
import { motion } from 'framer-motion';
import { useEffect, useRef } from 'react';

export default function Hero() {
  const title = "We Craft Digital Experiences".split(" ");
  
  return (
    <section className="relative h-screen flex flex-col items-center justify-center overflow-hidden px-6 text-center">
      <div className="absolute inset-0 z-0">
        {/* Simple particle alternative: radial gradient */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(79,142,247,0.15),transparent_50%)]" />
      </div>
      
      <div className="relative z-10 max-w-5xl">
        <h1 className="font-syne text-5xl md:text-7xl lg:text-8xl font-extrabold leading-tight mb-6">
          {title.map((word, i) => (
            <motion.span
              key={i}
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.8 + i * 0.1, duration: 0.8, ease: [0.2, 0.65, 0.3, 0.9] }}
              className="inline-block mr-[0.25em]"
            >
              {word}
            </motion.span>
          ))}
        </h1>
        
        <motion.p 
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 1.4, duration: 0.8 }}
          className="text-lg md:text-xl text-secondary max-w-2xl mx-auto mb-10"
        >
          Elevating brands through state-of-the-art web development, immersive UI/UX, and robust AI integrations.
        </motion.p>
        
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 1.6, duration: 0.8 }}
        >
          <a href="#work" className="px-8 py-4 rounded-full bg-accent text-white font-medium hover:bg-white hover:text-background transition-colors inline-block">
            View Our Work
          </a>
        </motion.div>
      </div>

      <motion.div 
        animate={{ y: [0, 10, 0] }}
        transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
        className="absolute bottom-10 left-1/2 -translate-x-1/2"
      >
        <div className="w-[1px] h-16 bg-gradient-to-b from-white to-transparent" />
      </motion.div>
    </section>
  );
}
""",
        "frontend/components/Services.tsx": """'use client';
import { motion } from 'framer-motion';

const services = [
  { title: 'Web Development', desc: 'High-performance React & Next.js applications tailored for scale.' },
  { title: 'AI Integration', desc: 'Smart algorithms, LLM integrations, and intelligent automation.' },
  { title: 'UX Design', desc: 'User-centric interfaces blending aesthetics with seamless usability.' },
];

export default function Services() {
  return (
    <section id="services" className="py-32 px-6 max-w-7xl mx-auto">
      <div className="mb-20 text-center">
        <h2 className="text-sm font-medium text-accent tracking-widest uppercase mb-4">Our Expertise</h2>
        <h3 className="font-syne text-4xl md:text-5xl font-bold">What We Do</h3>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {services.map((svc, i) => (
          <motion.div
            key={svc.title}
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.6, delay: i * 0.2 }}
            whileHover={{ y: -10 }}
            className="group relative p-10 rounded-3xl bg-white/[0.02] border border-white/[0.05] hover:border-accent/50 transition-colors backdrop-blur-md overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-accent/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            <h4 className="font-syne text-2xl font-bold mb-4 relative z-10">{svc.title}</h4>
            <p className="text-secondary leading-relaxed relative z-10">{svc.desc}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
""",
        "frontend/components/Stats.tsx": """'use client';
import { motion } from 'framer-motion';
import { useEffect, useState, useRef } from 'react';

const stats = [
  { value: 120, suffix: '+', label: 'Projects Completed' },
  { value: 8, suffix: '', label: 'Years Experience' },
  { value: 40, suffix: '+', label: 'Global Clients' },
  { value: 99, suffix: '%', label: 'Client Satisfaction' },
];

function Counter({ from, to }: { from: number; to: number }) {
  const [count, setCount] = useState(from);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          let startTimestamp: number | null = null;
          const duration = 2000;
          const step = (timestamp: number) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            setCount(Math.floor(progress * (to - from) + from));
            if (progress < 1) {
              window.requestAnimationFrame(step);
            }
          };
          window.requestAnimationFrame(step);
          observer.disconnect();
        }
      },
      { threshold: 0.5 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [from, to]);

  return <span ref={ref}>{count}</span>;
}

export default function Stats() {
  return (
    <section className="py-24 border-y border-white/5 bg-white/[0.01]">
      <div className="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-12 text-center">
        {stats.map((stat, i) => (
          <div key={i}>
            <div className="font-syne text-5xl md:text-6xl font-bold text-white mb-2">
              <Counter from={0} to={stat.value} />{stat.suffix}
            </div>
            <div className="text-sm text-secondary uppercase tracking-wider">{stat.label}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
""",
        "frontend/components/Showcase.tsx": """'use client';
import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

export default function Showcase() {
  const textRef = useRef(null);
  
  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
    
    gsap.to(textRef.current, {
      xPercent: -50,
      ease: "none",
      scrollTrigger: {
        trigger: "#work",
        start: "top bottom",
        end: "bottom top",
        scrub: 1
      }
    });
  }, []);

  return (
    <section id="work" className="py-32 overflow-hidden bg-background">
      <div className="whitespace-nowrap mb-20">
        <h2 ref={textRef} className="font-syne text-[15vw] font-black uppercase text-transparent bg-clip-text" style={{ WebkitTextStroke: '1px rgba(255,255,255,0.1)' }}>
          Selected Works &mdash; Selected Works &mdash; Selected Works &mdash;
        </h2>
      </div>
      
      <div className="max-w-7xl mx-auto px-6 grid gap-12">
        {[1, 2, 3].map((i) => (
          <div key={i} className="group relative h-[60vh] md:h-[80vh] w-full rounded-3xl overflow-hidden bg-white/5">
            <div className="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-transparent z-10" />
            <div className="absolute bottom-10 left-10 z-20">
              <div className="text-teal text-sm font-medium mb-2 tracking-widest uppercase">E-Commerce</div>
              <h3 className="font-syne text-4xl text-white font-bold mb-4">Project Alpha {i}</h3>
              <button className="px-6 py-2 rounded-full border border-white/30 text-white hover:bg-white hover:text-black transition-colors">View Case Study</button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
""",
        "frontend/components/Process.tsx": """'use client';

export default function Process() {
  const steps = [
    { title: 'Discover', desc: 'Understanding your goals and setting the strategic foundation.' },
    { title: 'Design', desc: 'Crafting premium visuals and intuitive user experiences.' },
    { title: 'Develop', desc: 'Writing clean, scalable, and high-performance code.' },
    { title: 'Launch', desc: 'Rigorous testing and deploying to production.' }
  ];

  return (
    <section id="process" className="py-32 px-6 max-w-4xl mx-auto">
      <h2 className="font-syne text-4xl font-bold text-center mb-24">How We Work</h2>
      <div className="relative border-l border-white/10 pl-10 md:pl-20 ml-4 md:ml-10 space-y-20">
        {steps.map((step, i) => (
          <div key={i} className="relative">
            <div className="absolute -left-[45px] md:-left-[85px] top-1 w-4 h-4 rounded-full bg-accent" />
            <h3 className="font-syne text-2xl font-bold text-white mb-3">0{i+1}. {step.title}</h3>
            <p className="text-secondary leading-relaxed bg-white/5 p-6 rounded-2xl">{step.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
""",
        "frontend/components/Contact.tsx": """'use client';
import { useState } from 'react';
import { motion } from 'framer-motion';

export default function Contact() {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    
    try {
      const res = await fetch('http://localhost:8000/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (res.ok) setStatus('success');
      else setStatus('error');
    } catch {
      setStatus('error');
    }
  };

  return (
    <section id="contact" className="py-32 px-6 bg-white/[0.02] border-t border-white/5">
      <div className="max-w-3xl mx-auto text-center">
        <h2 className="font-syne text-4xl md:text-5xl font-bold mb-6">Let's Build Something Great</h2>
        <p className="text-secondary mb-16">Ready to elevate your digital presence? We'd love to hear from you.</p>
        
        <form onSubmit={handleSubmit} className="space-y-6 text-left">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="relative">
              <input 
                type="text" 
                required 
                className="w-full bg-transparent border-b border-white/20 py-4 text-white focus:outline-none focus:border-accent peer placeholder-transparent"
                placeholder="Name"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
              />
              <label className="absolute left-0 top-4 text-secondary text-sm transition-all peer-focus:-top-2 peer-focus:text-xs peer-focus:text-accent peer-valid:-top-2 peer-valid:text-xs border-transparent">Your Name</label>
            </div>
            <div className="relative">
              <input 
                type="email" 
                required 
                className="w-full bg-transparent border-b border-white/20 py-4 text-white focus:outline-none focus:border-accent peer placeholder-transparent"
                placeholder="Email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
              />
              <label className="absolute left-0 top-4 text-secondary text-sm transition-all peer-focus:-top-2 peer-focus:text-xs peer-focus:text-accent peer-valid:-top-2 peer-valid:text-xs">Your Email</label>
            </div>
          </div>
          <div className="relative">
            <textarea 
              required 
              rows={4}
              className="w-full bg-transparent border-b border-white/20 py-4 text-white focus:outline-none focus:border-accent peer placeholder-transparent resize-none"
              placeholder="Message"
              value={formData.message}
              onChange={(e) => setFormData({...formData, message: e.target.value})}
            />
            <label className="absolute left-0 top-4 text-secondary text-sm transition-all peer-focus:-top-2 peer-focus:text-xs peer-focus:text-accent peer-valid:-top-2 peer-valid:text-xs">Tell us about your project</label>
          </div>
          
          <button 
            type="submit" 
            disabled={status === 'loading' || status === 'success'}
            className="w-full py-4 rounded-xl bg-white text-background font-bold text-lg hover:bg-accent hover:text-white transition-colors disabled:opacity-50"
          >
            {status === 'idle' && 'Send Message'}
            {status === 'loading' && 'Sending...'}
            {status === 'success' && 'Message Received ✓'}
            {status === 'error' && 'Error. Try Again.'}
          </button>
        </form>
      </div>
    </section>
  );
}
""",
        "frontend/components/Footer.tsx": """export default function Footer() {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className="py-8 px-6 border-t border-white/5 bg-background text-sm flex flex-col md:flex-row justify-between items-center gap-4 text-secondary">
      <div>&copy; {new Date().getFullYear()} NexCore Studio. All rights reserved.</div>
      <div className="flex gap-6">
        <a href="#" className="hover:text-white transition-colors">Twitter</a>
        <a href="#" className="hover:text-white transition-colors">LinkedIn</a>
        <a href="#" className="hover:text-white transition-colors">Instagram</a>
      </div>
      <button onClick={scrollToTop} className="hover:text-white transition-colors">
        Back to Top ↑
      </button>
    </footer>
  );
}
""",
        "frontend/app/page.tsx": """import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import Services from '../components/Services';
import Stats from '../components/Stats';
import Showcase from '../components/Showcase';
import Process from '../components/Process';
import Contact from '../components/Contact';
import Footer from '../components/Footer';

export default function Home() {
  return (
    <main>
      <Navbar />
      <Hero />
      <Services />
      <Stats />
      <Showcase />
      <Process />
      <Contact />
      <Footer />
    </main>
  );
}
"""
    }

    for path, content in files.items():
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [wrote] {full}")

    print("[frontend] Generating files complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    create_files(args.root)
