import os
import re

def update_landing_page():
    # 1. Update Navbar.tsx
    navbar_path = "frontend/src/components/Navbar.tsx"
    if os.path.exists(navbar_path):
        with open(navbar_path, "r", encoding='utf-8') as f:
            content = f.read()
        
        # Ensure MagneticButton import is correct
        if 'import MagneticButton from "./MagneticButton"' not in content:
            content = content.replace(
                'import { Menu, X } from "lucide-react";',
                'import { Menu, X } from "lucide-react";\\nimport Link from "next/link";\\nimport MagneticButton from "./MagneticButton";'
            ).replace(
                "import { Menu, X } from 'lucide-react';",
                "import { Menu, X } from 'lucide-react';\nimport Link from 'next/link';\nimport MagneticButton from './MagneticButton';"
            )

        # Update Join Waitlist button to link to /waitlist
        # Looking for the previously added CTA block or adding it fresh
        if 'href="/waitlist"' not in content:
            # Simple replacement logic for the desktop button
            # This is a bit fragile but based on the current Navbar.tsx structure
            button_pattern = re.compile(r'<div className="hidden md:block">.*?</div>', re.DOTALL)
            new_button = """<div className="hidden md:block">
            <MagneticButton>
              <Link 
                href="/waitlist" 
                className="bg-accent text-white px-6 py-2 rounded-full font-syne font-bold transition-transform hover:scale-105"
              >
                Join Waitlist
              </Link>
            </MagneticButton>
          </div>"""
            if button_pattern.search(content):
                content = button_pattern.sub(new_button, content)
            else:
                # Fallback: add before the toggle button
                content = content.replace(
                    '<button \\n            onClick={() => setIsOpen(!isOpen)}',
                    new_button + '\\n          <button \\n            onClick={() => setIsOpen(!isOpen)}'
                ).replace(
                    '<button \n            onClick={() => setIsOpen(!isOpen)}',
                    new_button + '\n          <button \n            onClick={() => setIsOpen(!isOpen)}'
                )

        with open(navbar_path, "w", encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {navbar_path}")

    # 2. Update Hero.tsx
    hero_path = "frontend/src/components/Hero.tsx"
    if os.path.exists(hero_path):
        with open(hero_path, "r", encoding='utf-8') as f:
            content = f.read()
        
        # Ensure MagneticButton and Link are available
        if 'import Link from "next/link"' not in content and "import Link from 'next/link'" not in content:
            content = "import Link from 'next/link';\n" + content
            
        # Update Hero CTA to "Join the Waitlist"
        # Assuming there is a button with a background accent
        content = content.replace(
            'Get Started', 'Join the Waitlist'
        ).replace(
            'Explore Works', 'See our Work'
        )
        
        # Replace button with Link if it's not already
        # This is generic but aims to wrap the primary action
        if 'href="/waitlist"' not in content:
            # Try to find the first button-like element and wrap it or change its behavior
            # For simplicity, we'll look for a specific button text and wrap it
            content = re.sub(
                r'(<span[^>]*?>Join the Waitlist</span>)',
                r'<Link href="/waitlist">\1</Link>',
                content
            )

        with open(hero_path, "w", encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {hero_path}")

if __name__ == "__main__":
    update_landing_page()
