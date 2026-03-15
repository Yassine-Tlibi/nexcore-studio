# Directive: Build Interactive Agency Website

## Objective

Scaffold and generate a complete interactive premium agency website
using Next.js + FastAPI following the Antigravity 2 project structure.

## Inputs Required

- Project root path (default: current directory)
- Agency name (default: "NexCore Studio")
- Accent color hex (default: #4f8ef7)

## Tools/Scripts

Call in this exact order:

1. `execution/scaffold_structure.py` — creates all folders and empty files
2. `execution/generate_frontend.py` — writes all Next.js/React/Tailwind code
3. `execution/generate_backend.py` — writes FastAPI backend code
4. `execution/generate_config.py` — writes .env.example, .gitignore, CLAUDE.md

## Outputs

A fully working project with:

- frontend/ — Next.js App Router with all sections and animations
- backend/ — FastAPI with /health and /contact endpoints
- All config files in place
- Dev-ready: `npm run dev` and `uvicorn main:app --reload` both work

## Tech Stack

- Next.js 14 + React + TypeScript + Tailwind CSS
- Framer Motion (entrance animations, hover, page transitions)
- GSAP + ScrollTrigger (parallax, scrub, drawSVG timeline)
- Lenis (smooth scroll, synced to GSAP ticker in layout.tsx)
- FastAPI + Pydantic + aiosmtplib (backend)

## Design Spec

- Background: #08080f
- Primary text: #f0f0f5
- Secondary text: #666680
- Accent: #4f8ef7, secondary teal #1d9e75
- Fonts: Syne 800 (headings), DM Mono (body/labels) via Google Fonts
- Border radius: 16px–24px everywhere
- Grain texture overlay via SVG filter in globals.css
- Frosted glass: backdrop-filter blur(12px) on navbar and cards

## Sections to generate

1. Navbar — transparent → frosted glass on scroll, layoutId active link
2. Hero — 100vh, staggered word reveal, canvas particles, bouncing arrow
3. Services — 3 tall cards, stagger entrance, hover lift + glow + zoom
4. Stats — 4 count-up numbers triggered by Intersection Observer
5. Showcase — GSAP horizontal scrub text, 3 parallax project cards
6. Process — SVG vertical line drawn by GSAP drawSVG, 4 steps
7. Contact — floating labels, POST to /contact, loading → success animation
8. Footer — minimal, social icons, Lenis back-to-top

## Global Behaviors

- Custom cursor: 12px dot + 40px ghost ring with lerp lag
- Loading screen: 0.8s logo animation, AnimatePresence fade out
- Scroll progress bar: 2px accent bar at top of viewport
- Lenis initialized in layout.tsx, synced to GSAP ticker
- All animations respect prefers-redu
