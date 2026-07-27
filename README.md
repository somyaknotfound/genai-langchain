# GenAI Course — Notebooks + Practice Agent

Companion repo for **Krish Naik's "Complete Generative AI with LangChain & HuggingFace"** (56 sections / 257 lectures).

Two moving parts:

1. **Colab → GitHub auto-push** — snapshot the notebook you're working on into `notebooks/` with one line.
2. **Practice agent** — reads your pushed notebooks, figures out where you are in the syllabus, and writes a dated practice set into `practice/` and into your Obsidian vault. Run it whenever you want (desktop launcher).

```
genai-langchain/
├── config.json            # repo + models + Obsidian settings
├── notebooks/             # pushed from Colab
├── practice/              # generated practice_YYYY-MM-DD.md
├── progress/progress.json # latest inferred progress snapshot
└── scripts/
    ├── curriculum.py         # the 56-section syllabus map + problem bank
    ├── generate_practice.py  # the agent
    ├── llm.py                # optional tiered-model layer
    └── colab_push.py         # Colab helper
```

The local clone lives at `C:\Users\manam\genai-langchain` (outside OneDrive, same as your `dsa-sync` setup, so OneDrive never fights `.git`).

---

## One-time setup

### 1. Create the GitHub repo
Create an **empty** repo named `genai-langchain` under `somyaknotfound` (no README/gitignore — this folder already has them). Then, from `C:\Users\manam\genai-langchain`:

```bash
git init && git add . && git commit -m "init: genai course repo + practice agent"
git branch -M main
git remote add origin https://github.com/somyaknotfound/genai-langchain.git
git push -u origin main
```

If you name it something else, update `repoUrl` in `config.json` and `REPO_URL_HTTPS`/`REPO_SLUG` in `scripts/colab_push.py`.

### 2. GitHub token for Colab
Create a **fine-grained PAT** (GitHub → Settings → Developer settings → Fine-grained tokens) scoped to just this repo with **Contents: Read and write**. In Colab, click the **key icon** (Secrets) in the left sidebar and add:
- Name: `GH_TOKEN`
- Value: the token
- Toggle "Notebook access" on

### 3. (Optional) LLM-tailored practice
The agent works fully offline with a curated problem bank. To get *personalized* sets (cheap model summarizes your notebooks, strong model writes the problems):

```bash
pip install -r requirements.txt
setx ANTHROPIC_API_KEY "sk-ant-..."   # then reopen the terminal
```

Model routing lives in `config.json → llm` (`cheapModel` = Haiku, `strongModel` = Sonnet). No key → it silently uses the offline bank.

---

## Daily use

### Push a notebook from Colab
Paste this into a cell at the end of a Colab session (rename the file to something meaningful first, e.g. `04_word2vec.ipynb`):

```python
# one-time per session: pull the helper, then push
!curl -s -o colab_push.py https://raw.githubusercontent.com/somyaknotfound/genai-langchain/main/scripts/colab_push.py
from colab_push import push
push("04_word2vec.ipynb")   # name it after the lecture/topic
```

Name notebooks with their topic (e.g. `lstm`, `rag`, `langgraph`) — the agent infers progress from those names **and** the notebook contents, so good names = better tracking.

### Generate a practice set
Double-click **`GenAI Practice.bat`** (or the `.exe`) on your Desktop. Or:

```bash
python C:\Users\manam\genai-langchain\scripts\generate_practice.py
```

Flags: `--no-push`, `--no-llm`, `--no-obsidian`, `--section <id>`.

Output lands in:
- `practice/practice_YYYY-MM-DD.md` (and pushed to the repo),
- your vault: `1 - Rough Thoughts/GenAI LOGS/` (a dated note + a living `GenAI Progress Dashboard`, linked from `Main.md`).

---

## How progress tracking works
The agent maps each notebook to syllabus sections by keyword (filename + cell contents), computes a per-stage completion %, picks your **current frontier** (the latest sections you've touched) plus one **spaced-repetition** topic, and builds problems for exactly those. Python basics/OOP are marked optional (you skipped them), so they never count against you.
