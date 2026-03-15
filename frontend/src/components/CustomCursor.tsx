'use client';
import { useEffect, useRef, useState } from 'react';
import gsap from 'gsap';

/**
 * CustomCursor Component
 * Replicated from kentokawazoe.com
 * Features: Hollow circle, smooth lerp trailing, expansion on hover.
 */
export default function CustomCursor() {
  const ring = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (typeof window === 'undefined' || !ring.current) return;

    // Set initial position
    gsap.set(ring.current, { xPercent: -50, yPercent: -50, scale: 1 });

    const xTo = gsap.quickTo(ring.current, "x", { duration: 0.6, ease: "power3" });
    const yTo = gsap.quickTo(ring.current, "y", { duration: 0.6, ease: "power3" });
    const scaleTo = gsap.quickTo(ring.current, "scale", { duration: 0.4, ease: "power2" });

    const moveCursor = (e: MouseEvent) => {
      xTo(e.clientX);
      yTo(e.clientY);

      const target = e.target as HTMLElement;
      const clickable = !!target.closest('button, a, input, textarea, [role="button"]');
      scaleTo(clickable ? 2.5 : 1);
      
      if (ring.current) {
        ring.current.style.backgroundColor = clickable ? 'rgba(255, 255, 255, 0.05)' : 'transparent';
      }
    };

    window.addEventListener('mousemove', moveCursor);
    return () => window.removeEventListener('mousemove', moveCursor);
  }, []);

  return (
    <div 
      ref={ring} 
      className="fixed top-0 left-0 pointer-events-none z-[9999] rounded-full border border-primary w-[30px] h-[30px]"
    />
  );
}
