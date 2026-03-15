'use client';
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
