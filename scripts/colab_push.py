"""Colab -> GitHub auto-push.

Paste the snippet from the repo README into a Colab cell, OR (if you've
cloned the repo into Colab) `from colab_push import push; push()`.

It grabs the CURRENTLY OPEN notebook straight from the Colab runtime,
writes it into notebooks/, and commits+pushes to your dedicated repo.
The GitHub token is read from Colab Secrets (key icon in the sidebar),
never hardcoded.

Setup once:
  1. Colab left sidebar -> key icon (Secrets) -> add secret named GH_TOKEN
     = a GitHub fine-grained PAT with 'Contents: read/write' on this repo.
  2. Run the cell. That's it - re-run push() anytime to snapshot progress.
"""
import json
import os
import subprocess

REPO_URL_HTTPS = "https://github.com/somyaknotfound/genai-langchain.git"
REPO_SLUG = "somyaknotfound/genai-langchain"   # user/repo
BRANCH = "main"
WORKDIR = "/content/genai-langchain"


def _run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0 and p.stderr.strip():
        print(p.stderr.strip())
    return p


def _token():
    # Colab Secrets first, then env var as a fallback.
    try:
        from google.colab import userdata
        t = userdata.get("GH_TOKEN")
        if t:
            return t.strip()
    except Exception:
        pass
    return os.environ.get("GH_TOKEN", "").strip()


def _current_notebook_json():
    """Fetch the live notebook from the Colab frontend."""
    from google.colab import _message
    return _message.blocking_request("get_ipynb", request="", timeout_sec=60)["ipynb"]


def push(notebook_name=None, subdir="notebooks", author="somyaknotfound",
         email="somyaknotfound@users.noreply.github.com"):
    token = _token()
    if not token:
        raise RuntimeError(
            "No GH_TOKEN found. Add it under Colab Secrets (key icon) or set the env var.")

    authed = REPO_URL_HTTPS.replace("https://", f"https://{token}@")

    # clone (shallow) or refresh
    if not os.path.isdir(os.path.join(WORKDIR, ".git")):
        _run(["git", "clone", "--depth", "1", "-b", BRANCH, authed, WORKDIR])
    else:
        _run(["git", "-C", WORKDIR, "pull", "--ff-only"])

    _run(["git", "-C", WORKDIR, "config", "user.name", author])
    _run(["git", "-C", WORKDIR, "config", "user.email", email])
    _run(["git", "-C", WORKDIR, "remote", "set-url", "origin", authed])

    # resolve a filename
    nb = _current_notebook_json()
    if not notebook_name:
        try:
            from google.colab import _message
            path = _message.blocking_request("get_ipynb", request="", timeout_sec=60)
            notebook_name = os.path.basename(path.get("ipynb", {}).get("metadata", {})
                                             .get("colab", {}).get("name", "")) or "colab_notebook"
        except Exception:
            notebook_name = "colab_notebook"
    if not notebook_name.endswith(".ipynb"):
        notebook_name += ".ipynb"

    dest_dir = os.path.join(WORKDIR, subdir)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, notebook_name)
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)

    _run(["git", "-C", WORKDIR, "add", os.path.join(subdir, notebook_name)])
    status = _run(["git", "-C", WORKDIR, "status", "--porcelain"]).stdout.strip()
    if not status:
        print("No changes to push - notebook already up to date.")
        return
    from datetime import datetime
    msg = f"colab: {notebook_name} @ {datetime.now():%Y-%m-%d %H:%M}"
    _run(["git", "-C", WORKDIR, "commit", "-m", msg])
    r = _run(["git", "-C", WORKDIR, "push", "origin", BRANCH])
    if r.returncode == 0:
        print(f"Pushed {subdir}/{notebook_name} to {REPO_SLUG}")
    else:
        print("Push failed - check the token has Contents:read/write on the repo.")


if __name__ == "__main__":
    push()
