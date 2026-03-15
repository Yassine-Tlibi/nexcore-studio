'use client';
import { useRef, useEffect } from 'react';
import gsap from 'gsap';

export default function MagneticButton({ children }: { children: React.ReactElement }) {
  const container = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const xTo = gsap.quickTo(container.current, "x", {duration: 1, ease: "elastic.out(1, 0.3)"});
    const yTo = gsap.quickTo(container.current, "y", {duration: 1, ease: "elastic.out(1, 0.3)"});

    const handleMouseMove = (e: MouseEvent) => {
      const { clientX, clientY } = e;
      const { left, top, width, height } = container.current!.getBoundingClientRect();
      const x = clientX - (left + width / 2);
      const y = clientY - (top + height / 2);
      
      const distance = Math.hypot(x, y);
      if (distance < 80) {
        xTo(x * 0.35);
        yTo(y * 0.35);
      } else {
        xTo(0);
        yTo(0);
      }
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return <div ref={container}>{children}</div>;
}
