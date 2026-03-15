import os
import subprocess
import argparse
import sys

def execute_command(cmd, cwd):
    print(f"[exec] Running: {cmd} in {cwd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def manage_dependencies(root, directory, action, packages):
    target_dir = os.path.join(root, directory)
    if not os.path.exists(target_dir):
        print(f"Error: Directory {target_dir} does not exist.")
        return

    # Determine package manager
    if os.path.exists(os.path.join(target_dir, "package.json")):
        pm = "npm"
    elif os.path.exists(os.path.join(target_dir, "requirements.txt")):
        pm = "pip"
    else:
        print(f"Error: No package.json or requirements.txt found in {target_dir}")
        return

    pkg_str = " ".join(packages)
    
    if pm == "npm":
        if action == "install":
            cmd = f"npm install {pkg_str}"
        elif action == "remove":
            cmd = f"npm uninstall {pkg_str}"
        elif action == "update":
            cmd = f"npm update {pkg_str}"
    else: # pip
        if action == "install":
            cmd = f"pip install {pkg_str}"
            # Also update requirements.txt? For now just run the command.
        elif action == "remove":
            cmd = f"pip uninstall -y {pkg_str}"
        elif action == "update":
            cmd = f"pip install --upgrade {pkg_str}"

    if execute_command(cmd, target_dir):
        print(f"Successfully {action}ed packages: {pkg_str}")
    else:
        print(f"Failed to {action} packages.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--dir", required=True, help="Target directory (frontend/backend)")
    parser.add_argument("--command", required=True, choices=["install", "remove", "update"], help="Action")
    parser.add_argument("--package", nargs="+", required=True, help="Package name(s)")
    
    args = parser.parse_args()
    manage_dependencies(args.root, args.dir, args.command, args.package)
