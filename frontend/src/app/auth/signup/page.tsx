'use client';
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { signupSchema, SignupInput } from '@/lib/validations/auth.schema';
import { AuthCard } from '@/components/auth/AuthCard';
import { FormInput } from '@/components/auth/FormInput';
import { GoogleButton } from '@/components/auth/GoogleButton';
import { PasswordStrength } from '@/components/auth/PasswordStrength';
import { supabase } from '@/lib/supabase';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function SignupPage() {
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const { register, handleSubmit, watch, formState: { errors } } = useForm<SignupInput>({
    resolver: zodResolver(signupSchema),
  });

  const password = watch('password', '');

  const onSubmit = async (data: SignupInput) => {
    setLoading(true);
    const { error } = await supabase.auth.signUp({
      email: data.email,
      password: data.password,
      options: {
        data: { full_name: data.full_name },
        emailRedirectTo: `${window.location.origin}/auth/callback`,
      }
    });
    
    setLoading(false);
    if (error) alert(error.message);
    else router.push('/waitlist');
  };

  return (
    <div className="min-h-screen bg-[#050505] flex items-center justify-center p-4 relative overflow-hidden">
      <div className="absolute inset-0 bg-[#0a0a0a] opacity-50 grainy-bg pointer-events-none" />
      <AuthCard title="Create an account">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-2">
          <FormInput label="Full Name" registration={register('full_name')} error={errors.full_name?.message} />
          <FormInput label="Email" type="email" registration={register('email')} error={errors.email?.message} />
          <FormInput label="Password" type="password" registration={register('password')} error={errors.password?.message} />
          <PasswordStrength password={password} />
          <button
            disabled={loading}
            className="w-full bg-accent hover:bg-accent/80 text-white py-3 rounded-full font-bold mt-8 transition-all disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'Sign Up'}
          </button>
        </form>
        <GoogleButton />
        <p className="text-center mt-6 text-white/40 text-sm">
          Already have an account? <Link href="/auth/login" className="text-accent hover:underline">Sign In</Link>
        </p>
      </AuthCard>
    </div>
  );
}
