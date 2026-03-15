import os
import argparse

GLOBALS_CSS = """@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: #F2EDE4;
  --foreground: #1A1A1A;
  --accent: #D92323;
}

body {
  color: var(--foreground);
  background: var(--background);
  font-family: 'Inter', sans-serif;
  overflow-x: hidden;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Playfair Display', serif;
  font-weight: 700;
}

i, .serif-italic {
  font-family: 'Playfair Display', serif;
  font-style: italic;
}

/* Texture overlay */
body::before {
  content: "";
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.03;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}

::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: var(--background);
}
::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 10px;
}
"""

TAILWIND_CONFIG = """import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#F2EDE4",
        primary: "#1A1A1A",
        secondary: "#4A4A4A",
        accent: "#D92323",
      },
      fontFamily: {
        serif: ["'Playfair Display'", "serif"],
        sans: ["'Inter'", "sans-serif"],
      },
      borderRadius: {
        'blob': '40% 60% 70% 30% / 40% 50% 60% 50%',
      }
    },
  },
  plugins: [],
};
export default config;
"""

NAVBAR_TSX = """'use client';
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X } from 'lucide-react';

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`fixed top-0 w-full z-50 transition-all duration-500 ${scrolled ? 'py-4 bg-background/80 backdrop-blur-md' : 'py-8 bg-transparent'}`}>
      <div className="max-w-7xl mx-auto px-6 flex justify-between items-center text-primary font-sans">
        <div className="text-2xl font-bold tracking-tighter">NEXCORE.</div>
        
        <button 
          onClick={() => setIsOpen(!isOpen)}
          className="p-2 hover:bg-black/5 rounded-full transition-colors"
        >
          {isOpen ? <X size={28} /> : <Menu size={28} />}
        </button>
      </div>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="fixed inset-0 bg-primary z-[60] flex flex-col items-center justify-center space-y-8 text-background font-serif"
          >
            <button 
              onClick={() => setIsOpen(false)}
              className="absolute top-8 right-8 text-background hover:rotate-90 transition-transform duration-300"
            >
              <X size={40} />
            </button>
            <a href="#services" onClick={() => setIsOpen(false)} className="text-6xl italic hover:text-accent transition-colors">Services</a>
            <a href="#method" onClick={() => setIsOpen(false)} className="text-6xl italic hover:text-accent transition-colors">Methodology</a>
            <a href="#contact" onClick={() => setIsOpen(false)} className="text-6xl italic hover:text-accent transition-colors">Contact</a>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
"""

HERO_TSX = """'use client';
import { motion } from 'framer-motion';

export default function Hero() {
  return (
    <section className="relative h-screen flex items-center justify-center bg-background px-6 pt-20">
      <div className="relative z-10 max-w-5xl text-center">
        <motion.h1 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="font-serif text-6xl md:text-8xl lg:text-9xl leading-[0.9] text-primary"
        >
          L'agence de <br />
          <span className="italic text-accent">stratégie</span> digitale.
        </motion.h1>
        
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 1 }}
          className="mt-12 text-lg md:text-xl font-sans text-secondary max-w-xl mx-auto uppercase tracking-widest font-medium"
        >
          Nous créons des expériences numériques qui marquent les esprits et transforment votre business.
        </motion.p>
      </div>

      {/* Red Abstract Mask Shape */}
      <motion.div 
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 0.1, scale: 1 }}
        transition={{ duration: 1.5, ease: "easeOut" }}
        className="absolute right-[5%] top-[20%] w-[500px] h-[500px] bg-accent rounded-blob rotate-12 blur-[100px] pointer-events-none"
      />
    </section>
  );
}
"""

MARQUEE_TSX = """'use client';
import { motion } from 'framer-motion';

const items = ["STRATÉGIE", "DESIGN", "DÉVELOPPEMENT", "MARKETING", "AI SOLUTIONS"];

export default function Marquee() {
  return (
    <div className="overflow-hidden whitespace-nowrap bg-primary py-6 flex">
      <motion.div 
        animate={{ x: [0, -1000] }}
        transition={{ repeat: Infinity, duration: 20, ease: "linear" }}
        className="flex space-x-12 items-center pr-12"
      >
        {[...items, ...items, ...items].map((item, i) => (
          <div key={i} className="flex items-center space-x-12">
            <span className="text-secondary text-2xl font-bold tracking-[0.2em]">{item}</span>
            <div className="w-2 h-2 rounded-full bg-accent" />
          </div>
        ))}
      </motion.div>
    </div>
  );
}
"""

SERVICES_TSX = """'use client';
import { motion } from 'framer-motion';

const services = [
  { id: '01', title: 'Consulting & Stratégie', desc: 'Audit, vision stratégique et accompagnement vers la transformation digitale.', img: '/api/placeholder/400/300' },
  { id: '02', title: 'Design & Expérience', desc: 'UI/UX centré sur l user, identité visuelle et branding premium.', img: '/api/placeholder/400/300' },
  { id: '03', title: 'Développement Web', desc: 'Architectures robustes, Next.js, performance et éco-conception.', img: '/api/placeholder/400/300' },
];

export default function Services() {
  return (
    <section id="services" className="py-32 px-6 bg-background">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-end mb-24 border-b border-primary/10 pb-12">
          <h2 className="font-serif text-6xl md:text-8xl italic">Nos Expertises</h2>
          <p className="max-w-xs text-sm uppercase tracking-widest text-secondary mt-6 md:mt-0">
            Une approche globale pour des résultats tangibles.
          </p>
        </div>

        <div className="space-y-32">
          {services.map((svc, i) => (
            <div key={svc.id} className="flex flex-col md:flex-row gap-12 items-center group">
              <div className="relative w-full md:w-1/2 overflow-hidden rounded-blob bg-black/5 aspect-square max-w-md mx-auto md:mx-0">
                <div className="absolute inset-0 bg-accent/20 group-hover:bg-accent/40 transition-colors duration-500 z-10" />
                <img src={svc.img} alt={svc.title} className="w-full h-full object-cover grayscale brightness-90 group-hover:scale-110 transition-transform duration-700" />
              </div>
              <div className="w-full md:w-1/2 space-y-6">
                <span className="font-serif text-accent text-3xl italic">{svc.id}.</span>
                <h3 className="font-serif text-5xl md:text-6xl font-bold">{svc.title}</h3>
                <p className="text-secondary text-lg max-w-lg leading-relaxed">{svc.desc}</p>
                <div className="pt-4">
                  <button className="text-primary font-bold tracking-widest uppercase text-sm border-b-2 border-accent pb-1 hover:text-accent transition-colors">Découvrir</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
"""

METHODOLOGY_TSX = """'use client';
import { motion } from 'framer-motion';

const steps = [
  { id: '01', title: 'IMMERSION', desc: 'Comprendre votre métier, vos enjeux et vos clients.' },
  { id: '02', title: 'CONCEPTION', desc: 'Designer les solutions et valider les prototypes.' },
  { id: '03', title: 'PRODUCTION', desc: 'Développer avec les meilleures technologies.' },
];

export default function Methodology() {
  return (
    <section id="method" className="bg-accent py-32 px-6 text-background">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-20">
        <div className="space-y-8">
          <h2 className="font-serif text-6xl md:text-8xl italic">Méthode.</h2>
          <p className="text-xl max-w-sm opacity-80 uppercase tracking-widest">
            Un processus rigoureux pour une exécution parfaite.
          </p>
        </div>
        <div className="divide-y divide-background/20">
          {steps.map((step) => (
            <div key={step.id} className="py-12 group cursor-pointer">
              <div className="flex justify-between items-center mb-4">
                <span className="font-serif text-2xl italic">{step.id}</span>
                <h3 className="font-serif text-4xl font-bold group-hover:italic transition-all uppercase">{step.title}</h3>
              </div>
              <p className="max-w-md opacity-0 h-0 group-hover:opacity-100 group-hover:h-auto transition-all duration-500 overflow-hidden text-lg">
                {step.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
"""

FOOTER_TSX = """'use client';

export default function Footer() {
  return (
    <footer className="bg-primary pt-32 pb-12 px-6 text-background overflow-hidden relative">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between gap-12 border-b border-background/10 pb-20">
        <div className="space-y-6 max-w-sm">
          <div className="text-4xl font-bold tracking-tighter">NEXCORE.</div>
          <p className="opacity-60 text-lg">Design & Tech Studio basé à Tahiti. Nous transformons vos idées en produits digitaux d'exception.</p>
        </div>
        <div className="grid grid-cols-2 gap-16 md:gap-32">
          <div className="space-y-4">
            <p className="uppercase tracking-widest text-xs font-bold text-accent">Studio</p>
            <nav className="flex flex-col space-y-2 opacity-60">
              <a href="#" className="hover:text-accent">Services</a>
              <a href="#" className="hover:text-accent">Projets</a>
              <a href="#" className="hover:text-accent">Contact</a>
            </nav>
          </div>
          <div className="space-y-4">
            <p className="uppercase tracking-widest text-xs font-bold text-accent">Social</p>
            <nav className="flex flex-col space-y-2 opacity-60">
              <a href="#" className="hover:text-accent">LinkedIn</a>
              <a href="#" className="hover:text-accent">Instagram</a>
              <a href="#" className="hover:text-accent">Dribbble</a>
            </nav>
          </div>
        </div>
      </div>
      
      <div className="max-w-7xl mx-auto pt-12 flex justify-between items-center text-xs opacity-40 uppercase tracking-widest">
        <div>&copy; {new Date().getFullYear()} NEXCORE STUDIO</div>
        <button onClick={() => window.scrollTo({top: 0, behavior: 'smooth'})} className="hover:text-accent">Back to Top ↑</button>
      </div>

      {/* Decorative large serif background text */}
      <div className="absolute -bottom-20 -right-20 pointer-events-none opacity-[0.02] select-none">
        <span className="font-serif text-[40vw] italic font-black">N.</span>
      </div>
    </footer>
  );
}
"""

PAGE_TSX = """import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import Marquee from '../components/Marquee';
import Services from '../components/Services';
import Methodology from '../components/Methodology';
import Contact from '../components/Contact';
import Footer from '../components/Footer';

export default function Home() {
  return (
    <main className="bg-background">
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

def redesign(root: str):
    files = {
        "frontend/app/globals.css": GLOBALS_CSS,
        "frontend/tailwind.config.ts": TAILWIND_CONFIG,
        "frontend/app/page.tsx": PAGE_TSX,
        "frontend/components/Navbar.tsx": NAVBAR_TSX,
        "frontend/components/Hero.tsx": HERO_TSX,
        "frontend/components/Marquee.tsx": MARQUEE_TSX,
        "frontend/components/Services.tsx": SERVICES_TSX,
        "frontend/components/Methodology.tsx": METHODOLOGY_TSX,
        "frontend/components/Footer.tsx": FOOTER_TSX,
    }

    for path, content in files.items():
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [redesign] {full}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    redesign(args.root)
    print("[redesign] All files updated successfully.")
