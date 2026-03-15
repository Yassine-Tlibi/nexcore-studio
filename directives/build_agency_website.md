# Directive: Hyper-Animated Premium Agency Website

## Objective
Rebuild the entire NexCore Studio frontend with a focus on immersive, high-end animations (20 specific techniques) using Next.js, Framer Motion, GSAP, and Lenis.

## Animation Requirements
1.  **Hero Animation**: Spitting text words, spring physics, staggered entrance, slow Ken Burns background.
2.  **Scroll-Triggered**: GSAP ScrollTrigger with scrub for every section.
3.  **Parallax**: Layered parallax (background 0.4x, images 0.6x, showcase 0.5x, shapes 0.2-0.7x).
4.  **Micro-Interactions**: Scale on mousedown, nav link underline draw, label float, glow pulse stats.
5.  **Hover Animations**: 3D tilt cards, lift, border glow, image zoom, overlay reveal.
6.  **Page Transitions**: Curtain slide-up on load, fade-between routes.
7.  **Animated Backgrounds**: Canvas particle system (80 dots, mouse repel), noise overlay, Mesh gradients.
8.  **Carousel**: Horizontal drag-to-scroll, active card scaling, pill dot navigation.
9.  **Accent Animations**: Pulsing shadows, typewriter effects, rule-line draw.
10. **Reveal Animations**: Word masks, clip-path wipes, image zoom-in.
11. **Lenis Sync**: 1.4s duration, synced to GSAP ticker.
12. **Preloader**: SVG stroke drawing (2s), progress bar, slide-out reveal.
13. **Mouse-Follow**: Lagging ghost ring cursor, hover morphing (accent circle, crosshair).
14. **Floating Shapes**: CSS bobbing, GSAP drift, Sin-wave badges.
15. **Split Text**: Span-wrapped word masks for all headings.
16. **Magnetic buttons**: 80px proximity pull, lerp strength 0.3.
17. **Glassmorphism**: rgba backgrounds, 1px borders, backdrop-blur 20px.
18. **Gradients**: Animated text gradients, rotating conic-gradients on buttons.
19. **SVG Path Drawing**: Vertical timeline path drawn by scroll.
20. **3D Web**: CSS perspective(1000px), card tilt max 12deg, digit flip-ins.

## Execution
1. Create `execution/generate_hyper_animated_frontend.py` to write all components.
2. Run the script.
3. Verify Lenis/GSAP sync in `layout.tsx`.
