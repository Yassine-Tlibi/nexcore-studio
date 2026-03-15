import os
import argparse

def scaffold(root: str, agency_name: str):
    dirs = [
        "directives",
        "execution",
        "frontend/app",
        "frontend/components/hooks",
        "frontend/public",
        "backend",
        ".tmp",
    ]

    files = {
        "frontend/app/layout.tsx": "// Root layout — init Lenis, CustomCursor, ScrollProgressBar",
        "frontend/app/page.tsx": "// Home page — assemble all sections",
        "frontend/app/globals.css": "/* Global styles, grain texture, font imports */",
        "frontend/components/Navbar.tsx": "",
        "frontend/components/Hero.tsx": "",
        "frontend/components/Services.tsx": "",
        "frontend/components/Stats.tsx": "",
        "frontend/components/Showcase.tsx": "",
        "frontend/components/Process.tsx": "",
        "frontend/components/Contact.tsx": "",
        "frontend/components/Footer.tsx": "",
        "frontend/components/CustomCursor.tsx": "",
        "frontend/components/LoadingScreen.tsx": "",
        "frontend/components/ScrollProgressBar.tsx": "",
        "frontend/components/hooks/useInView.ts": "",
        "frontend/components/hooks/useLenis.ts": "",
        "frontend/components/hooks/useCountUp.ts": "",
        "frontend/package.json": "",
        "frontend/tailwind.config.ts": "",
        "frontend/postcss.config.js": "",
        "frontend/tsconfig.json": "",
        "backend/main.py": "",
        "backend/requirements.txt": "",
        ".env.example": "",
        ".gitignore": "",
        "CLAUDE.md": "",
    }

    print(f"[scaffold] Creating structure in: {root}")

    for d in dirs:
        path = os.path.join(root, d)
        os.makedirs(path, exist_ok=True)
        print(f"  [dir]  {path}")

    for filepath, comment in files.items():
        full = os.path.join(root, filepath)
        if not os.path.exists(full):
            with open(full, "w") as f:
                if comment:
                    f.write(comment + "\n")
            print(f"  [file] {full}")
        else:
            print(f"  [skip] {full} already exists")

    print(f"[scaffold] Done. Agency: {agency_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Project root path")
    parser.add_argument("--name", default="NexCore Studio", help="Agency name")
    args = parser.parse_args()
    scaffold(args.root, args.name)
