'use client';
import React, { useState } from 'react';
import { AuthCard } from '@/components/auth/AuthCard';
import { supabase } from '@/lib/supabase';
import { motion } from 'framer-motion';
import { Check } from 'lucide-react';

export default function ResetPasswordPage() {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/auth/callback`,
    });
    setLoading(false);
    if (error) alert(error.message);
    else setSent(true);
  };

  return (
    <div className="min-h-screen bg-[#050505] flex items-center justify-center p-6 relative overflow-hidden">
      <div className="absolute inset-0 grainy-bg opacity-30 pointer-events-none" />
      <AuthCard>
        {!sent ? (
          <>
            <h2 className="text-2xl font-bold mb-8 tracking-tighter">Reset Password</h2>
            <form onSubmit={handleReset} className="space-y-12">
              <div className="relative">
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder=" "
                  className="w-full bg-transparent border-b border-white/20 py-3 outline-none transition-all focus:border-accent peer"
                />
                <label className="absolute left-0 top-3 text-white/40 pointer-events-none transition-all duration-300 peer-focus:-top-4 peer-focus:text-xs peer-focus:text-accent peer-[:not(:placeholder-shown)]:-top-4 peer-[:not(:placeholder-shown)]:text-xs">
                  Email address
                </label>
              </div>
              <button
                disabled={loading}
                className="w-full py-4 bg-accent text-white rounded-2xl font-bold uppercase tracking-widest text-xs disabled:opacity-50"
              >
                {loading ? 'Sending...' : 'Send Reset Link'}
              </button>
            </form>
          </>
        ) : (
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="text-center py-8"
          >
            <div className="w-16 h-16 bg-accent/20 rounded-full flex items-center justify-center mx-auto mb-6">
              <Check className="text-accent" size={32} />
            </div>
            <h3 className="text-xl font-bold mb-2">Check your inbox</h3>
            <p className="text-white/40 text-sm italic">We've sent a password reset link to {email}.</p>
          </motion.div>
        )}
      </AuthCard>
    </div>
  );
}
