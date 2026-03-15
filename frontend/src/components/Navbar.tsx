'use client';
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X } from 'lucide-react';

/**
 * Navbar Component
 * Features glassmorphism and animated text tracking.
 */
export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`fixed top-0 w-full z-50 transition-all duration-700 ${scrolled ? 'py-4 glass border-b border-white/5' : 'py-8 bg-transparent'}`}>
      <div className="max-w-7xl mx-auto px-6 flex justify-between items-center text-primary">
        <motion.div 
          whileHover={{ letterSpacing: '0.2em' }}
          transition={{ duration: 0.3 }}
          className="text-2xl font-syne font-bold cursor-pointer"
        >
          NEXCORE.
        </motion.div>
        
        <button 
          onClick={() => setIsOpen(!isOpen)}
          aria-label={isOpen ? "Fermer le menu" : "Ouvrir le menu"}
          className="p-3 bg-white/5 hover:bg-white/10 rounded-full transition-colors relative z-[70]"
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 1.1 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.6, ease: [0.76, 0, 0.24, 1] }}
            className="fixed inset-0 bg-background z-[60] flex flex-col items-center justify-center space-y-8 font-syne"
          >
            {['Services', 'Methodology', 'Contact'].map((item, i) => (
              <motion.a
                key={item}
                href={`#${item.toLowerCase()}`}
                onClick={() => setIsOpen(false)}
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2 + i * 0.1, duration: 0.8 }}
                className="text-5xl md:text-7xl uppercase hover:text-accent transition-colors relative"
              >
                {item}
                <motion.div 
                   className="absolute -bottom-2 left-0 w-0 h-1 bg-accent"
                   whileHover={{ width: '100%' }}
                />
              </motion.a>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
