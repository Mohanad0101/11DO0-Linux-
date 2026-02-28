# Lab 11: Python System Programming on Linux — Building Foundations for a Simple File Manager

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Learning Outcomes](#2-learning-outcomes)
3. [Prerequisites](#3-prerequisites)
4. [Lab Directory Layout](#4-lab-directory-layout)
5. [Part A — Linux Essentials](#part-a--linux-essentials-required)
6. [Part B — Vim Basics](#part-b--vim-basics-required)
7. [Part C — Install Tools](#part-c--install-tools-python-pip-venv-git)
8. [Part D — Virtual Environments and Reproducible Installation](#part-d--virtual-environments-and-reproducible-installation-required)
9. [Part E — Correct Project Copying](#part-e--correct-project-copying-copy-only-code--requirements)
10. [Part F — Real-World venv Practice: Flask Web Application](#part-f--real-world-venv-practice-flask-web-application-required)
11. [Part G — Bash ↔ Python Mapping](#part-g--bash--python-mapping-skills-needed-for-a-file-manager)
12. [Part H — Configuration File (config.json)](#part-h--configuration-file-configjson-required)
13. [Part I — Case Studies](#part-i--case-studies-step-by-step)
14. [Lab Deliverables](#lab-deliverables)
15. [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)
16. [References](#references)

---

## 1. Introduction

This lab prepares you to build a **simple command-line file manager** by teaching:

- **Safe path handling** restricting all operations to a configured workspace
- **Core file operations**  read, write, copy, move, delete
- **Reproducible environments**  virtual environments and `requirements.txt`
- **Structured configuration**  using `config.json` to separate settings from code

By the end of the lab, you will have a minimal but complete file manager that enforces a workspace boundary and can be tested interactively from the command line.

---

## 2. Learning Outcomes

By the end of this lab, you will be able to:

| # | Outcome |
|---|---------|
| 1 | Use essential Linux commands to manage files and directories. |
| 2 | Edit and save code using Vim. |
| 3 | Install Python tools and Git on Linux. |
| 4 | Create a virtual environment (venv) and manage dependencies with pip. |
| 5 | Export and reuse `requirements.txt` to rebuild an environment in a new folder. |
| 6 | Clone and run a real-world Python web application (Flask) to consolidate venv understanding. |
| 7 | Use `config.json` to configure a file manager (workspace boundary, encoding, feature flags). |
| 8 | Implement safe workspace restrictions that prevent path escaping. |
| 9 | Implement file operations (read, write, copy, move, delete) within a sandboxed workspace. |
| 10 | Build a minimal CLI file manager and test it interactively. |
| 11 | Clone, run, and test the official course repository on your machine. |

---

## 3. Prerequisites

- A **Linux** system (Ubuntu, Debian, or Linux Mint recommended) or a Linux virtual machine.
- A **terminal** and basic familiarity with typing commands.
- A **web browser** (e.g. Firefox) — needed in Part F to view the Flask application.
- **(Optional)** If your course provides an official file-manager repository URL, have it ready for Part I, Case Study 3B.

> **Working-directory rule:** All paths in this lab — `config.json`, the `workspace` folder, and all Python imports — are interpreted **relative to the directory from which you run the command**. Always verify your location with `pwd` before running any command. Explicit navigation instructions are given at every step.

---

## 4. Lab Directory Layout

All work in this lab lives under a single root folder in your home directory: **`~/lab11`**. Before starting Part A, this is the complete target structure you will build:

```
~/lab11/
├── prep_project/               ← Part D  (venv practice with NumPy)
│   ├── .venv/
│   ├── hello_numpy.py
│   └── requirements.txt
├── prep_project_copy/          ← Part E  (reproducibility test)
│   ├── .venv/
│   ├── hello_numpy.py
│   └── requirements.txt
├── flask_blog_practice/        ← Part F  (real-world venv exercise)
│   ├── .venv/
│   └── Flask-Blog-Tutorial/
│       └── tutorial1/
│           ├── app.py
│           ├── requirements.txt
│           └── ...
├── fm_project/                 ← Parts H & I  (the file manager you build)
│   ├── .venv/
│   ├── config.json
│   ├── config_loader.py
│   ├── safe_paths.py
│   ├── file_ops.py
│   ├── cli_manager.py
│   ├── test_sandbox.py
│   ├── test_ops.py
│   ├── requirements.txt
│   └── workspace/              ← sandbox boundary; all file-manager I/O stays here
│       └── docs/               ← created automatically during testing
└── Network_Systems_and_Applications/     ← Part I, Case Study 3B  (official cloned repo)
    ├── .venv/
    ├── fm/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── safety.py
    │   ├── ops.py
    │   ├── cli.py
    │   └── app.py
    ├── main.py
    ├── config.json
    ├── REPORT.md
    └── workspace/
```

Keep this diagram in mind as you work through each part; it shows exactly where every file belongs.

---

## Part A 

> **Starting location:** your home directory (`~`).

### Step A1: Create the lab root directory

**What you do:**

```bash
mkdir -p ~/lab11
cd ~/lab11
```

**Why:** A single root (`~/lab11`) keeps all lab work together and makes every relative path in later steps predictable. The `-p` flag creates parent directories silently if they already exist.

**Verify:**

```bash
pwd
```

**Expected output:** `/home/<your-username>/lab11`

> **Your result:** Record your actual output below.
>
> *`pwd` output:* _______________________________________________

---

### Step A2: List directory contents

**What you do:**

```bash
ls -la
```

**Why:** `ls -la` lists all entries in the current directory — including hidden ones (names beginning with `.`, such as `.venv`) — together with permissions, owner, size, and modification time. Listing directory contents is a fundamental file-manager operation.

At this point the directory is empty; the listing shows only `.` (current) and `..` (parent).

---

### Step A3: Practice basic file operations

> **Current location:** `~/lab11`

**What you do:**

```bash
touch sample.txt
ls -la
cp sample.txt sample_copy.txt
mv sample_copy.txt renamed.txt
rm renamed.txt sample.txt
ls -la
```

**Why:** These four commands map directly to the core operations your Python file manager must implement:

| Shell command | Operation | Python equivalent |
|---------------|-----------|-------------------|
| `touch file` | Create empty file | `Path.write_text("")` |
| `cp a b` | Copy | `shutil.copy2(a, b)` |
| `mv a b` | Move / rename | `shutil.move(a, b)` |
| `rm file` | Delete | `Path.unlink()` |

The final `ls -la` confirms the directory is clean before moving on.

---

## Part B — Vim Basics (required)

You will use **Vim** to create every Python and JSON file in this lab. Master this workflow once; refer back to the quick-reference tables whenever needed.

> **Current location:** `~/lab11`

### Step B1: Open (or create) a file

**What you do:**

```bash
vim notes.txt
```

**Why:** If `notes.txt` does not exist, Vim creates it when you save. Vim starts in **Normal mode**; you cannot type content until you switch to **Insert mode**.

---

### Step B2: Minimal edit–save–quit workflow

Follow these four steps every time you edit a file in Vim:

| Step | Key / command | What happens |
|------|---------------|--------------|
| 1 | Press `i` | Enter **Insert mode**. The status bar shows `-- INSERT --`. |
| 2 | Type (or paste) your content | Text is added at the cursor. |
| 3 | Press `Esc` | Return to **Normal mode**. The status bar clears. |
| 4 | Type `:wq` then `Enter` | **Write** the file to disk and **quit** Vim. |

**Why:** Normal mode is for navigation and commands; Insert mode is for typing. You must be in Normal mode before typing `:wq`.

**Practice:** Type a line of text, save, and quit. Then verify the file was created:

```bash
cat notes.txt
```

Remove the practice file when you are done: `rm notes.txt`

---

### Vim quick reference — save and modes

| Task | Command | Notes |
|------|---------|-------|
| Enter Insert mode | `i` | Type text from cursor position |
| Append after cursor | `a` | Alternative to `i`; inserts after the cursor |
| New line below | `o` | Opens a new line and enters Insert mode |
| Return to Normal mode | `Esc` | Always press Esc before running a command |
| Save (write) | `:w` + `Enter` | Keep editing after saving |
| Save and quit | `:wq` + `Enter` | Standard way to finish editing |
| Quit without saving | `:q!` + `Enter` | Discards all unsaved changes |
| Enable paste mode | `:set paste` + `Enter` | Prevents auto-indent when pasting from clipboard |
| Disable paste mode | `:set nopaste` + `Enter` | Restore normal Vim indent behaviour |

> **Paste tip:** When pasting multi-line code from a terminal or browser, always type `:set paste` before pressing `i`, then paste, then press `Esc` and `:set nopaste`. This prevents Vim from mis-indenting the code.

---

### Vim quick reference — navigation

| Task | Command | Notes |
|------|---------|-------|
| Move left / down / up / right | `h` / `j` / `k` / `l` | Arrow keys also work |
| Next word / previous word | `w` / `b` | Jump by words |
| Start of line | `0` | Column zero |
| First non-blank character | `^` | Useful for indented code |
| End of line | `$` | Last character |
| Beginning of file | `gg` | Jump to line 1 |
| End of file | `G` | Jump to last line |
| Go to line N | `Ngg` or `:N` | e.g. `25gg` or `:25` |

### Vim quick reference — editing and search

| Task | Command | Notes |
|------|---------|-------|
| Undo | `u` | Undo last change |
| Redo | `Ctrl+r` | Re-apply undone change |
| Delete current line | `dd` | Line is placed in the register |
| Delete to end of line | `D` | From cursor to line end |
| Copy (yank) line | `yy` | Then `p` to paste |
| Paste after cursor | `p` | Inserts register contents |
| Search forward | `/word` + `Enter` | Highlights matches |
| Jump to next match | `n` | Press again to continue |
| Replace all occurrences | `:%s/old/new/g` + `Enter` | Replaces every occurrence in the file |
| Replace with confirmation | `:%s/old/new/gc` + `Enter` | Prompts before each replacement |

---

## Part C — Install Tools (Python, pip, venv, Git)

Python 3, pip, the venv module, and Git must be installed before writing code.

> **Current location:** anywhere (installation is system-wide).

### Step C1: Install packages (Ubuntu / Debian / Mint)

**What you do:**

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
```

**Why:**

| Package | Role |
|---------|------|
| `python3` | The Python 3 interpreter |
| `python3-pip` | The `pip` package installer for Python 3 |
| `python3-venv` | The `venv` module for creating isolated environments |
| `git` | Version-control tool; used to clone repos in Parts F and I |

---

### Step C2: Verify installations

**What you do:**

```bash
python3 -V
pip3 -V
git --version
```

**Why:** Confirming installed versions before writing code avoids "command not found" errors later and ensures you are running a supported Python version (3.7 or later for `dataclasses`).

**Expected output (example):**

```
Python 3.10.12
pip 23.0.1 from /usr/lib/python3/dist-packages/pip (python 3.10)
git version 2.34.1
```

Exact version numbers depend on your Linux distribution.

> **Your result:** Record your installed versions below.
>
> Python version: _______________________________________________
>
> pip version: _______________________________________________
>
> Git version: _______________________________________________

---

## Part D — Virtual Environments and Reproducible Installation (required)

> **Current location:** `~/lab11`

A **virtual environment** (venv) is a self-contained Python installation that keeps a project's packages separate from the system-wide Python and from other projects. This prevents version conflicts.

The file **`requirements.txt`** records the exact package names and versions installed in a venv. Anyone can recreate the same environment on a different machine with:


This command reads `requirements.txt` line by line and installs every listed package into the active venv.

### Step D1: Create the practice project directory

**What you do:**

```bash
cd ~/lab11
mkdir -p prep_project
cd prep_project
```

**Why:** This folder is used only to practise venv creation and `requirements.txt`; the file manager will live in a separate directory (`fm_project`).

---

### Step D2: Create and activate a venv

**What you do:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Verify the venv is active:**

```bash
python -V
pip -V
which python
which pip
```

> **Your result:** Confirm the venv is active.
>
> Prompt prefix visible: `(.venv)` — Yes / No  *(circle one)*
>
> `python -V` output: _______________________________________________

**Why:**

- `python3 -m venv .venv` creates a private Python environment in the hidden folder `.venv`. The environment contains its own interpreter, pip, and site-packages directory.
- `source .venv/bin/activate` modifies your shell's `PATH` so that `python` and `pip` resolve to the venv's copies. You will see `(.venv)` at the start of your prompt as confirmation.
- Checking `python -V` (without the `3`) confirms you are using the venv's interpreter, not the system one.

---

### Step D3: Install a sample dependency and export requirements

**What you do:**

```bash
pip install numpy
pip freeze > requirements.txt
```

**Verify:**

```bash
cat requirements.txt
```

**Why:**

- `pip install numpy` downloads and installs the NumPy package into the active venv only — the system Python is unaffected.
- `pip freeze` outputs every installed package with its exact pinned version (e.g. `numpy==1.26.4`).
- Redirecting this to `requirements.txt` creates a **reproducible** dependency list: anyone (or you on another machine) can run `pip install -r requirements.txt` in a fresh venv to obtain the same set of packages.

**Expected output of `cat requirements.txt` (example):**

```
numpy==1.26.4
```

> **Your result:** Record the content of your `requirements.txt` below.
>
> *Content:* _______________________________________________

---

### Step D4: Create and run a test script

> **Current location:** `~/lab11/prep_project` with `.venv` active

**What you do:**

1. Open Vim: `vim hello_numpy.py`
2. Press `:set paste` + `Enter`, then `i`, then paste the code below, then `Esc` + `:set nopaste` + `:wq` + `Enter`.

```python
import numpy as np

# Confirms the venv is active and NumPy is importable.
a = np.array([1, 2, 3])
print("Array:", a)
print("Sum:", a.sum())
```

3. Run the script:

```bash
python hello_numpy.py
```

**Why:** If this script runs without error, the venv is active and NumPy is correctly installed.

**Expected output:**

```
Array: [1 2 3]
Sum: 6
```

> **Your result:** Record your actual script output below.
>
> Line 1: _______________________________________________
>
> Line 2: _______________________________________________
>
> Did the script run without errors? Yes / No  *(circle one)*

### Step D5: Deactivate the venv

**What you do:**

```bash
deactivate
Which python3 
which pip3
```

**Why:** `deactivate` restores your shell's `PATH` to its original state. Always deactivate a venv before moving to a different project that has its own venv. Failing to deactivate means the wrong Python or packages may be used in the next project.

After deactivating, the `(.venv)` prefix disappears from your prompt.

---

## Part E — Correct Project Copying (copy only code + requirements)

**Principle:** A virtual environment (`.venv/`) is **not portable**. It contains absolute paths specific to the machine and directory where it was created. When copying a Python project — to a new folder, a USB drive, or another machine — copy only:

- `.py` source files
- `requirements.txt`

Then recreate the environment with `python3 -m venv .venv` and `pip install -r requirements.txt` in the new location.

> **Current location:** `~/lab11` (you deactivated the venv in Step D5)

### Step E1: Create a clean destination folder

**What you do:**

```bash
cd ~/lab11
mkdir -p prep_project_copy
```

**Why:** The new folder is at the same level as `prep_project`, inside `~/lab11`.

---

### Step E2: Copy only Python files and requirements

**What you do:** From `~/lab11` (one level above `prep_project`), run:

```bash
cp prep_project/hello_numpy.py prep_project/requirements.txt prep_project_copy/
cd prep_project_copy
```

**Why:** Explicitly naming each file avoids accidentally copying `.venv`. At this point `prep_project_copy` contains only `hello_numpy.py` and `requirements.txt`.

**Verify:**

```bash
ls -la
```

Expected: `hello_numpy.py` and `requirements.txt` — no `.venv` folder.

> **Your result:** Confirm the contents of `prep_project_copy`.
>
> Files listed by `ls -la`: _______________________________________________
>
> Is `.venv` absent? Yes / No  *(circle one)*

---

### Step E3: Rebuild the environment and run

**What you do:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python hello_numpy.py
```

**Why:** If `hello_numpy.py` produces the same output (`Array: [1 2 3]`, `Sum: 6`) as in `prep_project`, the project is **reproducible**: the `requirements.txt` was sufficient to recreate the environment from scratch.

> **Your result:** Confirm reproducibility.
>
> Output matches `prep_project` output? Yes / No  *(circle one)*
>
> What does this prove about `requirements.txt`? _______________________________________________

### Step E4: Deactivate and return to the lab root

**What you do:**

```bash
deactivate
cd ~/lab11
```

**Why:** You have finished the reproducibility practice. Returning to `~/lab11` puts you in the correct position to start Part F.

---

## Part F — Real-World venv Practice: Flask Web Application (required)

> **Current location:** `~/lab11`

Parts D and E showed venv with a single numeric library (NumPy). A real-world Python application typically depends on many packages — each of which may depend on further packages. This part demonstrates that by cloning and running a **Flask web application**, a technology widely used to build websites and web APIs.

**What is Flask?** Flask is a lightweight Python web framework. When you run a Flask app, Python starts a small HTTP server that serves web pages in your browser. It depends on several libraries (Werkzeug for HTTP, Jinja2 for templates, etc.) — none of which are installed on the system Python. The venv isolates all of them.

**Why this matters for venv:** After this exercise, you will have seen venv being used on a project you did not write, proving that `requirements.txt` alone is sufficient to set up any correctly packaged Python project.

---

### Step F1: Create the practice folder and clone the repository

**What you do:**

```bash
cd ~/lab11
mkdir -p flask_blog_practice
cd flask_blog_practice
git clone https://github.com/Qoslaye/Flask-Students-Management-App.git
```

**Why:** `git clone` downloads the complete project history into `Flask-Blog-Tutorial/`. Keeping it inside `flask_blog_practice/` separates the venv (which you will create at the `flask_blog_practice` level) from the cloned source.

**Verify:**

```bash
ls -la
cd Flask-Students-Management-App
```
---

### Step F2: Explore the project structure

**What you do:**

```bash
ls -la 
```

**Why:** Before installing anything, observe what the project ships with. You will see:

| Entry | Purpose |
|-------|---------|
| `app.py` | The Flask application — the entry point you will run |
| `requirements.txt` | The dependency list for `pip install -r` |
| `templates/` | HTML templates (Jinja2) — Flask renders these as web pages |
| `static/` | CSS and JavaScript files served directly |

There is **no `.venv/`** folder — as expected for a correctly distributed Python project.

**Check what packages are required:**

```bash
cat requirements.txt
```

**Expected output (example):**

```
Flask
Flask-SQLAlchemy
```

Note the number of packages listed. After `pip install -r`, pip will resolve and install each package's own dependencies, typically installing 10–15 packages total from just 4 listed.

> **Your result:** Record the packages listed in the tutorial's `requirements.txt`.
>
> Number of packages listed: _______
>
> Package names: _______________________________________________

---

### Step F3: Create and activate a venv for the Flask exercise

> **Current location:** `~/lab11/flask_blog_practice`

**What you do:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Verify:**

```bash
python -V
pip list
```

**Why:** The venv is created at `flask_blog_practice/` level, not inside the cloned repo — so the same venv can serve any of the `tutorial1/`–`tutorial5/` sub-projects. After activating, `pip list` should show only `pip` and `setuptools` — a clean environment.

---

### Step F4: Install dependencies and inspect the result

**What you do:**

```bash
pip install -r requirements.txt
pip list
```

**Why:** This is the standard project setup step. `pip` resolves the dependency tree and installs every required package into the active venv. After installation, `pip list` shows the full set of installed packages — compare this with the short `requirements.txt` from Step F2 to appreciate how many transitive dependencies a framework brings.

**Expected output of `pip list` (example — versions will vary):**

```
Package          Version
---------------- -------
Flask            3.0.3
Flask-SQLAlchemy 3.1.1
itsdangerous     2.2.0
Jinja2           3.1.4
MarkupSafe       2.1.5
pip              23.0.1
SQLAlchemy       2.0.30
Werkzeug         3.0.3
```

Observe that 4 entries in `requirements.txt` produced 13 installed packages. This is the dependency chain that venv manages for you.

> **Your result:** Record the total number of packages installed.
>
> Total packages shown by `pip list`: _______
>
> How many more packages were installed compared to what was listed in `requirements.txt`? _______

---

### Step F5: Run the Flask application

> **Current location:** `~/lab11/flask_blog_practice` with `.venv` active

**What you do:**

```bash
python app.py
```

**Why:** `python app.py` starts the Flask development server. Flask listens on port 5000 by default.

**Expected terminal output (example):**

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000

```

---

### Step F6: View the application in the browser

**What you do:**

1. Open your browser (e.g. Firefox).
2. Navigate to: `http://127.0.0.1:5000`

**Why:** This confirms the application is serving HTTP responses. You should see a simple blog interface. This demonstrates that the venv contains everything Flask needs to serve a working web page — including the Jinja2 template engine, the Werkzeug HTTP layer, and all supporting packages — completely isolated from the system Python.

**Expected:** A blog-style web page rendered in the browser.

> **Your result:** Describe what you see in the browser.
>
> Page title or main heading: _______________________________________________
>
> Application is running correctly? Yes / No  *(circle one)*

---

### Step F7: Stop the server, deactivate, and return to the lab root

**What you do:**

1. In the terminal, press `Ctrl+C` to stop the Flask development server.
2. Then run:

```bash
deactivate
cd ~/lab11
```

**Why:** `Ctrl+C` sends `SIGINT`, which Flask catches and uses to shut down gracefully. Deactivating removes the Flask venv from the path so subsequent projects use their own environments.

---

### Step F8: Reflection — what this exercise demonstrates

| Question | Answer |
|----------|--------|
| Why could you not run `python app.py` without the venv? | `flask` is not installed on the system Python; it lives only in `.venv`. |
| Why is there no `.venv/` in the cloned repo? | Venvs are machine-specific; the project is distributed via `requirements.txt` only. |
| What would happen if two projects needed different Flask versions? | Each project has its own `.venv/`, so they coexist without conflict. |
| Why does `pip install -r requirements.txt` install 13 packages when only 4 were listed? | Each listed package has its own dependencies (transitive dependencies), which pip resolves automatically. |

> **Your reflection:** In your own words, state one benefit of virtual environments that you observed in this exercise.
>
> _______________________________________________
>
> _______________________________________________

---

## Part G — Bash ↔ Python Mapping (skills needed for a file manager)

The following table maps common shell operations to Python standard-library tools used in the file manager. Study it before writing code in Part I.

| File-manager operation | Bash command | Python standard library |
|------------------------|--------------|-------------------------|
| Print current directory | `pwd` | `Path.cwd()` |
| List directory contents | `ls` | `Path.iterdir()` |
| Create directory tree | `mkdir -p dir` | `Path.mkdir(parents=True, exist_ok=True)` |
| Read a text file | `cat file` | `Path.read_text(encoding="utf-8")` |
| Write a text file | `echo "text" > file` | `Path.write_text(text, encoding="utf-8")` |
| Copy a file | `cp src dst` | `shutil.copy2(src, dst)` |
| Move / rename a file | `mv src dst` | `shutil.move(src, dst)` |
| Delete a file | `rm file` | `Path.unlink()` |
| Walk a directory tree | `find dir` | `os.walk(dir)` or `Path.rglob("*")` |

**What this lab implements:** read, write, copy, move, and delete (Outcomes 9–10). Directory listing (`Path.iterdir()`) and folder navigation are implemented in the official reference repository (Case Study 3B).

**References:**
- [pathlib — Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html)
- [shutil — High-level file operations](https://docs.python.org/3/library/shutil.html)
- [os.walk](https://docs.python.org/3/library/os.html#os.walk)

---

## Part H — Configuration File (config.json) (required)

> **Current location:** `~/lab11`

### H1) Why use a configuration file?

A file manager should not hard-code paths, encoding, or feature flags inside Python code. Hard-coded values require a code change to adjust any setting. A **configuration file** externalises those values: you change the file, not the code.

In this lab, `config.json` defines the **workspace** — the directory boundary inside which all file operations are permitted. Changing `"workspace"` in the JSON file is all that is needed to point the file manager at a different folder.

---

### H2) Create the fm_project directory and config.json

**What you do:**

```bash
cd ~/lab11
mkdir -p fm_project
cd fm_project
```

Now create `config.json`:

1. Open Vim: `vim config.json`
2. Press `:set paste` + `Enter`, then `i`, paste the content below, then `Esc` + `:set nopaste` + `:wq` + `Enter`.

```json
{
  "workspace": "workspace",
  "start_dir": ".",
  "encoding": "utf-8",
  "allow_delete": true
}
```

**Field reference:**

| Field | Type | Meaning |
|-------|------|---------|
| `workspace` | string | Path to the sandbox folder, **relative to `fm_project`**. All file I/O is restricted to this folder. |
| `start_dir` | string | Initial subdirectory inside the workspace when the file manager starts. `"."` means the workspace root. |
| `encoding` | string | Character encoding used when reading and writing text files (e.g. `"utf-8"`). This setting does not affect how `config.json` itself is read — JSON is always decoded as UTF-8. |
| `allow_delete` | boolean | Feature flag. When `false`, the `del` command is disabled. This lets an administrator disallow deletion without modifying Python code. |

**Reference:** [json — JSON encoder and decoder](https://docs.python.org/3/library/json.html)

---

### H3) Validate JSON

**What you do:** From `~/lab11/fm_project`, run:

```bash
python3 -c "import json; d = json.load(open('config.json', encoding='utf-8')); print(d)"
```

**Why:** Common JSON errors — a missing comma between fields, a trailing comma after the last field, or an unquoted key — cause `json.JSONDecodeError`. Python prints the line and column of the problem, making it easy to fix. Validate the file now, before any Python code depends on it.

**Expected output:**

```
{'workspace': 'workspace', 'start_dir': '.', 'encoding': 'utf-8', 'allow_delete': True}
```

Note: Python represents the JSON `true` as Python `True` and the JSON object as a Python `dict`.

---

## Part I — Case Studies (step-by-step)

You will build three components in sequence:

1. **Case Study 1** — `config_loader.py` + `safe_paths.py`: load config and enforce the workspace boundary.
2. **Case Study 2** — `file_ops.py`: read, write, copy, move, and delete inside the sandbox.
3. **Case Study 3** — `cli_manager.py`: an interactive CLI, then compare with the official reference implementation.

> **Working directory for all of Part I:** `~/lab11/fm_project`
>
> Every command and every `python` invocation in Part I must be run from this directory.  
> Before starting Case Study 1, confirm:
>
> ```bash
> cd ~/lab11/fm_project
> pwd
> ```
>
> Expected: `/home/<your-username>/lab11/fm_project`

---

### Case Study 1: Safe workspace (prevent path escaping)

**Objective:** Load `config.json` and implement a sandbox class that restricts all path access to the configured workspace, blocking any attempt to escape (e.g. `../secret.txt` or `/etc/passwd`).

---

#### CS1 — Step 1: Create and activate a venv for fm_project

> **Location:** `~/lab11/fm_project`

**What you do:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Verify:**

```bash
python -V
```

**Why:** `fm_project` is a separate project and receives its own isolated environment. This environment will remain active for all remaining steps in Part I.

---

#### CS1 — Step 2: Create the workspace directory

> **Location:** `~/lab11/fm_project`

**What you do:**

```bash
mkdir -p workspace
```

**Why:** The `config.json` field `"workspace": "workspace"` is a path relative to `fm_project`. The `Sandbox` class (created in Step 4) calls `workspace.resolve()` and then `workspace.mkdir(parents=True, exist_ok=True)` in its constructor, so it will create the directory automatically if it is missing. Creating it manually here makes the layout explicit and confirms the configuration is correct before running any Python.

---

#### CS1 — Step 3: Create config_loader.py

> **Location:** `~/lab11/fm_project`

**What you do:**

1. Open Vim: `vim config_loader.py`
2. Press `:set paste` + `Enter`, then `i`, paste the code below, then `Esc` + `:set nopaste` + `:wq` + `Enter`.

```python
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    workspace: Path       # absolute or relative path to the sandbox folder
    start_dir: str = "."  # initial subdirectory inside the workspace
    encoding: str = "utf-8"
    allow_delete: bool = True


def load_config(path: str = "config.json") -> AppConfig:
    """
    Read config.json from the current working directory and return an AppConfig.
    Raises FileNotFoundError if the file is missing.
    Raises ValueError if the required 'workspace' field is absent.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(
            f"Config file not found: '{path}'. "
            f"Run this script from the fm_project directory."
        )

    data = json.loads(p.read_text(encoding="utf-8"))

    if "workspace" not in data:
        raise ValueError("config.json must contain the field 'workspace'.")

    return AppConfig(
        workspace=Path(data["workspace"]),
        start_dir=data.get("start_dir", "."),
        encoding=data.get("encoding", "utf-8"),
        allow_delete=bool(data.get("allow_delete", True)),
    )
```

**Why:** Separating configuration loading from the rest of the code is good software design. If the workspace path or encoding changes, you edit `config.json`, not the Python source. The `@dataclass(frozen=True)` decorator makes `AppConfig` immutable: once loaded, settings cannot be accidentally changed at runtime.

**Key design points:**

- `AppConfig.workspace` is a `Path` object, not a plain string, so `pathlib` methods (`resolve()`, `mkdir()`) can be called on it directly.
- `data.get(key, default)` avoids `KeyError` for optional fields, using safe defaults.
- The error message in `FileNotFoundError` tells the user exactly how to fix the problem.
- The `workspace` value in `config.json` is a path **relative to the current working directory** when the program runs; always run the application from `fm_project`.

---

#### CS1 — Step 4: Create safe_paths.py

> **Location:** `~/lab11/fm_project`

**What you do:**

1. Open Vim: `vim safe_paths.py`
2. Press `:set paste` + `Enter`, then `i`, paste the code below, then `Esc` + `:set nopaste` + `:wq` + `Enter`.

```python
from pathlib import Path


class Sandbox:
    """
    Restricts all path access to a single workspace directory.

    Any user-supplied path that resolves outside the workspace raises
    PermissionError. This blocks directory-traversal attacks such as
    '../secret.txt' or absolute paths like '/etc/passwd'.
    """

    def __init__(self, workspace: Path) -> None:
        # resolve() converts to an absolute path and eliminates '..' and symlinks.
        self.workspace: Path = workspace.resolve()
        # Create the workspace if it does not already exist.
        self.workspace.mkdir(parents=True, exist_ok=True)

    def resolve_inside(self, user_path: str) -> Path:
        """
        Join user_path to the workspace and resolve the result.
        Return the resolved Path if it is inside the workspace.
        Raise PermissionError if it is outside.
        """
        candidate: Path = (self.workspace / user_path).resolve()

        # A path is 'inside' the workspace if the workspace is one of its
        # ancestors, or if the candidate IS the workspace itself.
        if candidate == self.workspace or self.workspace in candidate.parents:
            return candidate

        raise PermissionError(
            f"Access denied: '{user_path}' resolves outside the workspace."
        )
```

**Why — the containment check explained:**

`Path.resolve()` converts any path to an absolute, normalised form by:
1. Expanding `..` and `.` components (e.g. `workspace/../secret` → `/home/user/lab11/secret`)
2. Following symbolic links to their real targets

After resolving, `candidate.parents` is the ordered sequence of all ancestor directories of `candidate`. The condition:

```
candidate == self.workspace   OR   self.workspace in candidate.parents
```

means: the candidate path is either the workspace itself, or the workspace appears somewhere in the candidate's ancestry — i.e., the candidate is inside the workspace. Any path that fails this test is outside the sandbox and is rejected with `PermissionError`.

---

#### CS1 — Step 5: Test sandbox behaviour

> **Location:** `~/lab11/fm_project`

**What you do:**

1. Open Vim: `vim test_sandbox.py`
2. Paste the content below, save and quit.

```python
from config_loader import load_config
from safe_paths import Sandbox

cfg = load_config("config.json")
sb = Sandbox(cfg.workspace)

test_paths = [
    "notes.txt",         # inside workspace — should be allowed
    "folder/a.txt",      # inside a subdirectory of workspace — allowed
    "../secret.txt",     # one level above workspace — must be blocked
    "/etc/passwd",       # absolute path outside workspace — must be blocked
]

print(f"Workspace: {sb.workspace}\n")
for path in test_paths:
    try:
        resolved = sb.resolve_inside(path)
        print(f"  OK      '{path}'\n          -> {resolved}")
    except PermissionError as e:
        print(f"  BLOCKED '{path}'\n          -> {e}")
```

3. Run:

```bash
python test_sandbox.py
```

**Why:** This script systematically tests both the allowed and the blocked cases. If the sandbox is implemented correctly, the first two paths resolve and the last two raise `PermissionError`.

**Expected output (example — absolute paths depend on your username):**

```
Workspace: /home/username/lab11/fm_project/workspace

  OK      'notes.txt'
          -> /home/username/lab11/fm_project/workspace/notes.txt
.
.
  BLOCKED '/etc/passwd'
          -> Access denied: '/etc/passwd' resolves outside the workspace.
```

> **Your result:** Record your actual `test_sandbox.py` output below.
>
> Workspace path shown: _______________________________________________
>
> Are `../secret.txt` and `/etc/passwd` both BLOCKED? Yes / No  *(circle one)*

---

### Case Study 2: File operations (read, write, copy, move, delete)

**Objective:** Build a `FileOps` class that implements every file operation through the sandbox, using the configured encoding for all text I/O.

---

#### CS2 — Step 1: Create file_ops.py

> **Location:** `~/lab11/fm_project`

**What you do:**

1. Open Vim: `vim file_ops.py`
2. Paste the content below, save and quit.

```python
import shutil
from pathlib import Path
from safe_paths import Sandbox


class FileOps:
    """
    Provides sandboxed file operations: read, write, copy, move, delete.

    Every method resolves the caller-supplied path through the Sandbox before
    performing any I/O. Operations outside the workspace are therefore
    impossible — the Sandbox raises PermissionError first.
    """

    def __init__(self, sandbox: Sandbox, encoding: str = "utf-8") -> None:
        self.sb = sandbox
        self.encoding = encoding

    def write_text(self, name: str, text: str) -> None:
        """Write text to a file inside the workspace, creating parent dirs."""
        p = self.sb.resolve_inside(name)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding=self.encoding)

    def read_text(self, name: str) -> str:
        """Read and return the text content of a file inside the workspace."""
        p = self.sb.resolve_inside(name)
        return p.read_text(encoding=self.encoding)

    def copy_file(self, src: str, dst: str) -> None:
        """Copy src to dst inside the workspace. Creates dst parent dirs."""
        s = self.sb.resolve_inside(src)
        d = self.sb.resolve_inside(dst)
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)

    def move(self, src: str, dst: str) -> None:
        """Move (rename) src to dst inside the workspace."""
        s = self.sb.resolve_inside(src)
        d = self.sb.resolve_inside(dst)
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(s), str(d))

    def delete_file(self, name: str) -> None:
        """Delete a single file inside the workspace."""
        p = self.sb.resolve_inside(name)
        p.unlink()
```

**Why:**

- Every method calls `self.sb.resolve_inside(...)` as its first action. Path safety is enforced at one central point (the Sandbox), not duplicated in each method.
- `p.parent.mkdir(parents=True, exist_ok=True)` automatically creates any missing intermediate directories.
- `shutil.copy2` preserves the source file's metadata (timestamps, permissions). `shutil.move` is used instead of `Path.rename` because it works correctly across different filesystem mount points.
- `str(s)` and `str(d)` are passed to `shutil.move` for compatibility with Python 3.7 and earlier.

---

#### CS2 — Step 2: Test file operations

> **Location:** `~/lab11/fm_project`

**What you do:**

1. Open Vim: `vim test_ops.py`
2. Paste the content below, save and quit.

```python
from config_loader import load_config
from safe_paths import Sandbox
from file_ops import FileOps

cfg = load_config("config.json")
sb  = Sandbox(cfg.workspace)
ops = FileOps(sb, encoding=cfg.encoding)

# Write
ops.write_text("note.txt", "Hello File Manager")
print("WRITE  -> note.txt created")

# Read
content = ops.read_text("note.txt")
print("READ   ->", content)

# Copy
ops.copy_file("note.txt", "note_copy.txt")
print("COPY   -> note_copy.txt created")
print("       ->", ops.read_text("note_copy.txt"))

# Move into a subdirectory
ops.move("note_copy.txt", "docs/moved.txt")
print("MOVE   -> docs/moved.txt")
print("       ->", ops.read_text("docs/moved.txt"))

# Delete
if cfg.allow_delete:
    ops.delete_file("note.txt")
    print("DELETE -> note.txt removed")
else:
    print("DELETE -> disabled by config (allow_delete = false)")
```

3. Run:

```bash
python test_ops.py
```

**Why:** This script exercises write, read, copy, move, and delete in a fixed sequence, covering all methods of `FileOps`. It also respects the `allow_delete` flag from `config.json`.

**Expected output:**

```
WRITE  -> note.txt created
.
.
DELETE -> note.txt removed
```

> **Your result:** Paste your actual `test_ops.py` output below.
>
> All five operations (WRITE, READ, COPY, MOVE, DELETE) succeeded? Yes / No  *(circle one)*
>
> Any unexpected errors? _______________________________________________

---

### Case Study 3: CLI file manager and official repository (required)

#### Part 3A: Build a minimal interactive CLI

**Objective:** Implement an interactive command-line interface that reads user commands in a loop, dispatches them to `FileOps`, and handles errors gracefully.

---

##### CS3A — Step 1: Create cli_manager.py

> **Location:** `~/lab11/fm_project`

**What you do:**

1. Open Vim: `vim cli_manager.py`
2. Paste the content below, save and quit.

```python
from config_loader import load_config
from safe_paths import Sandbox
from file_ops import FileOps


HELP = """
Commands:
  put  <file> <text>   Write text to a file (creates the file if absent)
  read <file>          Print the contents of a file
  copy <src> <dst>     Copy src to dst
  move <src> <dst>     Move (rename) src to dst
  del  <file>          Delete a file  (only if allow_delete = true in config)
  help                 Show this message
  exit                 Quit the file manager
"""


def main() -> None:
    cfg = load_config("config.json")
    sb  = Sandbox(cfg.workspace)
    ops = FileOps(sb, encoding=cfg.encoding)

    print("Simple File Manager")
    print(f"Workspace : {sb.workspace}")
    print(f"Encoding  : {cfg.encoding}")
    print(f"Delete    : {'enabled' if cfg.allow_delete else 'DISABLED'}")
    print(HELP)

    while True:
        try:
        cmdline = input("fm> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye")
            return

        if not cmdline:
            continue

        parts = cmdline.split(" ", 2)
        cmd   = parts[0].lower()

        try:
            if cmd == "exit":
                print("Goodbye")
                return

            elif cmd == "help":
                print(HELP)

            elif cmd == "put":
                if len(parts) < 2:
                    print("Usage: put <file> <text>")
                    continue
                filename = parts[1]
                text     = parts[2] if len(parts) > 2 else ""
                ops.write_text(filename, text)
                print(f"Saved: {filename}")

            elif cmd == "read":
                if len(parts) < 2:
                    print("Usage: read <file>")
                    continue
                print(ops.read_text(parts[1]))

            elif cmd == "copy":
                if len(parts) < 3:
                    print("Usage: copy <src> <dst>")
                    continue
                _, src, dst = cmdline.split(" ", 2)
                ops.copy_file(src, dst)
                print(f"Copied: {src} -> {dst}")

            elif cmd == "move":
                if len(parts) < 3:
                    print("Usage: move <src> <dst>")
                    continue
                _, src, dst = cmdline.split(" ", 2)
                ops.move(src, dst)
                print(f"Moved: {src} -> {dst}")

            elif cmd == "del":
                if not cfg.allow_delete:
                    print("Delete is disabled (allow_delete = false in config.json).")
                    continue
                if len(parts) < 2:
                    print("Usage: del <file>")
                    continue
                ops.delete_file(parts[1])
                print(f"Deleted: {parts[1]}")

            else:
                print(f"Unknown command: '{cmd}'. Type 'help' for the command list.")

        except PermissionError as e:
            print(f"Security error: {e}")
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
```

**Why — key design decisions:**

| Feature | Reason |
|---------|--------|
| `HELP` as a module-level constant | Easy to update; printed at startup and on `help` command |
| `len(parts) < N` guard before each command | Prevents `IndexError` when the user omits required arguments |
| `except (EOFError, KeyboardInterrupt)` around `input()` | Allows clean exit with `Ctrl+D` or `Ctrl+C` |
| Three separate `except` clauses | Distinguishes security errors, missing files, and other runtime errors |
| `if __name__ == "__main__"` guard | Allows the module to be imported in tests without running the loop |

---

##### CS3A — Step 2: Generate requirements.txt for fm_project

> **Location:** `~/lab11/fm_project` with `.venv` active

**What you do:**

```bash
pip freeze > requirements.txt
```

**Why:** The file manager uses only the Python standard library (`json`, `pathlib`, `shutil`, `dataclasses`). No third-party packages were installed, so `requirements.txt` will be empty or contain only pip's own metadata. Generating it anyway makes the project portable: anyone who receives `fm_project` can run `pip install -r requirements.txt` without needing to know whether extra packages are required.

---

##### CS3A — Step 3: Run and test the CLI interactively

> **Location:** `~/lab11/fm_project` with `.venv` active

**What you do:**

```bash
python cli_manager.py
```

At the `fm>` prompt, type each command below and press `Enter`:

```
put a.txt Hello
read a.txt
copy a.txt b.txt
read b.txt
move b.txt docs/b.txt
read docs/b.txt
del a.txt
help
exit
```

**Expected session:**

```
Simple File Manager

...
fm> put a.txt Hello 
Saved: a.txt
fm> read a.txt
xt
fm> exit
Goodbye
```

**Security test:** After re-running `python cli_manager.py`, try:

```
read ../config.json
```

**Expected:** `Security error: Access denied: '../config.json' resolves outside the workspace.`

> **Your result:** Record your CLI session outcomes.
>
> Normal session completed without errors? Yes / No  *(circle one)*
>
> Security test (`read ../config.json`) produced `Security error`? Yes / No  *(circle one)*
>
> Workspace path shown at startup: _______________________________________________

---

#### Part 3B: Clone, run, and test the official course repository (required)

**Objective:** Clone the official reference implementation, recreate its environment, run it, and compare its architecture and behaviour with your own `fm_project`.

---

##### Official repository architecture overview

The reference implementation follows a **professional multi-module package structure** that satisfies all 10 required operations from the assignment brief. Understanding its layout before cloning helps you read the code meaningfully.

```
file_manager_reference/
├── fm/                     ← Python package (the application core)
│   ├── __init__.py         ← makes fm/ a package
│   ├── config.py           ← AppConfig dataclass + ConfigLoader
│   ├── safety.py           ← PathGuard (sandbox) + PathEscapeError
│   ├── ops.py              ← FileManagerOps (one method per operation) + FMState
│   ├── cli.py              ← CommandRouter + CommandSpec (shlex-based parser)
│   └── app.py              ← FileManagerApp (wires components together)
├── main.py                 ← entry point: python main.py
├── config.json             ← workspace path (auto-created on first run)
├── REPORT.md               ← evidence template for instructor submission
└── workspace/              ← sandbox boundary (auto-created)
```

**Key architectural differences from your `fm_project`:**

| Aspect | Your `fm_project` | Official reference |
|--------|------------------|--------------------|
| Structure | Flat (all files in one directory) | Package (`fm/` with 5 modules) |
| Entry point | `python cli_manager.py` | `python main.py` |
| Path safety method | `candidate.parents` containment | `candidate.relative_to(workspace)` |
| Argument parsing | `.split(" ", 2)` | `shlex.split()` (handles quoted strings) |
| Current directory | Fixed (workspace root) | Virtual `cwd` via `FMState` |
| Folder navigation | Not implemented | `in`, `out`, `where`, `show` |
| Command names | `put`, `read`, `copy`, `move`, `del` | `put`, `read`, `dup`, `move`, `del`, `ren`, `new`, `mkd`, `rmd`, `in`, `out`, `show`, `where` |

---

##### CS3B — Step 1: Return to the lab root and deactivate the venv

**What you do:**

```bash
deactivate
cd ~/lab11
```

**Why:** The cloned repository is a separate project inside `~/lab11` and will have its own venv.

---

##### CS3B — Step 2: Obtain and clone the repository

**What you do:** Get the official file-manager repository URL from your instructor or course materials, then run:

```bash
git clone https://github.com/Mohanad0101/Network_Systems_and_Applications.git

cd Network_Systems_and_Applications
```

Replace `<REPOSITORY_URL>` with the URL provided by your instructor (e.g. `https://github.com/org/file-manager.git`).

**Why:** `git clone` creates a complete copy of the repository in `file_manager_reference`. Using a dedicated folder avoids mixing the reference code with your own `fm_project`.

**After cloning, verify the structure:**

```bash
ls -la
ls -la fm/
```

You should see `main.py`, `config.json`, `REPORT.md`, and the `fm/` directory with five `.py` modules.

---

##### CS3B — Step 3: Recreate the environment and run

**What you do:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Why:** The entry point is `main.py`, not `cli_manager.py`. `main.py` calls `ensure_default_config()` (creates `config.json` automatically if missing) then starts `FileManagerApp`.

**Expected startup output:**

```
FileManager started. Type 'help' for commands.
fm>
```

---

##### CS3B — Step 4: Run the official test scenario

At the `fm>` prompt, execute the following sequence — it exercises all major features:

```
help
mkd docs
new docs/a.txt
put docs/a.txt "hello world"
read docs/a.txt
show
in docs
where
out
ren docs/a.txt docs/b.txt
dup docs/b.txt docs/copy.txt
move docs/copy.txt moved.txt
del moved.txt
show
quit
```

**Expected behaviour highlights:**

| Command | Expected output |
|---------|----------------|
| `mkd docs` | `OK: created folder 'docs'` |
| `put docs/a.txt "hello world"` | `OK: wrote 11 chars to 'docs/a.txt'` |
| `show` | Lists `dirs: ['docs']` and `files: []` |
| `in docs` | `OK: entered 'docs'` |
| `where` | `/docs` (virtual path inside workspace) |
| `out` | `OK: moved up one level` |
| `ren docs/a.txt docs/b.txt` | `OK: renamed 'docs/a.txt' -> 'docs/b.txt'` |

> **Your result:** Record key outputs from the reference CLI test scenario.
>
> Output of `mkd docs`: _______________________________________________
>
> Output of `where` (after `in docs`): _______________________________________________
>
> Did all commands execute without errors? Yes / No  *(circle one)*

---

##### CS3B — Step 5: Security test

At the `fm>` prompt, try to escape the workspace:

```
in ..
```

**Expected output:**

```
ERROR: Forbidden: attempted to escape workspace via '..'
```

> **Your result:** Did the security test produce an ERROR as expected?
>
> Yes / No  *(circle one)*
>
> Exact error message displayed: _______________________________________________

**Why:** The reference implementation uses `PathGuard.inside()`, which calls `candidate.relative_to(self.workspace)`. If the resolved candidate is not inside the workspace, `relative_to()` raises `ValueError`, which `PathGuard` converts to `PathEscapeError`. This achieves the same security goal as your `Sandbox.resolve_inside()` but via a different API.

---

##### CS3B — Step 6: Comparative analysis

After running the reference implementation, record your answers in `REPORT.md`. Brief notes may also be written in the spaces below.

1. **Path safety:** Your sandbox uses `self.workspace in candidate.parents`. The reference uses `candidate.relative_to(self.workspace)`. Both produce the same security result — describe what each approach checks and why both are correct.

   > *Your notes:* _______________________________________________

2. **Argument parsing:** Your CLI uses `cmdline.split(" ", 2)`. The reference uses `shlex.split()`. Try running `put note.txt hello world` in each. What difference do you observe, and why does `shlex` handle it better?

   > *Your notes:* _______________________________________________

3. **Folder navigation:** The reference implements a virtual `cwd` via `FMState`. What would you need to add to your `cli_manager.py` to support `in`/`out` navigation?

   > *Your notes:* _______________________________________________

4. **Architecture:** List the responsibilities of each module in `fm/` and explain why separating them into files is better than putting all code in a single script.

   > *Your notes:* _______________________________________________

---

##### CS3B — Step 7: Fill in REPORT.md and deactivate

**What you do:**

1. Open `REPORT.md` in Vim and fill in the required sections (name, group, OS, install commands, test scenario output, security check, comparative analysis answers, conclusion).
2. Then:

```bash
deactivate
cd ~/lab11
```

---

## Lab Deliverables

At the end of the lab your `~/lab11` directory should match the following tree:

```
~/lab11/
├── prep_project/
│   ├── .venv/                        ← venv (not submitted)
│   ├── hello_numpy.py
│   └── requirements.txt
├── prep_project_copy/
│   ├── .venv/                        ← venv (not submitted)
│   ├── hello_numpy.py
│   └── requirements.txt
├── flask_blog_practice/
│   ├── .venv/                        ← venv (not submitted)
│   └── Flask-Blog-Tutorial/
│       └── tutorial1/
│           ├── app.py
│           └── requirements.txt
├── fm_project/
│   ├── .venv/                        ← venv (not submitted)
│   ├── config.json
│   ├── config_loader.py
│   ├── safe_paths.py
│   ├── file_ops.py
│   ├── cli_manager.py
│   ├── test_sandbox.py
│   ├── test_ops.py
│   ├── requirements.txt
│   └── workspace/
│       └── docs/
│           └── moved.txt             ← created during testing
└── Network_Systems_and_Applications/           ← cloned reference repo
    ├── .venv/                        ← venv (not submitted)
    ├── fm/
    ├── main.py
    ├── config.json
    ├── REPORT.md                     ← filled in and submitted
    └── workspace/
```

**Required evidence of completion (submit as instructed by your course):**

| Item | How to capture |
|------|----------------|
| Flask app running in browser (Part F) | Screenshot of `http://127.0.0.1:5000` |
| Output of `test_sandbox.py` | Screenshot or copied terminal text |
| Output of `test_ops.py` | Screenshot or copied terminal text |
| CLI session from CS3A Step 3 including the security test | Screenshot or copied terminal text |
| `ls -la ~/lab11` and `ls -la ~/lab11/fm_project` | Screenshot or copied terminal text |
| Reference repo CLI session from CS3B Steps 4–5 | Screenshot or copied terminal text |
| Completed `REPORT.md` from `file_manager_reference/` | Submitted file |

> When submitting a zip archive, **exclude all `.venv/` directories** — they are large and machine-specific. Include only `.py`, `.json`, `.txt`, and `.md` files.

---

## Common Issues and Troubleshooting

| Symptom | Likely cause | Resolution |
|---------|-------------|------------|
| `FileNotFoundError: Config file not found: 'config.json'` | Script was not run from `fm_project`. | `cd ~/lab11/fm_project` then re-run. |
| `PermissionError: Access denied: '...' resolves outside the workspace.` | The path you typed escapes the workspace. | Use only relative paths that stay inside the workspace (e.g. `notes.txt`, `subdir/file.txt`). This is expected security behaviour. |
| `ModuleNotFoundError: No module named 'config_loader'` | Script run from the wrong directory. | Confirm `pwd` is `~/lab11/fm_project`. All `.py` modules must be in the same directory. |
| `python3: command not found` or `pip3: command not found` | Tool not installed or not on PATH. | Run Part C again. Verify with `which python3`. |
| `(.venv)` not shown in prompt after `source .venv/bin/activate` | Used wrong shell (e.g. fish or csh). | Run `bash` to start a Bash session, then re-run the activate command. |
| Vim shows garbled or extra characters when pasting | Auto-indent conflicts with clipboard paste. | Type `:set paste` + `Enter` before pressing `i`, then paste. Type `:set nopaste` before saving. |
| `Usage: copy <src> <dst>` printed when command is run | Too few arguments were provided. | Include both source and destination: `copy a.txt b.txt`. |
| `flask: command not found` | The Flask venv is not active, or Flask is not installed. | Run `source ~/lab11/flask_blog_practice/.venv/bin/activate` then retry. Alternatively, use `python -m flask run`. |
| `OSError: [Errno 98] Address already in use` on port 5000 | Another Flask process is already running. | Press `Ctrl+C` in the other terminal to stop it, or run on a different port: `flask run --port 5001`. |
| `pip install numpy` fails with network errors | No internet access. | Ask your instructor for an offline `.whl` file and install it with `pip install numpy-<version>.whl`. |
| `git clone` fails with "Repository not found" | Wrong URL or no authentication. | Double-check the URL. For private repos, ensure you are logged in or have an SSH key configured. |

---

## References

| Topic | URL |
|-------|-----|
| `pathlib` — Object-oriented filesystem paths | https://docs.python.org/3/library/pathlib.html |
| `shutil` — High-level file operations | https://docs.python.org/3/library/shutil.html |
| `json` — JSON encoder and decoder | https://docs.python.org/3/library/json.html |
| `dataclasses` — Data Classes | https://docs.python.org/3/library/dataclasses.html |
| `os.walk` — Directory tree traversal | https://docs.python.org/3/library/os.html#os.walk |
| `pip freeze` — Export installed packages | https://pip.pypa.io/en/stable/cli/pip_freeze/ |
| `venv` — Creation of virtual environments | https://docs.python.org/3/library/venv.html |
| Flask — Web framework | https://flask.palletsprojects.com/ |
| Flask-Blog-Tutorial — Practice repository | https://github.com/techwithtim/Flask-Blog-Tutorial |

---

*End of Lab 11*
