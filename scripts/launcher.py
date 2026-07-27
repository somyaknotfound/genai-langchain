"""Thin desktop launcher -> frozen to 'GenAI Practice.exe'.

Runs the LIVE generate_practice.py with the system Python, so edits to the
curriculum / problem bank take effect without rebuilding the exe. Falls back
to the repo default path; override with the GENAI_REPO env var if you move it.
"""
import os
import subprocess
import sys

REPO = os.environ.get("GENAI_REPO", r"C:\Users\manam\genai-langchain")
SCRIPT = os.path.join(REPO, "scripts", "generate_practice.py")


def _python():
    for cand in ("python", "py"):
        try:
            subprocess.run([cand, "--version"], capture_output=True, check=True)
            return cand
        except Exception:
            continue
    return None


def main():
    py = _python()
    if not py:
        print("Python not found on PATH. Install Python or run the .bat launcher.")
    elif not os.path.exists(SCRIPT):
        print(f"Could not find the agent at {SCRIPT}. Set GENAI_REPO to the repo path.")
    else:
        rc = subprocess.call([py, SCRIPT] + sys.argv[1:])
        if rc != 0:
            print(f"\nAgent exited with code {rc}.")
    try:
        input("\nPress Enter to close...")
    except EOFError:
        pass


if __name__ == "__main__":
    main()
