'use client';
import { motion } from 'framer-motion';

const steps = [
  { id: '01', title: 'IMMERSION', desc: 'Comprendre votre métier, vos enjeux et vos clients.' },
  { id: '02', title: 'CONCEPTION', desc: 'Designer les solutions et valider les prototypes.' },
  { id: '03', title: 'PRODUCTION', desc: 'Développer avec les meilleures technologies.' },
];

export default function Methodology() {
  return (
    <section id="method" className="relative bg-accent py-40 px-6 text-background overflow-hidden">
      {/* 18. Mesh Gradient Background Animation */}
      <motion.div 
        animate={{ 
          x: [0, 100, 0],
          y: [0, -50, 0],
          scale: [1, 1.2, 1]
        }}
        transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-0 right-0 w-[800px] h-[800px] bg-white/5 blur-[150px] -z-10 rounded-full"
      />

      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-24">
        <div className="space-y-12">
          <motion.h2 
            initial={{ clipPath: 'inset(100% 0 0 0)' }}
            whileInView={{ clipPath: 'inset(0% 0 0 0)' }}
            transition={{ duration: 1, ease: 'circOut' }}
            className="font-syne text-7xl md:text-9xl uppercase leading-[0.8]"
          >
            Notre <br/><span className="italic">Méthode.</span>
          </motion.h2>
          <p className="text-xl max-w-sm opacity-80 uppercase tracking-widest font-bold">
            Un processus rigoureux pour une exécution digitale parfaite.
          </p>
        </div>

        <div className="space-y-4">
          {steps.map((step, i) => (
            <motion.div 
              key={step.id} 
              initial={{ x: 100, opacity: 0 }}
              whileInView={{ x: 0, opacity: 1 }}
              transition={{ delay: i * 0.2, duration: 0.8 }}
              className="py-12 group cursor-pointer relative"
            >
              {/* Typewriter effect for ID */}
              <div className="flex justify-between items-center mb-4">
                <motion.span 
                  initial={{ width: 0 }}
                  whileInView={{ width: 'auto' }}
                  transition={{ duration: 0.5, delay: i * 0.3 }}
                  className="font-mono text-xl overflow-hidden whitespace-nowrap inline-block"
                >
                  {step.id}
                </motion.span>
                <h3 className="font-syne text-4xl md:text-5xl uppercase transition-all duration-500 group-hover:pl-8">{step.title}</h3>
                <div className="w-12 h-12 bg-background/10 rounded-full flex items-center justify-center group-hover:bg-background group-hover:text-accent transition-all">
                  <span className="group-hover:rotate-45 transition-transform duration-300">→</span>
                </div>
              </div>
              
              {/* Animated Horizontal Rule */}
              <motion.div 
                initial={{ scaleX: 0 }}
                whileInView={{ scaleX: 1 }}
                transition={{ duration: 1, ease: 'easeOut' }}
                style={{ originX: 0 }}
                className="absolute bottom-0 left-0 w-full h-[1px] bg-background/20"
              />
              <p className="mt-6 max-w-md opacity-0 text-lg translate-y-4 group-hover:opacity-80 group-hover:translate-y-0 transition-all duration-500">
                {step.desc}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
