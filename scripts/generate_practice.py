"""GenAI course practice agent.

Run it (or double-click the desktop launcher) whenever you want a fresh
practice set. It:
  1. pulls the dedicated repo (fetches notebooks you pushed from Colab),
  2. infers which syllabus sections you've covered from those notebooks,
  3. writes a dated practice_*.md focused on your current frontier
     (offline curated bank, or a tailored LLM set if configured),
  4. mirrors the result into your Obsidian vault,
  5. optionally commits + pushes practice/ + progress/ back to the repo.

Pure standard library for the core path; `anthropic` is optional (see llm.py).
"""
from __future__ import annotations
import json
import os
import re
import sys
import subprocess
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from curriculum import CURRICULUM  # noqa: E402
import llm  # noqa: E402


# ----------------------------- paths & config -----------------------------

def repo_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(os.environ.get("GENAI_REPO", r"C:\Users\manam\genai-langchain"))
    return Path(__file__).resolve().parents[1]


REPO = repo_root()


def load_config() -> dict:
    cfg_path = REPO / "config.json"
    if cfg_path.exists():
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    return {}


# ------------------------------- git helpers ------------------------------

def _git(*args, check=False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(REPO), *args],
        capture_output=True, text=True, check=check,
    )


def git_pull() -> str:
    if not (REPO / ".git").exists():
        return "no git repo yet (skipped pull)"
    if not _git("remote").stdout.strip():
        return "no remote configured (skipped pull)"
    r = _git("pull", "--ff-only")
    return (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "pulled"


def git_push_outputs(files) -> str:
    if not (REPO / ".git").exists() or not _git("remote").stdout.strip():
        return "no remote (saved locally only)"
    for f in files:
        _git("add", f)
    if not _git("status", "--porcelain").stdout.strip():
        return "nothing to commit"
    _git("commit", "-m", f"practice: add set for {date.today().isoformat()}")
    r = _git("push")
    return "pushed" if r.returncode == 0 else f"commit ok, push failed: {r.stderr.strip()}"


# --------------------------- notebook scanning ----------------------------

def notebook_text(path: Path) -> str:
    """Filename + all markdown/code source, lowercased, for keyword matching."""
    parts = [path.stem.replace("_", " ").replace("-", " ")]
    try:
        nb = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
        for cell in nb.get("cells", []):
            src = cell.get("source", "")
            parts.append("".join(src) if isinstance(src, list) else str(src))
    except Exception:
        pass
    return "\n".join(parts).lower()


def scan_notebooks() -> list[dict]:
    nb_dir = REPO / "notebooks"
    out = []
    if not nb_dir.exists():
        return out
    for p in sorted(nb_dir.rglob("*.ipynb")):
        out.append({"path": p, "name": p.name, "text": notebook_text(p)})
    return out


# --------------------------- progress inference ---------------------------

def _kw_hit(text: str, kw: str) -> bool:
    """Match kw at a word start (left boundary) so short tokens like 'bow'
    don't match inside 'cbow', while stems like 'summariz' still match
    'summarization'."""
    return re.search(r"(?<![a-z0-9])" + re.escape(kw), text) is not None


def detect_covered(notebooks) -> dict:
    """section_id -> list of notebook names that touched it."""
    covered: dict[str, list[str]] = {}
    for sec in CURRICULUM:
        hits = []
        for nb in notebooks:
            if any(_kw_hit(nb["text"], kw) for kw in sec["keywords"]):
                hits.append(nb["name"])
        if hits:
            covered[sec["id"]] = hits
    return covered


def build_progress(covered) -> dict:
    required = [s for s in CURRICULUM if not s.get("optional")]
    done = [s for s in required if s["id"] in covered]
    order = {s["id"]: i for i, s in enumerate(CURRICULUM)}
    frontier_idx = max((order[s["id"]] for s in CURRICULUM if s["id"] in covered), default=-1)

    stages: dict[str, dict] = {}
    for s in required:
        st = stages.setdefault(s["stage"], {"total": 0, "done": 0})
        st["total"] += 1
        if s["id"] in covered:
            st["done"] += 1

    # next uncovered required section after the frontier
    nxt = None
    for s in CURRICULUM:
        if not s.get("optional") and s["id"] not in covered and order[s["id"]] > frontier_idx:
            nxt = s
            break
    if nxt is None:
        nxt = next((s for s in CURRICULUM if not s.get("optional") and s["id"] not in covered), None)

    return {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "notebooks_seen": sum(len(v) for v in covered.values()),
        "required_total": len(required),
        "required_done": len(done),
        "percent": round(100 * len(done) / max(len(required), 1)),
        "frontier_idx": frontier_idx,
        "covered_ids": list(covered.keys()),
        "stages": stages,
        "next_id": nxt["id"] if nxt else None,
    }


def section_by_id(sid):
    return next((s for s in CURRICULUM if s["id"] == sid), None)


def choose_focus(covered, progress, cfg) -> list[dict]:
    """Most-recent covered required sections + one spaced-repetition pick."""
    window = cfg.get("recentSectionsWindow", 2)
    covered_required = [s for s in CURRICULUM if s["id"] in covered and not s.get("optional")]

    if not covered_required:
        # nothing detected yet -> start at first required section
        first = next((s for s in CURRICULUM if not s.get("optional")), CURRICULUM[0])
        return [first]

    focus = covered_required[-window:]
    if cfg.get("spacedRepetition") and len(covered_required) > window:
        earlier = covered_required[:-window]
        pick = earlier[date.today().toordinal() % len(earlier)]
        if pick not in focus:
            focus = [pick] + focus
    return focus


# ----------------------------- markdown build -----------------------------

STAGE_LABEL = {
    "foundations": "Foundations (NLP + Deep Learning)",
    "core-genai": "Core GenAI (LangChain / RAG)",
    "agents": "Agents & Tooling",
    "advanced": "Advanced (fine-tuning, graphs, MCP)",
    "deployment": "Deployment",
}


def roadmap_block(progress) -> str:
    lines = ["## Where you are", "", f"**{progress['required_done']}/{progress['required_total']} "
             f"required sections ({progress['percent']}%)** - "
             f"{progress['notebooks_seen']} notebook hits detected.", ""]
    for stage in ["foundations", "core-genai", "agents", "advanced", "deployment"]:
        st = progress["stages"].get(stage)
        if not st:
            continue
        filled = round(10 * st["done"] / max(st["total"], 1))
        bar = "#" * filled + "-" * (10 - filled)
        lines.append(f"- `{bar}` {STAGE_LABEL[stage]} - {st['done']}/{st['total']}")
    lines.append("")
    return "\n".join(lines)


def next_after(focus, covered) -> dict | None:
    """First required, uncovered section after the last focused one."""
    order = {s["id"]: i for i, s in enumerate(CURRICULUM)}
    last = max(order[s["id"]] for s in focus)
    return next((s for s in CURRICULUM if not s.get("optional")
                 and s["id"] not in covered and order[s["id"]] > last), None)


def bank_body(focus, covered, cfg) -> str:
    out = ["## Practice problems", ""]
    for sec in focus:
        out.append(f"### {sec['title']}")
        for i, p in enumerate(sec["problems"], 1):
            out.append(f"{i}. {p}")
        out.append("")
        out.append("**Checkpoint questions**")
        for c in sec["checkpoints"]:
            out.append(f"- {c}")
        out.append("")
    nxt = next_after(focus, covered)
    if nxt:
        out.append("## Up next")
        out.append(f"When ready, move on to **{nxt['title']}**.")
        out.append("")
    return "\n".join(out)


def llm_body(focus, covered, notebooks, progress, cfg) -> str:
    # cheap model: summarize the most recent notebooks
    recent = notebooks[-4:]
    summaries = [f"- {nb['name']}: {llm.summarize_notebook(cfg, nb['name'], nb['text'])}"
                 for nb in recent]
    covered_titles = [section_by_id(i)["title"] for i in progress["covered_ids"] if section_by_id(i)]
    focus_titles = [s["title"] for s in focus]
    nxt = next_after(focus, covered)

    context = (
        f"Learner progress: {progress['required_done']}/{progress['required_total']} "
        f"required sections ({progress['percent']}%).\n\n"
        f"Sections already covered:\n- " + "\n- ".join(covered_titles or ["(none yet)"]) + "\n\n"
        f"Focus these for this practice set:\n- " + "\n- ".join(focus_titles) + "\n\n"
        f"Recent notebooks and what they practiced:\n" + "\n".join(summaries) + "\n\n"
        f"Next unstarted section (mention only as a teaser): "
        f"{nxt['title'] if nxt else 'course complete'}.\n"
    )
    try:
        return llm.generate_practice(cfg, context)
    except Exception as e:
        return bank_body(focus, covered, cfg) + f"\n\n> _(LLM generation failed, used curated bank: {e})_\n"


def build_markdown(focus, covered, notebooks, progress, cfg, used_llm) -> str:
    today = date.today().isoformat()
    header = [f"# GenAI Practice - {today}", "",
              f"> Auto-generated by your practice agent "
              f"({'tailored via ' + cfg['llm']['strongModel'] if used_llm else 'curated bank'}). "
              f"Cadence: every {cfg.get('practiceCadenceDays', 3)} days.", "", ""]
    body = (llm_body(focus, covered, notebooks, progress, cfg) if used_llm
            else bank_body(focus, covered, cfg))
    return "\n".join(header) + roadmap_block(progress) + "\n" + body + "\n"


# ----------------------------- obsidian sync ------------------------------

BEGIN, END = "<!-- genai-sync:begin -->", "<!-- genai-sync:end -->"


def sync_obsidian(md, progress, cfg, practice_filename):
    ob = cfg.get("obsidian", {})
    if not ob.get("enabled"):
        return "obsidian disabled"
    vault = Path(ob["vaultPath"])
    if not vault.exists():
        return f"vault not found: {vault}"
    notes_dir = vault / ob["notesSubdir"]
    notes_dir.mkdir(parents=True, exist_ok=True)

    # 1) copy the dated practice note
    (notes_dir / practice_filename.replace("practice_", "Practice ")).write_text(md, encoding="utf-8")

    # 2) update a living progress dashboard (only between markers)
    dash = notes_dir / "GenAI Progress Dashboard.md"
    block = _dashboard_block(progress, practice_filename)
    if dash.exists():
        txt = dash.read_text(encoding="utf-8")
        if BEGIN in txt and END in txt:
            txt = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END),
                         BEGIN + "\n" + block + "\n" + END, txt, flags=re.S)
        else:
            txt = txt.rstrip() + f"\n\n{BEGIN}\n{block}\n{END}\n"
    else:
        txt = f"# GenAI Course - Progress Dashboard\n\n{BEGIN}\n{block}\n{END}\n"
    dash.write_text(txt, encoding="utf-8")

    # 3) one guarded wikilink in Main.md (idempotent)
    if ob.get("addToMainDashboard"):
        _link_from_main(vault)
    return f"synced to {notes_dir}"


def _dashboard_block(progress, practice_filename) -> str:
    lines = [f"_Updated {progress['generated']}_", "",
             f"**Progress: {progress['required_done']}/{progress['required_total']} "
             f"required sections ({progress['percent']}%)**", ""]
    for stage in ["foundations", "core-genai", "agents", "advanced", "deployment"]:
        st = progress["stages"].get(stage)
        if st:
            lines.append(f"- {STAGE_LABEL[stage]}: {st['done']}/{st['total']}")
    nxt = section_by_id(progress["next_id"]) if progress["next_id"] else None
    if nxt:
        lines += ["", f"Next up: **{nxt['title']}**"]
    latest = practice_filename.replace("practice_", "Practice ").replace(".md", "")
    lines += ["", f"Latest practice: [[{latest}]]"]
    return "\n".join(lines)


def _link_from_main(vault: Path):
    main = vault / "Main.md"
    if not main.exists():
        return
    txt = main.read_text(encoding="utf-8")
    if "GenAI Progress Dashboard" in txt:
        return
    marker = "<!-- genai-sync:link -->"
    if marker in txt:
        return
    block = (f"\n**GenAI**\n{marker}\n"
             f"- [[GenAI Progress Dashboard]] - Generative AI course tracker\n")
    if "Important Notes" in txt:
        idx = txt.index("Important Notes")
        nl = txt.index("\n", idx) + 1
        txt = txt[:nl] + block + txt[nl:]
    else:
        txt = txt.rstrip() + "\n" + block
    main.write_text(txt, encoding="utf-8")


# --------------------------------- main -----------------------------------

def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Generate a GenAI course practice set.")
    ap.add_argument("--no-push", action="store_true", help="don't commit/push to the repo")
    ap.add_argument("--no-llm", action="store_true", help="force the offline curated bank")
    ap.add_argument("--no-obsidian", action="store_true", help="skip Obsidian sync")
    ap.add_argument("--section", help="force focus on a specific section id")
    args = ap.parse_args(argv)

    cfg = load_config()
    print("GenAI practice agent")
    print("=" * 40)
    print("repo:", REPO)
    print("pull:", git_pull())

    notebooks = scan_notebooks()
    covered = detect_covered(notebooks)
    progress = build_progress(covered)
    (REPO / "progress").mkdir(exist_ok=True)
    (REPO / "progress" / "progress.json").write_text(
        json.dumps(progress, indent=2), encoding="utf-8")

    print(f"notebooks: {len(notebooks)} | covered required: "
          f"{progress['required_done']}/{progress['required_total']} ({progress['percent']}%)")

    if args.section:
        sec = section_by_id(args.section)
        focus = [sec] if sec else choose_focus(covered, progress, cfg)
    else:
        focus = choose_focus(covered, progress, cfg)
    print("focus:", ", ".join(s["title"] for s in focus))

    used_llm = (not args.no_llm) and llm.available(cfg)
    print("mode:", "LLM (tiered models)" if used_llm else "offline curated bank")

    md = build_markdown(focus, covered, notebooks, progress, cfg, used_llm)

    fname = f"practice_{date.today().isoformat()}.md"
    (REPO / "practice").mkdir(exist_ok=True)
    (REPO / "practice" / fname).write_text(md, encoding="utf-8")
    print("wrote:", REPO / "practice" / fname)

    if not args.no_obsidian:
        print("obsidian:", sync_obsidian(md, progress, cfg, fname))

    if cfg.get("autoPush") and not args.no_push:
        print("push:", git_push_outputs([f"practice/{fname}", "progress/progress.json"]))

    print("=" * 40)
    print("Done. Open the file above (or the note in your vault) and start practicing.")


if __name__ == "__main__":
    main()
