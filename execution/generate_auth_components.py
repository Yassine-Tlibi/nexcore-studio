import os

def generate_auth_components():
    base_dir = "frontend/src/components/auth"
    os.makedirs(base_dir, exist_ok=True)
    
    components = {
        "AuthCard.tsx": """'use client';
import { motion } from 'framer-motion';
import React from 'react';

export const AuthCard = ({ children }: { children: React.ReactNode }) => {
  return (
    <motion.div 
      initial={{ y: 40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
      className="p-8 rounded-3xl border border-white/10 bg-white/5 backdrop-blur-2xl shadow-2xl relative group w-full max-w-md"
    >
      <div className="absolute -inset-[1px] bg-gradient-to-r from-accent/30 to-transparent rounded-[24px] opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none" />
      {children}
    </motion.div>
  );
};
""",
        "GoogleButton.tsx": """'use client';
import React from 'react';
import { supabase } from '@/lib/supabase';
import MagneticButton from '../MagneticButton';

export const GoogleButton = () => {
  const handleGoogleLogin = async () => {
    const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || window.location.origin;
    await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${siteUrl}/auth/callback`,
      },
    });
  };

  return (
    <MagneticButton onClick={handleGoogleLogin}>
      <div className="w-full flex items-center justify-center gap-3 px-6 py-4 bg-white/10 hover:bg-white/15 border border-white/10 text-white rounded-2xl font-medium transition-all group">
        <svg className="w-5 h-5 group-hover:scale-110 transition-transform" viewBox="0 0 24 24">
          <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/>
          <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
        </svg>
        Continue with Google
      </div>
    </MagneticButton>
  );
};
""",
        "FormInput.tsx": """'use client';
import { motion, AnimatePresence } from 'framer-motion';
import React, { useState } from 'react';
import { UseFormRegisterReturn } from 'react-hook-form';
import { Eye, EyeOff } from 'lucide-react';

interface FormInputProps {
  label: string;
  type?: string;
  error?: string;
  registration: UseFormRegisterReturn;
}

export const FormInput = ({ label, type = 'text', error, registration }: FormInputProps) => {
  const [show, setShow] = useState(false);
  const isPassword = type === 'password';
  const inputType = isPassword ? (show ? 'text' : 'password') : type;

  return (
    <div className="mb-8 relative group">
      <input
        {...registration}
        type={inputType}
        placeholder=" "
        className={`w-full bg-transparent border-b border-white/20 py-3 outline-none transition-all peer focus:border-accent ${
          error ? 'border-red-500' : ''
        }`}
      />
      <label className="absolute left-0 top-3 text-white/40 pointer-events-none transition-all duration-300 peer-focus:-top-4 peer-focus:text-xs peer-focus:text-accent peer-[:not(:placeholder-shown)]:-top-4 peer-[:not(:placeholder-shown)]:text-xs">
        {label}
      </label>
      
      {isPassword && (
        <button 
          type="button"
          onClick={() => setShow(!show)}
          className="absolute right-0 top-3 text-white/20 hover:text-white transition-colors"
        >
          {show ? <EyeOff size={18} /> : <Eye size={18} />}
        </button>
      )}

      <AnimatePresence>
        {error && (
          <motion.p
            initial={{ y: -5, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ opacity: 0 }}
            className="text-red-500 text-[10px] mt-1 absolute uppercase tracking-widest font-bold"
          >
            {error}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
};
""",
        "TabSwitcher.tsx": """'use client';
import { motion } from 'framer-motion';
import React from 'react';

export const TabSwitcher = ({ active, onChange }: { active: 'login' | 'signup', onChange: (t: 'login' | 'signup') => void }) => {
  return (
    <div className="flex gap-8 mb-10 border-b border-white/5 relative">
      <button 
        onClick={() => onChange('login')}
        className={`pb-4 text-sm uppercase tracking-widest transition-colors ${active === 'login' ? 'text-white' : 'text-white/40 hover:text-white/60'}`}
      >
        Sign In
      </button>
      <button 
        onClick={() => onChange('signup')}
        className={`pb-4 text-sm uppercase tracking-widest transition-colors ${active === 'signup' ? 'text-white' : 'text-white/40 hover:text-white/60'}`}
      >
        Sign Up
      </button>
      <motion.div 
        layoutId="tab-underline"
        className="absolute bottom-0 h-[2px] bg-accent"
        initial={false}
        animate={{ 
          left: active === 'login' ? 0 : '88px',
          width: active === 'login' ? '54px' : '62px'
        }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      />
    </div>
  );
};
""",
        "PasswordStrength.tsx": """'use client';
import React from 'react';

export const PasswordStrength = ({ password }: { password: string }) => {
  const getStrength = (pass: string) => {
    let score = 0;
    if (!pass) return 0;
    if (pass.length >= 8) score++;
    if (/[A-Z]/.test(pass)) score++;
    if (/[0-9]/.test(pass)) score++;
    if (/[^a-zA-Z0-9]/.test(pass)) score++;
    return score;
  };

  const strength = getStrength(password);
  const labels = ['Empty', 'Weak', 'Fair', 'Good', 'Strong'];
  const colors = ['bg-white/10', 'bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-green-500'];

  return (
    <div className="mt-2 mb-8">
      <div className="flex justify-between items-center mb-2">
        <span className="text-[10px] uppercase tracking-widest text-white/40">Security</span>
        <span className={`text-[10px] uppercase tracking-widest ${strength > 0 ? 'text-white' : 'text-white/40'}`}>
          {labels[strength]}
        </span>
      </div>
      <div className="flex gap-1 h-1 w-full">
        {[1, 2, 3, 4].map((step) => (
          <div 
            key={step}
            className={`h-full flex-1 rounded-full transition-all duration-700 ${
              step <= strength ? colors[strength] : 'bg-white/10'
            }`}
          />
        ))}
      </div>
    </div>
  );
};
"""
    }

    for path, content in components.items():
        with open(os.path.join(base_dir, path), "w", encoding='utf-8') as f:
            f.write(content)
        print(f"Generated: {path}")

if __name__ == "__main__":
    generate_auth_components()
