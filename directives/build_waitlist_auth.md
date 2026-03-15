# Directive: Waitlist and Authentication System

## Objective
Implement a full authentication and waitlist system for NexCore Studio using Supabase and following the premium animated design language.

## Inputs
- Supabase Project URL and Anon Key (from User)
- Existing frontend design system (Next.js, Framer Motion, GSAP)
- Existing backend architecture (FastAPI)

## Stack
- **Database/Auth**: Supabase
- **Frontend Libs**: `@supabase/supabase-js`, `@supabase/auth-helpers-nextjs`, `react-hook-form`, `zod`, `framer-motion`, `canvas-confetti`
- **Backend Libs**: `supabase`, `python-jose`

## Execution Steps
1.  **Setup Supabase**: Run `execution/setup_supabase.py` to:
    - Generate SQL migrations (`execution/migrations/001_waitlist.sql`)
    - Create Supabase client (`frontend/src/lib/supabase.ts`)
    - Update `.env.example`
2.  **Generate Auth Frontend**: Run `execution/generate_auth_pages.py` to:
    - Create Signup, Login, Callback, and Reset Password pages (`frontend/src/app/auth/`).
    - Create Auth components (`frontend/src/components/auth/`).
    - Implement Zod validations.
3.  **Generate Waitlist Frontend**: Run `execution/generate_waitlist_page.py` to:
    - Create Waitlist page (`frontend/src/app/waitlist/page.tsx`).
    - Create Waitlist components (`frontend/src/components/waitlist/`).
    - Implement premium animations and sharing logic.
4.  **Backend Integration**: Manually update `backend/main.py` and `backend/requirements.txt` to handle waitlist logic and token verification.

## Outputs
- Fully functional Auth flow (Email/Pass + Google OAuth).
- Waitlist system with real-time counter and user position tracking.
- All pages matching the agency's premium "dark/glass" aesthetic.

## Edge Cases
- **Duplicate Signups**: Handled by Supabase or SQL unique constraints.
- **Session Expiry**: Ensure client handles redirect to login.
- **Invalid Tokens**: Backend must return 401.

## Escalation Path
- If Supabase environment variables are missing, stop and ask the user to provide them.
- If existing animation components (MagneticButton, etc.) are missing, ask for their location or to create them.
