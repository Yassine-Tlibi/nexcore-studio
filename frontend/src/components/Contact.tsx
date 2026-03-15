'use client';
import { useState } from 'react';
import { motion } from 'framer-motion';
import MagneticButton from './MagneticButton';

export default function Contact() {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/contact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        setStatus('success');
        setFormData({ name: '', email: '', message: '' });
      } else {
        setStatus('error');
      }
    } catch (err) {
      console.error('Contact submission error:', err);
      setStatus('error');
    }
  };

  return (
    <section id="contact" className="py-40 px-6 bg-[#08080f] relative">
      {/* 7. Subtle animated noise/grain overlay for this section */}
      <div className="absolute inset-0 bg-[#08080f] opacity-50 z-0" />
      
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-32 relative z-10">
        <div className="space-y-12">
          <motion.h2 
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            className="font-syne text-7xl md:text-9xl uppercase leading-[0.8]"
          >
            Let's <br/> <span className="text-accent underline decoration-2 underline-offset-8">Talk.</span>
          </motion.h2>
          <div className="space-y-6">
             <p className="text-secondary text-lg max-w-sm leading-relaxed uppercase tracking-widest font-bold">
               NOTRE ÉQUIPE EST À VOTRE ÉCOUTE POUR TRANSFORMER VOTRE VISION EN RÉALITÉ.
             </p>
             <a href="mailto:hello@nexcore.studio" className="inline-block text-3xl font-syne uppercase text-accent hover:tracking-widest transition-all duration-300">hello@nexcore.studio</a>
          </div>
        </div>
        
        <form onSubmit={handleSubmit} className="glass p-12 rounded-3xl space-y-12 border border-white/5">
          <div className="space-y-12">
            {[
              { id: 'name', label: 'Votre Nom', type: 'text' },
              { id: 'email', label: 'Votre Email', type: 'email' },
              { id: 'message', label: 'Votre Message', type: 'textarea' }
            ].map((field) => (
              <div key={field.id} className="relative group overflow-hidden">
                {field.type === 'textarea' ? (
                  <textarea 
                    required 
                    rows={1}
                    className="w-full bg-transparent border-b border-white/10 py-4 text-primary focus:outline-none focus:border-accent peer placeholder-transparent resize-none transition-all"
                    id={field.id}
                    value={(formData as any)[field.id]}
                    onChange={(e) => setFormData({...formData, [field.id]: e.target.value})}
                  />
                ) : (
                  <input 
                    type={field.type}
                    required 
                    className="w-full bg-transparent border-b border-white/10 py-4 text-primary focus:outline-none focus:border-accent peer placeholder-transparent transition-all"
                    id={field.id}
                    value={(formData as any)[field.id]}
                    onChange={(e) => setFormData({...formData, [field.id]: e.target.value})}
                  />
                )}
                <label htmlFor={field.id} className="absolute left-0 top-4 text-secondary uppercase tracking-[0.2em] text-xs transition-all peer-focus:-top-4 peer-focus:text-accent peer-valid:-top-4">
                  {field.label}
                </label>
                <motion.div className="absolute bottom-0 left-0 w-0 h-[1px] bg-accent" whileHover={{ width: '100%' }} />
              </div>
            ))}
          </div>
          
          <div className="pt-8">
            <MagneticButton>
              <button 
                type="submit" 
                disabled={status === 'loading' || status === 'success'}
                className="group w-full bg-accent text-background py-8 rounded-2xl font-bold uppercase tracking-widest transition-all hover:shadow-[0_0_50px_rgba(79,142,247,0.3)] disabled:opacity-50"
              >
                {status === 'idle' && 'Envoyer le message'}
                {status === 'loading' && 'Traitement...'}
                {status === 'success' && 'Envoyé ✓'}
                {status === 'error' && 'Réessayer'}
              </button>
            </MagneticButton>
          </div>
        </form>
      </div>
    </section>
  );
}
