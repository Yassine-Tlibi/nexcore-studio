# Directive: Build Auth & Waitlist System

## Objective
Connect the NexCore Studio website to Supabase for authentication and implement a full waitlist system with premium animations.

## Inputs
- Next.js frontend with Framer Motion/GSAP
- Supabase Project URL and Anon Key (provided by user)

## Stack
- **Database/Auth**: Supabase
- **Frontend**: Next.js, Framer Motion, GSAP, Zod, React Hook Form, canvas-confetti

## Layer 3: Execution Scripts
1. `execution/setup_supabase.py`:
   - Generate `frontend/src/lib/supabase.ts`.
   - Generate `execution/migrations/001_waitlist.sql`.
   - Update `.env.example`.
2. `execution/generate_auth_components.py`:
   - Create `AuthCard.tsx`, `GoogleButton.tsx`, `FormInput.tsx`, `PasswordStrength.tsx`, `TabSwitcher.tsx`.
3. `execution/generate_auth_pages.py`:
   - Create `/waitlist`, `/auth/login`, `/waitlist/success`, `/auth/callback`, `/auth/reset-password`.
   - Create `frontend/src/lib/auth.ts` (Auth logic) and `frontend/src/lib/validations/auth.schema.ts`.
4. `execution/update_landing_page.py`:
   - Modify `Navbar.tsx` and `Hero.tsx` for "Join Waitlist" CTAs.

## Requirements
- **Strictly Dark Theme**: Matching the existing site's aesthetic.
- **Animations**: Staggered entrance, magnetic buttons, glassmorphism, confetti.
- **Security**: RLS enabled, passwords handled by Supabase, PKCE flow for OAuth.

## Escalation Path
- If any script fails, stop and report the error to the user.
- If dependencies cannot be installed, escalate.
