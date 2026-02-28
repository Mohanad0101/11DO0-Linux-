# Lab 1 — Primitive File Manager (CLI + JSON config + sandbox)

## What you build
A minimal file manager that works **only inside a configured workspace folder** and blocks escaping outside it.
Commands are custom (not shell duplicates).

## Setup (Linux Mint 22)
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python main.py
```

## Commands (custom names, not shell duplicates)
- help / help <command>
- where, show
- mkd, rmd, in, out
- new, put, read, del
- dup, move, ren
- quit

Tip: `put note.txt "hello world"`

## Evidence for teacher
Capture a run log:
```bash
script -q run_log.txt
python main.py
# run your test scenario
exit
```
Fill `REPORT.md` and commit both `REPORT.md` and `run_log.txt`.
