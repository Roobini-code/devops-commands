# Git on Windows 11 — First-Time Setup, PAT Clone, and Daily Commands

A quick reference for cloning a fresh repo in VS Code on Windows 11 for the very first time, configuring your Personal Access Token (PAT), and the everyday commands you'll use.

---

## 1. Install Git for Windows

1. Download the installer from https://git-scm.com/download/win (it auto-detects 64-bit).
2. Run the installer. Recommended options at each screen:
   - **Default editor used by Git:** *Visual Studio Code*.
   - **Adjusting the name of the initial branch:** *Override the default → `main`*.
   - **Adjusting your PATH environment:** *Git from the command line and also from 3rd-party software* (so VS Code + PowerShell can call `git`).
   - **HTTPS transport backend:** *Use the native Windows Secure Channel library*.
   - **Line ending conversions:** *Checkout Windows-style, commit Unix-style line endings* (default).
   - **Credential helper:** *Git Credential Manager* — this is what stores your PAT in Windows Credential Manager.
   - Leave all other defaults.
3. Open a new **PowerShell** or **Windows Terminal** window and verify:

```powershell
git --version
```

You should see something like `git version 2.45.x.windows.1`.

> Alternative (one-liner): `winget install --id Git.Git -e --source winget`

---

## 2. One-time global config

Run these once per machine — they apply to every repo you touch. Use PowerShell.

```powershell
git config --global user.name  "Your Name"
git config --global user.email "your.email@company.com"
git config --global init.defaultBranch main
git config --global pull.rebase false                # merge on pull (safe default)
git config --global core.editor "code --wait"        # use VS Code for commit messages
git config --global core.autocrlf true               # Windows line-endings on checkout
git config --global credential.helper manager        # Windows Credential Manager
```

**Are these 3 required?** (`init.defaultBranch`, `pull.rebase`, `core.editor`)
Only `user.name` and `user.email` are truly required — Git will refuse to commit without them. The others are strong recommendations:
- `init.defaultBranch main` — matches GitHub's default; skip only if you like the old `master` name.
- `pull.rebase false` — safest default for beginners; avoids surprise rebases.
- `core.editor "code --wait"` — only useful if you use VS Code as your editor.

Check with:

```powershell
git config --global --list
```

---

## 3. Create your PAT (GitHub)

1. GitHub → **Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. **Generate new token (classic)** → set an expiry, then check the scopes.
3. Copy the token — **you won't see it again**. Store it in a password manager.

**Are these 3 scopes required?** (`repo`, `workflow`, `read:org`)
Depends on the repo:

| Scope | When you need it |
|---|---|
| `repo` | **Always** — required to clone, pull, and push. |
| `workflow` | Only if you'll edit files under `.github/workflows/` (GitHub Actions YAML). |
| `read:org` | Only for private repos owned by an organisation (e.g. `ford-mstech/*`). Needed for SSO enterprise repos. |

For a **Ford enterprise repo**, keep all three. For a **personal public repo**, `repo` alone is fine.

> If your org enforces SSO, after creating the PAT click **Configure SSO → Authorize** next to the org name.

---

## 4. Clone using your PAT (HTTPS)

### Recommended — let Credential Manager cache the PAT

If you installed **Git Credential Manager** during setup (default), just clone normally:

```powershell
cd C:\Users\<you>\source\repos       # or wherever you keep code
git clone https://github.com/<org>/<repo>.git
```

At the first `git push`, a browser popup or Credential Manager dialog appears. Enter:
- **Username** = your GitHub username
- **Password** = paste your PAT

The PAT is saved in **Windows Credential Manager → Windows Credentials** as `git:https://github.com`. Future clones/pushes won't prompt.

### One-time embed (not recommended)

```powershell
git clone https://<USERNAME>:<PAT>@github.com/<org>/<repo>.git
```

Fast, but the PAT ends up in your shell history and `.git/config`. Avoid on shared machines.

Open the folder in VS Code:

```powershell
code <repo>
```

---

## 5. Daily Git commands

| Command | What it does |
|---|---|
| `git status` | show changed/staged/untracked files |
| `git branch` | list branches (`* main` = current) |
| `git checkout -b feature/xyz` | create + switch to new branch |
| `git checkout main` | switch branches |
| `git pull` | fetch + merge from remote current branch |
| `git fetch --all` | refresh all remote refs (no merge) |
| `git add <file>` / `git add .` | stage specific / all changes |
| `git commit -m "message"` | commit staged changes |
| `git push` | push current branch to remote |
| `git push -u origin feature/xyz` | first push of a new branch |
| `git log --oneline -10` | last 10 commits, compact |
| `git diff` | unstaged changes vs working tree |
| `git diff --staged` | staged changes vs last commit |
| `git restore <file>` | discard unstaged changes to a file |
| `git restore --staged <file>` | unstage a file (keeps edits) |
| `git stash` / `git stash pop` | park uncommitted work / restore it |
| `git merge <branch>` | merge branch into current |
| `git rebase main` | replay your commits on top of main |
| `git remote -v` | show remote URLs |

---

## 6. Typical PR workflow

```powershell
git checkout main
git pull
git checkout -b feature/add-login
# edit files…
git add .
git commit -m "feat: add login endpoint"
git push -u origin feature/add-login
# open PR on GitHub → get approval → merge
```

---

## 7. Rotate / replace your PAT later

When your PAT expires or you generate a new one:

1. Open **Start → search "Credential Manager"**.
2. Click **Windows Credentials**.
3. Under **Generic Credentials**, find `git:https://github.com` → **Remove**.
4. Next `git push` will re-prompt — paste the new PAT.

Or from PowerShell:

```powershell
git credential-manager erase
protocol=https
host=github.com

```
*(hit Enter on a blank line to confirm)*

---

## Rules of thumb

- **Never commit** PATs, `.env` files, private keys, or secrets.
- **Small, focused commits** with clear messages — future-you will thank you.
- **Always `git pull` before starting** work on a shared branch.
- **Push branches early** — a WIP push is better than losing work locally.
- Use a password manager (1Password, Bitwarden, KeePass) to store PATs; rotate them when they expire.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `git: command not found` in PowerShell | Reopen the terminal after installing. If still broken, re-run installer and pick *Git from the command line and also from 3rd-party software*. |
| `fatal: Authentication failed` on push | PAT expired or revoked → recreate + follow §7 to clear old creds. |
| `remote: The 'workflow' scope is required` | PAT missing `workflow` scope — regenerate with it checked. |
| `SAML SSO enforcement` error | Go to PAT settings → **Configure SSO → Authorize** for your org. |
| Line-ending / whitespace-only diffs | Confirm `git config --global core.autocrlf true`. |
