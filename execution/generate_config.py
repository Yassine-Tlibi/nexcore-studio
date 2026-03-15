"""
Generates .env.example, .gitignore, and CLAUDE.md
Usage: python execution/generate_config.py --root .
"""

import os
import argparse

ENV_EXAMPLE = """# Frontend Config
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend Config
FRONTEND_URL=http://localhost:3000
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASS=password
CONTACT_RECEIVER=receiver@example.com
"""

GITIGNORE = """# See https://help.github.com/articles/ignoring-files/ for more about ignoring files.

# dependencies
node_modules
/.pnp
.pnp.js

# testing
/coverage

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env files
.env*.local
.env

# python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
"""

CLAUDE_MD = """# Agent Instructions
Follow Layered Architecture:
1. Directive (directives/): What to do
2. Orchestration: Your decisions
3. Execution (execution/): Actual python scripts
"""

def generate(root: str):
    files = {
        ".env.example": ENV_EXAMPLE,
        ".gitignore": GITIGNORE,
        "CLAUDE.md": CLAUDE_MD,
    }
    for path, content in files.items():
        full = os.path.join(root, path)
        with open(full, "w") as f:
            f.write(content)
        print(f"  [wrote] {full}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    generate(args.root)
    print("[config] Done.")
