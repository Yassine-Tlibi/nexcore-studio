'use client';
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
