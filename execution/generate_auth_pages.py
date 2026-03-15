import os

def generate_auth_pages():
    base_dir = "frontend/src"
    
    # 1. Validations
    os.makedirs(os.path.join(base_dir, "lib/validations"), exist_ok=True)
    with open(os.path.join(base_dir, "lib/validations/auth.schema.ts"), "w") as f:
        f.write("""import { z } from 'zod';

export const signInSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(1, 'Password is required'),
});

export const signUpSchema = z.object({
  fullName: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email format'),
  password: z
    .string()
    .min(8, 'Min 8 characters')
    .regex(/[A-Z]/, 'One uppercase required')
    .regex(/[0-9]/, 'One number required')
    .regex(/[^a-zA-Z0-9]/, 'One special char required'),
});

export type SignInInput = z.infer<typeof signInSchema>;
export type SignUpInput = z.infer<typeof signUpSchema>;
""")

    # 2. Auth Lib
    with open(os.path.join(base_dir, "lib/auth.ts"), "w") as f:
        f.write("""import { supabase } from './supabase';

export const signUpWithEmail = async (email: string, password: string, fullName: string) => {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: { full_name: fullName },
    }
  });
  if (error) throw error;

  // Add to waitlist
  if (data.user) {
    const { data: waitlist, error: waitlistError } = await supabase
      .from('waitlist')
      .insert({
        user_id: data.user.id,
        email: email,
        full_name: fullName,
      })
      .select()
      .single();
    
    if (waitlistError) throw waitlistError;
    return waitlist;
  }
};

export const signInWithEmail = async (email: string, password: string) => {
  const { error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) throw error;
};

export const getCurrentUser = async () => {
  const { data: { user } } = await supabase.auth.getUser();
  return user;
};

export const signOut = async () => {
  return await supabase.auth.signOut();
};
""")

    # 3. Pages
    pages = {
        "app/waitlist/page.tsx": """'use client';
import React, { useEffect, useState } from 'react';
import { motion, useSpring, useTransform } from 'framer-motion';
import MagneticButton from '@/components/MagneticButton';
import { useRouter } from 'next/navigation';
import { supabase } from '@/lib/supabase';

export default function WaitlistPage() {
  const [count, setCount] = useState(0);
  const router = useRouter();
  const springCount = useSpring(0, { stiffness: 40, damping: 20 });
  const displayCount = useTransform(springCount, (latest) => Math.floor(latest));

  useEffect(() => {
    const fetchCount = async () => {
      const { count: total } = await supabase
        .from('waitlist')
        .select('*', { count: 'exact', head: true });
      setCount(total || 0);
    };
    fetchCount();
  }, []);

  useEffect(() => {
    springCount.set(count);
  }, [count, springCount]);

  return (
    <div className="min-h-screen bg-[#050505] text-white flex flex-col items-center justify-center p-6 relative overflow-hidden">
      <div className="absolute inset-0 grainy-bg opacity-30 pointer-events-none" />
      
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
        className="text-center z-10"
      >
        <h1 className="text-7xl md:text-9xl font-bold tracking-tighter mb-8 italic">
          Be the first<br/>to know.
        </h1>
        <p className="text-xl text-white/40 mb-12 max-w-xl mx-auto uppercase tracking-widest font-light">
          Join the waitlist and get early access to NexCore Studio.
        </p>
        
        <div className="flex flex-col items-center gap-12">
          <MagneticButton onClick={() => router.push('/auth/login')}>
            <span className="px-12 py-5 bg-accent text-white rounded-full font-bold text-lg hover:scale-105 transition-transform block">
              Get Early Access
            </span>
          </MagneticButton>

          <div className="flex flex-col items-center">
            <motion.span className="text-6xl font-bold italic text-accent line-height-none mb-2">
              {displayCount}
            </motion.span>
            <span className="text-[10px] uppercase tracking-[0.3em] font-bold text-white/20">Users in queue</span>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
""",
        "app/auth/login/page.tsx": """'use client';
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { signInSchema, signUpSchema, SignInInput, SignUpInput } from '@/lib/validations/auth.schema';
import { AuthCard } from '@/components/auth/AuthCard';
import { FormInput } from '@/components/auth/FormInput';
import { GoogleButton } from '@/components/auth/GoogleButton';
import { TabSwitcher } from '@/components/auth/TabSwitcher';
import { PasswordStrength } from '@/components/auth/PasswordStrength';
import { signInWithEmail, signUpWithEmail } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import { AnimatePresence, motion } from 'framer-motion';
import MagneticButton from '@/components/MagneticButton';

export default function LoginPage() {
  const [tab, setTab] = useState<'login' | 'signup'>('login');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const { register: regLogin, handleSubmit: handleLogin, formState: { errors: logErrors } } = useForm<SignInInput>({
    resolver: zodResolver(signInSchema),
  });

  const { register: regSign, handleSubmit: handleSign, watch, formState: { errors: signErrors } } = useForm<SignUpInput>({
    resolver: zodResolver(signUpSchema),
  });

  const password = watch('password', '');

  const onLogin = async (data: SignInInput) => {
    setLoading(true);
    try {
      await signInWithEmail(data.email, data.password);
      router.push('/waitlist/success');
    } catch (e: any) {
      alert(e.message);
    } finally {
      setLoading(false);
    }
  };

  const onSignup = async (data: SignUpInput) => {
    setLoading(true);
    try {
      await signUpWithEmail(data.email, data.password, data.fullName);
      router.push('/waitlist/success');
    } catch (e: any) {
      alert(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#050505] flex items-center justify-center p-6 relative overflow-hidden">
      <div className="absolute inset-0 grainy-bg opacity-30 pointer-events-none" />
      
      <AuthCard>
        <TabSwitcher active={tab} onChange={setTab} />
        
        <AnimatePresence mode="wait">
          {tab === 'login' ? (
            <motion.form
              key="login"
              initial={{ x: -20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 20, opacity: 0 }}
              onSubmit={handleLogin(onLogin)}
              className="space-y-4"
            >
              <FormInput label="Email" registration={regLogin('email')} error={logErrors.email?.message} />
              <FormInput label="Password" type="password" registration={regLogin('password')} error={logErrors.password?.message} />
              
              <div className="mt-8">
                <MagneticButton>
                  <button disabled={loading} className="w-full py-4 bg-accent text-white rounded-2xl font-bold uppercase tracking-widest text-xs disabled:opacity-50">
                    {loading ? 'Processing...' : 'Sign In'}
                  </button>
                </MagneticButton>
              </div>
            </motion.form>
          ) : (
            <motion.form
              key="signup"
              initial={{ x: 20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: -20, opacity: 0 }}
              onSubmit={handleSign(onSignup)}
              className="space-y-4"
            >
              <FormInput label="Full Name" registration={regSign('fullName')} error={signErrors.fullName?.message} />
              <FormInput label="Email" registration={regSign('email')} error={signErrors.email?.message} />
              <FormInput label="Password" type="password" registration={regSign('password')} error={signErrors.password?.message} />
              <PasswordStrength password={password} />
              
              <div className="mt-8">
                <MagneticButton>
                  <button disabled={loading} className="w-full py-4 bg-accent text-white rounded-2xl font-bold uppercase tracking-widest text-xs disabled:opacity-50">
                    {loading ? 'Processing...' : 'Create Account'}
                  </button>
                </MagneticButton>
              </div>
            </motion.form>
          )}
        </AnimatePresence>

        <div className="mt-10 pt-10 border-t border-white/5">
          <p className="text-center text-[10px] uppercase tracking-[0.2em] text-white/20 mb-6">Or continue with</p>
          <GoogleButton />
        </div>
      </AuthCard>
    </div>
  );
}
""",
        "app/waitlist/success/page.tsx": """'use client';
import React, { useEffect, useState } from 'react';
import { motion, useSpring, useTransform } from 'framer-motion';
import confetti from 'canvas-confetti';
import Link from 'next/link';
import { supabase } from '@/lib/supabase';
import { ArrowLeft } from 'lucide-react';

export default function SuccessPage() {
  const [position, setPosition] = useState(0);
  const springPos = useSpring(0, { stiffness: 40, damping: 20 });
  const displayPos = useTransform(springPos, (latest) => Math.floor(latest));

  useEffect(() => {
    confetti({
      particleCount: 150,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#000000', '#ffffff', '#6366f1']
    });

    const fetchPosition = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      if (user) {
        const { data } = await supabase
          .from('waitlist')
          .select('position')
          .eq('user_id', user.id)
          .single();
        if (data) setPosition(data.position);
      }
    };
    fetchPosition();
  }, []);

  useEffect(() => {
    springPos.set(position);
  }, [position, springPos]);

  const share = () => {
    navigator.clipboard.writeText(`${window.location.origin}/waitlist?ref=${position}`);
    alert('Referral link copied!');
  };

  return (
    <div className="min-h-screen bg-[#050505] text-white flex flex-col items-center justify-center p-6 relative overflow-hidden text-center">
      <div className="absolute inset-0 grainy-bg opacity-30 pointer-events-none" />
      
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
        className="z-10"
      >
        <h1 className="text-4xl md:text-5xl font-bold mb-4 tracking-tighter">You're on the list!</h1>
        <p className="text-white/40 uppercase tracking-[0.3em] text-[10px] mb-12">Queue position</p>
        
        <div className="mb-16">
          <motion.div className="text-[12rem] md:text-[16rem] font-bold line-height-none tracking-tighter italic text-accent">
            #{displayPos}
          </motion.div>
        </div>

        <div className="flex flex-col items-center gap-6">
          <button 
            onClick={share}
            className="px-10 py-4 border border-white/10 rounded-full text-xs uppercase tracking-widest font-bold hover:bg-white/5 transition-colors"
          >
            Share referral link
          </button>
          
          <Link href="/" className="flex items-center gap-2 text-white/40 hover:text-white transition-colors text-xs uppercase tracking-widest">
            <ArrowLeft size={14} /> Back to Home
          </Link>
        </div>
      </motion.div>
    </div>
  );
}
""",
        "app/auth/callback/route.ts": """import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const requestUrl = new URL(request.url);
  const code = requestUrl.searchParams.get('code');

  if (code) {
    const supabase = createRouteHandlerClient({ cookies });
    const { data: { user } } = await supabase.auth.exchangeCodeForSession(code);
    
    if (user) {
      // Check if in waitlist
      const { data: existing } = await supabase
        .from('waitlist')
        .select('id')
        .eq('user_id', user.id)
        .single();
      
      if (!existing) {
        await supabase.from('waitlist').insert({
          user_id: user.id,
          email: user.email!,
          full_name: user.user_metadata.full_name,
          provider: 'google'
        });
      }
    }
  }

  return NextResponse.redirect(`${requestUrl.origin}/waitlist/success`);
}
""",
        "app/auth/reset-password/page.tsx": """'use client';
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
"""
    }

    for path, content in pages.items():
        full_path = os.path.join(base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding='utf-8') as f:
            f.write(content)
        print(f"Generated: {path}")

if __name__ == "__main__":
    generate_auth_pages()
