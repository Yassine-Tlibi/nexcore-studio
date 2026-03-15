'use client';
import { motion } from 'framer-motion';

export default function Footer() {
  return (
    <footer className="bg-[#08080f] pt-40 pb-12 px-6 overflow-hidden relative border-t border-white/5">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-16 mb-40">
        <div className="lg:col-span-2 space-y-8">
          <motion.div 
            whileHover={{ scale: 1.05, originX: 0 }}
            className="text-5xl font-syne font-bold tracking-tighter cursor-pointer"
          >
            NEXCORE.
          </motion.div>
          <p className="text-secondary text-lg max-w-sm leading-relaxed">
            Studio d'innovation digitale spécialisé dans la création d'expériences mémorables et ultra-performantes.
          </p>
        </div>

        <div className="space-y-8">
          <h4 className="text-accent font-bold uppercase tracking-widest text-xs">Navigation</h4>
          <nav className="flex flex-col space-y-4 font-syne uppercase">
            {['Services', 'Methodology', 'Showcase', 'Contact'].map((item) => (
               <a key={item} href={`#${item.toLowerCase()}`} className="hover:text-accent transition-colors opacity-60 hover:opacity-100">{item}</a>
            ))}
          </nav>
        </div>

        <div className="space-y-8">
          <h4 className="text-accent font-bold uppercase tracking-widest text-xs">Social</h4>
          <div className="flex flex-col space-y-4">
            {['LinkedIn', 'Instagram', 'Twitter'].map((social) => (
              <motion.a 
                key={social}
                href="#"
                whileHover={{ x: 10, rotate: 5 }}
                className="font-syne uppercase opacity-60 hover:opacity-100 flex items-center space-x-2"
              >
                <span>{social}</span>
              </motion.a>
            ))}
          </div>
        </div>
      </div>
      
      <div className="max-w-7xl mx-auto pt-12 flex flex-col md:flex-row justify-between items-center text-[10px] text-secondary/40 uppercase tracking-[0.3em] border-t border-white/5">
        <div>&copy; {new Date().getFullYear()} NEXCORE STUDIO — DESIGNED TO WIN</div>
        <motion.button 
          whileHover={{ y: -5 }}
          onClick={() => window.scrollTo({top: 0, behavior: 'smooth'})} 
          className="hover:text-accent mt-6 md:mt-0"
        >
          BACK TO TOP ↑
        </motion.button>
      </div>

      {/* 4. Large background glow */}
      <div className="absolute -bottom-[20%] -left-[10%] w-[600px] h-[600px] bg-accent/5 blur-[150px] rounded-full pointer-events-none" />
    </footer>
  );
}
