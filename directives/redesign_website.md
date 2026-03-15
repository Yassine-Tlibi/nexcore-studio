# Directive: Redesign Website (Tahiti Numerique Style)

## Objective
Redesign the existing Next.js frontend to match the premium, boutique-agency aesthetic of https://tahitinumerique.pf/.

## Inputs Required
- Existing `frontend/` directory.

## Tools/Scripts
Call in this exact order:
1. `execution/redesign_frontend.py` — rewrites styles, config, and components.

## Outputs
- Updated `globals.css` with Cream/Red/Dark theme and Serif/Sans-serif fonts.
- Updated `tailwind.config.ts` with new color tokens.
- Redesigned components: `Navbar.tsx`, `Hero.tsx`, `Services.tsx`, `Footer.tsx`.
- New components: `Marquee.tsx`, `Methodology.tsx`.

## Design Spec
- **Background:** #F2EDE4 (Cream)
- **Accent:** #D92323 (Red)
- **Primary Text:** #1A1A1A (Dark Gray)
- **Typography:**
  - Headers: Playfair Display (Serif)
  - Body: Inter (Sans-serif)
- **Vibe:** Clean, editorial, minimalist, high-contrast.

## Component Specifics
1. **Navbar:** Sticky, minimalist, hamburger menu focus.
2. **Hero:** Centered Serif headline, red organic mask shape background element.
3. **Marquee:** "Infinite scrolling" horizontal text for services.
4. **Services:** Vertical list with images masked by the organic shape.
5. **Methodology:** Large numbers, accordion-style reveal, bold red background section.
