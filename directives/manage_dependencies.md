# Directive: Manage Dependencies

## Objective
Provide a unified way to install, remove, or update dependencies for both frontend (npm) and backend (pip/uv) components.

## Inputs Required
- `dir`: Target directory (e.g., "frontend", "backend")
- `command`: Action to take (install, remove, update)
- `package`: Package name(s) to process

## Tools/Scripts
- `execution/manage_dependencies.py`

## Outputs
- Updated `package.json` or `requirements.txt`
- Successful execution logs

## Edge Cases
- Missing package manager: Script should check for npm/pip.
- Invalid directory: Script should validate the target path.
- Network issues: Script should report installation failures.
