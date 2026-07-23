# Installing Soothsayer

Soothsayer is a set of Claude Code skills. Installing it means putting those skills
where Claude Code can find them. It takes a few minutes, you do it once, and there
is no API key and no account.

## What you need first

- **Claude Code**, already set up and working. Soothsayer runs on your Claude Code
  subscription.
- **A terminal.** On a Mac, open the Terminal app (Applications, then Utilities,
  then Terminal, or search "Terminal" with Spotlight). On Windows, use WSL or Git
  Bash (see below).
- **git** and **Python 3.10 or newer.** Both are standard on macOS. Check what you
  have:

```
git --version
python3 --version
```

If either says "command not found":

- **git** on a Mac: run `xcode-select --install` and follow the prompt.
- **Python** on a Mac: install from https://www.python.org/downloads/, or with
  Homebrew (`brew install python`).
- On Windows: install git from https://git-scm.com and Python from
  https://www.python.org/downloads/ (tick "Add Python to PATH" during setup).

## Install (macOS and Linux)

Paste these three lines into your terminal:

```
git clone https://github.com/DrDonDon/soothsayer.git
cd soothsayer
./install
```

You should see it list the skills (`/sooth-define`, `/sooth-structure`, and so on)
and say "Installed 11 skills".

Then **restart Claude Code** so it picks up the new skills.

## Check it worked

In Claude Code, type `/sooth-define`. If Soothsayer starts asking you to define a
problem, you are done.

You can also test the checking engine on its own, in the terminal:

```
python3 -m soothsayer demo
```

That prints each check catching a good case and a bad one.

## Install on Windows

The `./install` script needs a Unix-style shell. Use **WSL** (Windows Subsystem
for Linux) or **Git Bash**, then follow the macOS steps above. If you cannot use
either, the skills are plain folders under `skills/sooth-*`; copy each folder into
your Claude Code skills directory by hand.

## Updating

To get the latest version later:

```
cd soothsayer
git pull
./install
```

## Removing it

```
cd soothsayer
./uninstall
```

That removes the skills from Claude Code and leaves the folder in place.

## If something goes wrong

- **"command not found: git" or "python3"** — install the missing tool (see "What
  you need first").
- **"permission denied" when you run `./install`** — run `chmod +x install
  uninstall` inside the soothsayer folder, then `./install` again.
- **The skills do not appear in Claude Code** — make sure you restarted Claude
  Code. Check they installed with `ls ~/.claude/skills | grep sooth`.
- **A skill says it cannot find the checking engine** — re-run `./install` from
  inside the soothsayer folder; it records where the folder lives.
