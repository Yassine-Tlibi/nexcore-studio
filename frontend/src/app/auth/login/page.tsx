'use client';
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
