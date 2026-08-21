# Linux Hands-On Scenarios — Interviews & Real Production

Each scenario follows **Problem → Approach → Commands (each with a `# what it does` explanation) → Verify → Gotchas**. Run these in the sandbox container or on any Linux box. Cross-reference the [command reference](linux-commands.md) whenever a flag is new.

> Legend: 🎓 = classic interview question · 🔥 = real incident pattern · 🛠️ = day-to-day admin task.

---

## Table of contents

### Users, groups, sudo
1. [Create a new sudo user](#1-create-a-new-sudo-user-)
2. [Force password change on first login](#2-force-password-change-on-first-login-)
3. [Give a user permission to restart one service only](#3-give-a-user-permission-to-restart-one-service-only-)
4. [Lock a leaving employee's account without deleting data](#4-lock-a-leaving-employees-account-without-deleting-data-)
5. [Set up SSH key-only login](#5-set-up-ssh-key-only-login-)

### Permissions & files
6. [Fix "permission denied" on a web-served directory](#6-fix-permission-denied-on-a-web-served-directory-)
7. [Share a directory between multiple users (setgid)](#7-share-a-directory-between-multiple-users-setgid-)
8. [Recover a file that's still open but deleted from disk](#8-recover-a-file-thats-still-open-but-deleted-from-disk-)
9. [Rename 1000 files in bulk safely](#9-rename-1000-files-in-bulk-safely-)
10. [Find and clean up files older than 30 days](#10-find-and-clean-up-files-older-than-30-days-)

### Disk & filesystem
11. [Server is out of disk — triage checklist](#11-server-is-out-of-disk--triage-checklist-)
12. [df says full but du says empty (deleted-open-file trap)](#12-df-says-full-but-du-says-empty-)
13. [Extend an LVM logical volume online](#13-extend-an-lvm-logical-volume-online-)
14. [Add a swap file on a live server](#14-add-a-swap-file-on-a-live-server-)
15. [Mount a new data disk on boot](#15-mount-a-new-data-disk-on-boot-)

### Processes & performance
16. [High CPU — find the culprit](#16-high-cpu--find-the-culprit-)
17. [High load but low CPU (I/O wait investigation)](#17-high-load-but-low-cpu-io-wait-investigation-)
18. [Memory leak — identify the process](#18-memory-leak--identify-the-process-)
19. [OOM killer struck — post-mortem](#19-oom-killer-struck--post-mortem-)
20. [Zombie processes — what and why](#20-zombie-processes--what-and-why-)
21. [Fork bomb defense with ulimit](#21-fork-bomb-defense-with-ulimit-)

### Networking
22. ["Site is down" — end-to-end triage](#22-site-is-down--end-to-end-triage-)
23. [Find which process owns port 8080](#23-find-which-process-owns-port-8080-)
24. [DNS resolves differently than expected](#24-dns-resolves-differently-than-expected-)
25. [Capture a specific request with tcpdump](#25-capture-a-specific-request-with-tcpdump-)
26. [Set up an SSH bastion / jump host workflow](#26-set-up-an-ssh-bastion--jump-host-workflow-)
27. [Reach a private service through an SSH tunnel](#27-reach-a-private-service-through-an-ssh-tunnel-)

### Logs & scheduled jobs
28. [Grep an error out of a compressed, rotated log set](#28-grep-an-error-out-of-a-compressed-rotated-log-set-)
29. [Top 10 error-generating clients in an access log](#29-top-10-error-generating-clients-in-an-access-log-)
30. [Schedule a daily backup with cron and rotate output](#30-schedule-a-daily-backup-with-cron-and-rotate-output-)
31. [Set up log rotation for a custom app](#31-set-up-log-rotation-for-a-custom-app-)

### Services & boot
32. [Convert a shell-script daemon into a systemd service](#32-convert-a-shell-script-daemon-into-a-systemd-service-)
33. [Investigate a slow boot](#33-investigate-a-slow-boot-)
34. [Service keeps restarting — debug the loop](#34-service-keeps-restarting--debug-the-loop-)

### Security & audit
35. [Detect a brute-force SSH attempt](#35-detect-a-brute-force-ssh-attempt-)
36. [Find world-writable files and SUID binaries](#36-find-world-writable-files-and-suid-binaries-)
37. [Audit what a user can `sudo`](#37-audit-what-a-user-can-sudo-)
38. [Make `/etc/resolv.conf` tamper-resistant](#38-make-etcresolvconf-tamper-resistant-)

### Text-processing drills
39. [Replace a config value across many files atomically](#39-replace-a-config-value-across-many-files-atomically-)
40. [Sum the 5th column, group by the 2nd, for a big TSV](#40-sum-the-5th-column-group-by-the-2nd-for-a-big-tsv-)
41. [Extract every URL from a JSON payload with jq](#41-extract-every-url-from-a-json-payload-with-jq-)

### Interview classics (theory + short demos)
42. [Hard link vs symbolic link](#42-hard-link-vs-symbolic-link-)
43. [What is an inode?](#43-what-is-an-inode-)
44. [Process vs thread](#44-process-vs-thread-)
45. [Foreground vs background vs daemon](#45-foreground-vs-background-vs-daemon-)
46. [`/etc/passwd` vs `/etc/shadow`](#46-etcpasswd-vs-etcshadow-)
47. [What happens when you type `ls` and press Enter?](#47-what-happens-when-you-type-ls-and-press-enter-)
48. [SIGTERM vs SIGKILL vs SIGHUP](#48-sigterm-vs-sigkill-vs-sighup-)
49. [`>` vs `>>` vs `2>&1` vs `&>`](#49--vs--vs-21-vs--)
50. [`chmod 644` vs `chmod u=rw,go=r` — same thing?](#50-chmod-644-vs-chmod-urwgor--same-thing-)

---

## 1. Create a new sudo user 🛠️

**Problem.** Add engineer `alice` with `sudo` privileges.

```bash
sudo useradd -m -s /bin/bash alice
# useradd            → create a new user account.
# -m                 → also create /home/alice with default skeleton files.
# -s /bin/bash       → login shell will be bash.
# alice              → account name.

sudo passwd alice
# passwd             → set/change a user's password interactively.
# alice              → whose password to set.

sudo usermod -aG sudo alice
# usermod            → modify an existing account.
# -a                 → APPEND (never leave -a out — see gotchas).
# -G sudo            → target group is `sudo` (Debian/Ubuntu). RHEL uses `wheel`.
```

**Verify.**

```bash
id alice
# id                 → prints uid, gid and every group alice belongs to.

sudo -l -U alice
# sudo -l            → list allowed sudo commands.
# -U alice           → check FOR alice (not for you).

su - alice -c 'sudo whoami'
# su - alice         → become alice with a login shell.
# -c '...'           → run this single command and exit.
# should print `root` because sudo → the whoami runs as root.
```

**Gotchas.**

- **Always use `-aG`** — bare `-G` **replaces** the entire secondary-group list.
- Home dir perms should be `700`; `useradd -m` handles that.
- On RHEL/CentOS/Rocky, use `wheel` instead of `sudo`.

---

## 2. Force password change on first login 🛠️

```bash
sudo chage -d 0 alice
# chage              → change password aging info.
# -d 0               → set the "last password change" date to epoch (1970-01-01)
#                      which the kernel treats as expired.
# alice              → target user.

sudo chage -l alice
# -l                 → LIST current aging values (verify what we just set).
```

**Related aging controls:**

```bash
sudo chage -M 90 -m 7 -W 14 alice
# -M 90              → max password age (must change within 90 days).
# -m 7               → min password age (cannot change again within 7 days).
# -W 14              → warn user 14 days before expiry at each login.
```

---

## 3. Give a user permission to restart one service only 🛠️

**Problem.** `alice` needs to restart nginx but must NOT have full root.

```bash
sudo visudo -f /etc/sudoers.d/alice
# visudo             → open a sudoers file in the editor with a syntax check
#                      before it's written (never edit sudoers with plain vim).
# -f <path>          → open THIS drop-in file instead of /etc/sudoers.
```

Contents:

```
alice ALL=(root) NOPASSWD:/bin/systemctl restart nginx, \
                          /bin/systemctl status  nginx
# alice             → the user this rule applies to.
# ALL=              → applies on any host (the "hostname" field of sudoers).
# (root)            → she may run these AS root (target user).
# NOPASSWD:         → don't prompt her for her own password.
# <command list>    → exact executables + args she's allowed to run.
```

**Verify.**

```bash
sudo -l -U alice
# → should list only the two systemctl commands and nothing else.

su - alice -c 'sudo systemctl restart nginx'   # → works.
su - alice -c 'sudo cat /etc/shadow'           # → denied (not on her allow-list).
```

**Gotchas.**

- Use the **full path** (`/bin/systemctl`, not `systemctl`) — sudoers matches on the literal path.
- Do NOT use wildcards like `/bin/systemctl restart *`. A user could append `; rm -rf /` on some old sudoers builds. Pin the exact command.

---

## 4. Lock a leaving employee's account without deleting data 🛠️

```bash
sudo usermod -L alice
# usermod -L         → prepend `!` to alice's password hash in /etc/shadow,
#                      making password auth impossible.

sudo chage -E 0 alice
# chage -E 0         → set account expiry date to epoch → account is disabled
#                      regardless of password/keys.

sudo pkill -KILL -u alice
# pkill              → signal every process by criteria.
# -KILL              → SIGKILL (uncatchable — force exit).
# -u alice           → owned by user alice. Kicks her live sessions.

sudo -u alice truncate -s 0 ~alice/.ssh/authorized_keys
# sudo -u alice      → run as alice (so ownership stays correct).
# truncate -s 0      → shrink file to zero bytes without deleting it.
# ~alice             → home dir of alice (tilde expansion).
```

Later, archive and delete the account cleanly:

```bash
sudo tar -czf /backups/alice.tgz -C /home alice
# tar -c             → create archive.
# -z                 → gzip compress.
# -f /backups/alice.tgz → output file path.
# -C /home           → change to /home before archiving.
# alice              → path (relative to -C) to include.

sudo userdel alice
# userdel            → delete the user (leaves home dir behind since we used no -r).
```

---

## 5. Set up SSH key-only login 🛠️

**On your laptop:**

```bash
ssh-keygen -t ed25519 -C "alice@laptop"
# ssh-keygen         → generate a key pair.
# -t ed25519         → use the Ed25519 algorithm (fast, modern, small keys).
# -C "..."           → comment stored in the public key (helps identify keys later).

ssh-copy-id -p 22 alice@server
# ssh-copy-id        → copy your default public key(s) to the remote authorized_keys.
# -p 22              → SSH port (change if the server listens elsewhere).
# alice@server       → who to authenticate as, where to install the key.
```

**On the server** — harden sshd once key login works:

```bash
sudo sed -i \
    -e 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' \
    -e 's/^#\?PermitRootLogin.*/PermitRootLogin no/' \
    -e 's/^#\?ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' \
    /etc/ssh/sshd_config
# sed -i             → edit file in place.
# -e '<expr>'        → multiple substitution rules.
# 's/^#\?FOO.*/FOO=no/' → whether the line is commented (#) or not, force the desired value.

sudo sshd -t
# sshd -t            → CONFIG TEST — parses sshd_config and exits, non-zero on error.
#                      Never skip this: a bad reload can lock you out.

sudo systemctl reload ssh
# systemctl reload   → send sshd SIGHUP so it re-reads config with no dropped sessions.
```

**Verify.**

```bash
ssh alice@server                              # should succeed (key auth).
ssh -o PubkeyAuthentication=no alice@server   # should fail (password disabled).
# -o KEY=VALUE       → override a single ssh option for THIS invocation only.
```

**Gotcha.** Keep the current SSH session open while you reload. If the new config breaks anything, you still have a way in to fix it.

---

## 6. Fix "permission denied" on a web-served directory 🛠️

**Symptom.** nginx (running as `www-data`) logs `13: Permission denied` for `/var/www/site`.

Nginx needs `x` on every parent dir it traverses, `r` on files it serves, `x` on dirs it lists.

```bash
sudo chown -R deploy:www-data /var/www/site
# chown              → change ownership.
# -R                 → recurse into subdirs.
# deploy:www-data    → owner=deploy, group=www-data (the web-server group).

sudo find /var/www/site -type d -exec chmod 750 {} \;
# find <path>        → traverse the tree.
# -type d            → only directories.
# -exec chmod 750 {} → run chmod 750 on each match.
# \;                 → end of -exec (one exec per match — slower than +, but fine here).
# 750                → rwx r-x --- (owner all, group read+traverse, other none).

sudo find /var/www/site -type f -exec chmod 640 {} \;
# 640                → rw- r-- --- (owner read+write, group read only, other none).

namei -mo /var/www/site/index.html
# namei              → walk each component of the path.
# -m                 → print mode (rwx string) of each component.
# -o                 → print owner and group of each component.
# → single most useful command when permission-denied is somewhere UP the path.
```

---

## 7. Share a directory between multiple users (setgid) 🛠️

```bash
sudo groupadd -f devs
# groupadd           → create group.
# -f                 → silently succeed if it already exists.

sudo usermod -aG devs alice
sudo usermod -aG devs bob
# -aG devs           → APPEND devs to the users' secondary groups.

sudo mkdir -p /srv/shared
# mkdir -p           → create with parents, no error if exists.

sudo chown root:devs /srv/shared
# chown owner:group  → root owns it, devs is the shared group.

sudo chmod 2775 /srv/shared
# 2775               → SUID/SGID/sticky digit + rwxrwxr-x.
# leading `2`        → SETGID on the directory: new files inside inherit group=devs.

sudo find /srv/shared -type d -exec chmod 2775 {} \;
sudo find /srv/shared -type f -exec chmod 664  {} \;
# apply the same policy retroactively to existing content.

sudo setfacl -R -m d:g:devs:rwx /srv/shared
# setfacl -R         → recursive.
# -m d:g:devs:rwx    → MODIFY the DEFAULT (d:) ACL: group devs gets rwx.
# → default ACLs apply automatically to future files created under the tree.
```

**Test.**

```bash
sudo -u alice touch /srv/shared/hello
# create as alice.

ls -l /srv/shared/hello
# → group should read as `devs`, mode `-rw-rw-r--`.
```

---

## 8. Recover a file that's still open but deleted from disk 🔥

**Symptom.** Someone `rm`'d `app.log` while the app kept writing to it; `ls` doesn't show it but `df` doesn't recover the space either.

```bash
sudo lsof +L1 | grep app.log
# lsof               → list open files.
# +L1                → filter to files with link count < 1
#                      i.e. deleted but still open.
# grep app.log       → narrow to the one we care about.

# example output:
# myapp 1234 app 3w REG 8,1  10485760 0 12345 /var/log/app.log (deleted)
#                ^^^ fd=3 in write mode

sudo cp /proc/1234/fd/3 /var/log/app.log.recovered
# /proc/<PID>/fd/<N> → symlink to the still-open inode.
# copying through it → reads the current live contents to a new path.
```

**Verify + follow-up.**

```bash
wc -l /var/log/app.log.recovered
# wc -l              → count lines in the recovered file.

sudo lsof +L1 | grep app.log
# → still shown as (deleted) until the app itself closes/rotates the fd.

# Long-term fix: switch logrotate to `copytruncate` OR have the app HUP on rotate.
```

---

## 9. Rename 1000 files in bulk safely 🛠️

Prepend today's date to every `*.log`:

```bash
today=$(date +%F)
# $(...)             → command substitution.
# date +%F           → today's date as YYYY-MM-DD (ISO 8601).

for f in *.log; do
    mv -n -- "$f" "${today}_${f}"
done
# for f in *.log     → iterate matching files (glob expansion).
# mv -n              → NO-CLOBBER: refuse to overwrite an existing target file.
# --                 → end of options — filenames beginning with `-` are treated as filenames.
# "${today}_${f}"    → new name.
```

Or with the Perl `rename` (Debian/Ubuntu):

```bash
rename -n 's/^/'"$today"'_/' *.log     # -n = dry run: preview first.
rename    's/^/'"$today"'_/' *.log     # remove -n to actually rename.
# rename 's/A/B/'    → apply Perl substitution to each filename.
```

Safe with weird filenames (spaces, newlines):

```bash
find . -maxdepth 1 -type f -name '*.log' -print0 |
    xargs -0 -I{} mv -n -- {} "${today}_"{}
# -print0            → separate results with NUL, not newline.
# xargs -0           → read NUL-separated input.
# -I{}               → placeholder — appears twice in the command.
```

---

## 10. Find and clean up files older than 30 days 🛠️

```bash
find /var/backups -type f -mtime +30 -printf '%T+ %s %p\n' | sort
# find <path>        → walk tree.
# -type f            → regular files only.
# -mtime +30         → mtime older than 30 * 24h.
# -printf '%T+ %s %p\n' → format: mtime<tab>size<space>path.
# sort               → chronological output for review.
```

Compress first, delete later:

```bash
find /var/backups -type f -mtime +30 ! -name '*.gz' -exec gzip {} +
# ! -name '*.gz'     → skip already-compressed files.
# -exec gzip {} +    → gzip in batches (one gzip call per batch — much faster).

find /var/backups -type f -mtime +90 -delete
# -delete            → remove the matched files in place.
```

`-mtime` recap:

| Expression | Meaning |
|---|---|
| `-mtime +30` | Modified MORE than 30 days ago. |
| `-mtime -1` | Modified in the LAST 24h. |
| `-mtime 0` | Modified in the last 24h (same as `-1`). |
| `-mmin +10` | Modified more than 10 minutes ago (finer control). |

---

## 11. Server is out of disk — triage checklist 🔥

```bash
df -hT
# df                 → disk-free per mount.
# -h                 → human-readable sizes.
# -T                 → show filesystem type — tells you if it's tmpfs, xfs, ext4, overlay…

df -i
# -i                 → INODE usage. A FS can be full on inodes (millions of tiny files)
#                      while byte usage still shows GB free.

sudo du -h -x -d 1 / 2>/dev/null | sort -h | tail
# du                 → disk-usage per path.
# -h                 → human-readable.
# -x                 → stay on ONE filesystem (don't cross into /proc, /sys, mounts).
# -d 1               → depth 1 (only immediate children).
# 2>/dev/null        → hide "permission denied" noise.
# sort -h            → sort by human-readable sizes.
# tail               → biggest at the bottom.

sudo ncdu -x /var
# ncdu               → interactive TUI drill-down of du output.
# -x                 → don't cross filesystems.
```

**Usual suspects (in order):**

1. `/var/log/*.log` grew unbounded — see scenario 31 to rotate it.
2. `journalctl` — check with `sudo journalctl --disk-usage`, trim with `sudo journalctl --vacuum-time=7d`.
3. Docker layers — `sudo docker system df` + `sudo docker system prune -af --volumes`.
4. Package cache — `sudo apt clean` or `sudo dnf clean all`.
5. Old kernels — `sudo apt autoremove --purge`.
6. Deleted-but-open files — see scenario 12.
7. Inode exhaustion — `find / -xdev -type f | wc -l` on a suspect FS.

---

## 12. df says full but du says empty 🔥

**Cause.** A process still holds an FD to a file that was `rm`'d. Blocks stay allocated to the inode until the FD closes.

```bash
sudo lsof +L1
# +L1                → filter: link count < 1 → deleted but still open.

sudo lsof +L1 | awk '$7+0 > 1024*1024*100 {print $2, $9, $7}' | sort -k3 -n
# awk               → filter to files > 100 MiB.
# $7+0              → force numeric interpretation of column 7 (size in bytes).
# > 1024*1024*100   → 100 MiB threshold.
# print $2 $9 $7    → PID, path, size.
# sort -k3 -n       → sort by size column numerically.
```

**Fix.**

```bash
# 1) Restart the guilty process (or send SIGHUP if it reopens logs).
sudo systemctl restart myapp

# 2) Emergency stopgap without restart — truncate through /proc:
sudo bash -c ': > /proc/1234/fd/3'
# : > FILE           → the null command with output redirection truncates FILE.
# /proc/<PID>/fd/<N> → the still-open inode.
```

---

## 13. Extend an LVM logical volume online 🛠️

**Scenario.** `/data` is on `/dev/data-vg/app-lv` and needs +20 GB while it's mounted.

```bash
sudo vgs
# vgs                → summary of every volume group (name, PVs, LVs, free space).
# → confirm data-vg has ≥ 20 GB free BEFORE extending.

sudo lvextend -L +20G /dev/data-vg/app-lv
# lvextend           → grow a logical volume.
# -L +20G            → RELATIVE growth (leading `+`) of 20 GiB.
# path               → the LV device.

sudo resize2fs /dev/data-vg/app-lv
# resize2fs          → grow (or shrink) ext[234] FS to match its device.
# → for XFS instead:  sudo xfs_growfs /data     (XFS takes the MOUNT POINT).

df -h /data
# → verify new size shows up.
```

**No free VG extents?**

```bash
sudo pvcreate /dev/sdc
# pvcreate           → mark /dev/sdc as an LVM physical volume.

sudo vgextend data-vg /dev/sdc
# vgextend           → add the PV to the VG so more space is available.
```

**Gotchas.**

- `xfs_growfs` takes the **mount point**, `resize2fs` takes the **device**.
- XFS can grow but never shrink.

---

## 14. Add a swap file on a live server 🛠️

```bash
sudo fallocate -l 4G /swapfile
# fallocate          → allocate space fast (no zero-fill on ext4/xfs).
# -l 4G              → 4 GiB length.

sudo chmod 600 /swapfile
# chmod 600          → owner rw only. Kernel refuses to swapon otherwise.

sudo mkswap /swapfile
# mkswap             → format the file with swap metadata.

sudo swapon /swapfile
# swapon             → activate it as a swap device.

swapon --show
free -h
# --show             → list active swap.
# free -h            → confirm total memory now includes swap.

echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
# tee -a /etc/fstab  → append a persistent mount entry so it survives reboot.
# sw                 → default swap options.
# 0 0                → dump=0, fsck=0.
```

Tune for a DB workload:

```bash
sudo sysctl vm.swappiness=10
# sysctl vm.swappiness=10 → prefer to keep pages in RAM; use swap only under pressure.

echo 'vm.swappiness=10' | sudo tee /etc/sysctl.d/99-swap.conf
# drop-in makes it persist across reboots.
```

---

## 15. Mount a new data disk on boot 🛠️

```bash
lsblk
# lsblk              → tree view: disks → partitions → mounts. Spot the new /dev/sdb.

sudo parted /dev/sdb mklabel gpt
# parted mklabel gpt → create a GPT partition table (modern layout).

sudo parted -a opt /dev/sdb mkpart primary ext4 0% 100%
# -a opt             → optimal alignment.
# mkpart <name> <fs-hint> <start> <end> → create one partition spanning the whole disk.

sudo mkfs.ext4 -L data /dev/sdb1
# mkfs.ext4          → format as ext4.
# -L data            → give the FS the label "data" (usable as `LABEL=data` in fstab).

sudo mkdir -p /data
sudo mount /dev/sdb1 /data
# mkdir -p           → create the mount point.
# mount              → mount NOW (not persistent yet).

blkid /dev/sdb1
# blkid              → print UUID + TYPE. Copy the UUID for /etc/fstab.

echo 'UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx /data ext4 defaults,nofail 0 2' \
    | sudo tee -a /etc/fstab
# UUID=…             → immutable identifier; safer than /dev/sdX which can renumber.
# /data              → mount point.
# ext4               → FS type.
# defaults,nofail    → normal options + don't block boot if the disk is missing (cloud disks!).
# 0                  → dump: skip.
# 2                  → fsck order (2 = non-root).

sudo mount -a
# -a                 → mount everything in fstab (silent on success = you're good).

sudo findmnt /data
# findmnt            → confirm what's mounted where + options in effect.
```

---

## 16. High CPU — find the culprit 🔥

```bash
top -o %CPU
# top                → live process table.
# -o %CPU            → sort by CPU descending on launch.
# → note the offending PID.

ps -eo pid,user,pcpu,pmem,cmd --sort=-pcpu | head
# ps -e              → all processes.
# -o …               → custom columns.
# --sort=-pcpu       → descending by %cpu.
# head               → top 10.

pidstat -u 1 5 -p <PID>
# pidstat            → per-process stats.
# -u                 → CPU usage.
# 1 5                → sample every 1 second for 5 samples.
# -p <PID>           → narrow to one process → confirms sustained (not spike) load.
```

Figure out **why**:

```bash
ls -l /proc/<PID>/exe
# → symlink to the binary — reveals actual program path (helpful when the name is generic like `python`).

cat /proc/<PID>/cmdline | tr '\0' ' '; echo
# /proc/<PID>/cmdline → the exact argv as NUL-separated bytes.
# tr '\0' ' '        → turn NULs into spaces so you can read it.
# ; echo             → newline at the end.

sudo strace -c -p <PID>
# strace             → trace syscalls of a running process (needs SYS_PTRACE).
# -c                 → don't dump every syscall — accumulate a summary.
# → Ctrl-C after ~30s to see counts by syscall.

sudo perf top -p <PID>
# perf top           → live sampling profiler.
# -p <PID>           → attach to one process. Shows hottest functions.
```

Interpretation cheat-sheet from `strace -c`:

- `futex` dominates → thread contention.
- `read`/`write` dominate → I/O bound.
- `getpid` / `clock_gettime` dominate → busy-wait loop.

---

## 17. High load but low CPU (I/O wait investigation) 🔥

**Symptom.** `uptime` shows load 20 on a 4-CPU box; `%CPU` in top is 30%. Likely disk wait.

```bash
top
# → look at the `wa` column (I/O wait %). Anything > 10% sustained = bad.

vmstat 1
# vmstat 1           → every 1s, print system counters.
# → watch `b` column (blocked processes). Climbing = something is stuck in D-state.

iostat -xz 1
# iostat -x          → extended per-device stats.
# -z                 → skip idle devices.
# 1                  → every second.
# → high `%util`, `await`, `r_await`/`w_await` = disk is the bottleneck.

ps -eo pid,stat,cmd | awk '$2 ~ /D/'
# ps -eo …           → PID, state, command.
# awk '$2 ~ /D/'     → filter to state field containing "D" (uninterruptible sleep).
# → these are processes waiting on I/O the kernel won't interrupt.

sudo iotop -oPa
# iotop              → per-process I/O rates.
# -o                 → show ONLY procs doing I/O right now.
# -P                 → show processes (not threads).
# -a                 → accumulate totals since iotop started.
```

Common causes: NFS server hung, disk failing, RAID rebuild, dirty-page flush storm from a DB.

---

## 18. Memory leak — identify the process 🔥

```bash
watch -n 5 'ps -eo pid,user,rss,vsz,cmd --sort=-rss | head'
# watch              → re-run a command periodically.
# -n 5               → every 5 seconds.
# rss                → resident set size (physical RAM).
# vsz                → virtual size (address space).
# → look for one process whose RSS grows monotonically.

# quantify the growth over time:
while true; do
    printf '%s %s\n' "$(date +%s)" "$(ps -p <PID> -o rss=)"
    sleep 30
done | tee mem.log
# printf '%s %s\n'   → epoch<space>RSS<newline>.
# date +%s           → seconds since 1970.
# ps -p <PID> -o rss= → just the RSS value, no header.
# sleep 30           → 30 seconds between samples.
# tee mem.log        → capture to file while also printing on screen.
```

Rule out shared / cached pages:

```bash
cat /proc/<PID>/status | grep -E 'VmRSS|VmSwap|VmPeak'
# grep -E            → extended regex (alternation via |).

cat /proc/<PID>/smaps_rollup 2>/dev/null | grep -E 'Rss|Pss|Swap'
# smaps_rollup       → summary of memory mappings.
# Pss (Proportional Set Size) = private + shared/N_sharers.
#     Fairest single-number memory metric per process.
```

---

## 19. OOM killer struck — post-mortem 🔥

```bash
sudo dmesg -T | grep -iE 'oom|killed process'
# dmesg              → kernel ring buffer.
# -T                 → human timestamps (instead of seconds since boot).
# grep -iE           → case-insensitive extended regex.
# → find the kernel line that names the victim.

sudo journalctl -k | grep -iE 'oom|killed process'
# journalctl -k      → kernel messages via the journal (same as dmesg, but persistent).

sudo journalctl -k --since '1 hour ago' | less
# --since '1 hour ago' → context around the event.
# less               → paged reading.
```

Key kernel line:
`Out of memory: Killed process 1234 (myapp) total-vm:...kB, anon-rss:...kB, ...`

**Prevent recurrence:**

- Add `MemoryHigh` / `MemoryMax` to the systemd unit.
- Add swap (scenario 14).
- `vm.overcommit_memory=2` + tuned ratio if you'd rather have malloc fail than a random kill.
- Fix the leak.

---

## 20. Zombie processes — what and why 🎓

**Symptom.** `ps aux` shows processes with state `Z`, command `[foo] <defunct>`.

**Explanation.** A zombie has already exited; the parent hasn't called `wait()` to reap it. It holds no memory or CPU — only a PID slot.

```bash
ps -eo pid,ppid,stat,cmd | awk '$3 ~ /^Z/'
# ps -eo …           → PID, parent PID, state, command.
# awk '$3 ~ /^Z/'    → third column starts with Z (zombie).

ps -eo pid,ppid,stat,cmd | awk '$3 ~ /^Z/ {print $2}' | sort -u
# $2                 → parent PID column.
# sort -u            → deduplicate → unique parents responsible for zombies.
```

**Fix.** You cannot kill a zombie (already dead). Kill the **parent** so init (`PID 1`) inherits and reaps them:

```bash
sudo kill -CHLD <PPID>
# kill -CHLD         → send SIGCHLD to the parent — sometimes wakes it into calling wait().

sudo kill <PPID>
# → last resort: kill the parent so init reaps the zombies.
```

Common cause: shell scripts that spawn background children without `wait`. Fix by adding `wait` or `trap 'wait' CHLD`.

---

## 21. Fork bomb defense with ulimit 🎓

The classic bomb:

```bash
:(){ :|:& };:
# :()  →  define a function named ":".
# { :|:& }  →  its body pipes itself into itself, backgrounded.
# ;:   →  call it.
# → doubles processes exponentially until the system dies.
```

Defend by capping per-user processes:

```bash
ulimit -u 200
# ulimit -u          → max user processes (for the CURRENT shell + descendants).

# System-wide, PAM-enforced at login:
# /etc/security/limits.d/50-forkbomb.conf
#   *   soft   nproc   1024
#   *   hard   nproc   2048

ulimit -a
# -a                 → dump every limit currently in effect.

cat /proc/<PID>/limits
# → shows per-process kernel-enforced limits (read-only).
```

---

## 22. "Site is down" — end-to-end triage 🔥

Work outward from the app:

```bash
# 1. Is the process alive?
systemctl status nginx
pgrep -a nginx || echo 'nginx not running'
# pgrep -a nginx     → PIDs + cmdline of matching procs. || echo prints only if pgrep found none.

# 2. Is it listening?
sudo ss -tulpn | grep -E ':(80|443)\b'
# ss -tulpn          → tcp+udp+listen+numeric+with PID.
# grep -E ':(80|443)\b' → port 80 or 443, word-boundary end (avoids :8080).

# 3. Is it accepting locally?
curl -kI https://127.0.0.1/
# curl -k            → insecure — don't verify TLS cert (loopback often has self-signed).
# -I                 → HEAD request → returns just headers.

# 4. Is DNS pointing here?
dig +short mysite.example.com A
# dig +short         → just the answer records.
# A                  → IPv4 record type.

# 5. Is the network path open?
sudo iptables -L -n -v | head
sudo ufw status
# iptables -L        → list rules.
# -n                 → numeric (no DNS reverse lookups → faster).
# -v                 → verbose (packet counters).

# from an external box:
nc -zv mysite.example.com 443
# nc -z              → scan for open port — don't send data.
# -v                 → verbose.

# 6. Any recent errors?
sudo tail -n 200 /var/log/nginx/error.log
journalctl -u nginx --since '10 min ago'
# --since <time>     → filter by time window.

# 7. Certificate expired?
echo | openssl s_client -servername mysite.example.com -connect mysite.example.com:443 2>/dev/null \
    | openssl x509 -noout -dates
# echo               → provide empty stdin so s_client exits after handshake.
# -servername        → SNI hostname for TLS.
# openssl x509 -noout -dates → print notBefore / notAfter of the leaf cert.
```

**Golden rule:** prove each hop works before assuming the next one.

---

## 23. Find which process owns port 8080 🛠️

```bash
sudo ss -tulpn | grep :8080
# ss                 → modern socket stats.
# -t                 → TCP.
# -u                 → UDP.
# -l                 → listening only.
# -p                 → include owning process/PID.
# -n                 → don't resolve port names / hosts.

sudo lsof -i :8080
# lsof -i :N         → files matching Internet address filter on port N.

sudo fuser -n tcp 8080
# fuser              → identify processes using resources.
# -n tcp 8080        → namespace tcp, port 8080.
```

Kill it (polite → forced):

```bash
sudo fuser -k -TERM -n tcp 8080
# -k                 → KILL — send signal.
# -TERM              → SIGTERM (polite).

sleep 3

sudo fuser -k -KILL -n tcp 8080
# -KILL              → SIGKILL (last resort).
```

---

## 24. DNS resolves differently than expected 🔥

```bash
dig example.com A
# → what the system resolver returns.

dig @8.8.8.8 example.com A
# @8.8.8.8           → ask Google's public DNS specifically.
# → compare with the system answer to see if a local resolver is lying to you.

getent hosts example.com
# getent hosts       → uses the same lookup path (nsswitch) that libc uses.
#                      This is what most applications actually see.

cat /etc/hosts
# local static overrides — a stale entry here can hijack a name.

cat /etc/nsswitch.conf | grep ^hosts
# → order of lookup sources (`files dns mdns` etc.).

cat /etc/resolv.conf
# → currently-active resolvers. Often managed by systemd-resolved or NetworkManager.

resolvectl status
# → per-interface DNS on systemd-resolved boxes.

resolvectl query example.com
# → same lookup path as an app, showing which interface answered.
```

**Usual culprits.** VPN pushed a bogus search domain; `systemd-resolved` cache is stale (`sudo resolvectl flush-caches`); Docker/WSL/podman DNS overlay in front.

---

## 25. Capture a specific request with tcpdump 🔥

```bash
sudo tcpdump -i any -A -s0 'tcp port 80' -c 20
# tcpdump            → packet capture.
# -i any             → any interface.
# -A                 → print payload as ASCII.
# -s0                → snapshot length 0 → capture entire packet (not truncated).
# 'tcp port 80'      → BPF filter.
# -c 20              → stop after 20 packets.

sudo tcpdump -i eth0 -w /tmp/client.pcap host 10.1.2.3
# -w <file>          → write raw pcap for later analysis (Wireshark, tshark).
# host 10.1.2.3      → BPF filter — traffic to/from that IP.

sudo tcpdump -r /tmp/client.pcap -nn 'tcp port 443 and host 10.1.2.3'
# -r <file>          → read a saved pcap.
# -nn                → no name resolution (faster + deterministic).
# extra filter       → re-filter the pcap for a subset.
```

Copy the pcap out for graphical inspection:

```bash
scp server:/tmp/client.pcap .
# scp                → SSH-based copy from server to current dir.
```

---

## 26. Set up an SSH bastion / jump host workflow 🛠️

`~/.ssh/config` on your laptop:

```
Host bastion
    HostName bastion.example.com
    User alice
    IdentityFile ~/.ssh/id_ed25519

Host internal-*
    User alice
    IdentityFile ~/.ssh/id_ed25519
    ProxyJump bastion

# Host bastion       → alias you'll use on the CLI.
# HostName …         → real DNS name.
# User …             → default user for this host.
# IdentityFile …     → which private key to try.
# ProxyJump bastion  → transparently open a session THROUGH `bastion`.
```

Now `ssh internal-db01` hops through `bastion` automatically. Nothing on the internal net needs a public IP.

Multiplex to avoid repeated auth:

```
Host *
    ControlMaster auto
    ControlPath   ~/.ssh/cm-%r@%h:%p
    ControlPersist 10m

# ControlMaster auto → reuse an existing connection if one is open.
# ControlPath …      → socket path; %r=user %h=host %p=port.
# ControlPersist 10m → keep master alive 10 min after last client disconnects.
```

---

## 27. Reach a private service through an SSH tunnel 🛠️

Forward a private DB port to your laptop:

```bash
ssh -L 15432:db01.internal:5432 alice@bastion
# -L LOCAL_PORT:REMOTE_HOST:REMOTE_PORT
#     forward laptop:15432 → (via bastion) → db01.internal:5432.

psql -h 127.0.0.1 -p 15432 -U app mydb
# psql               → PostgreSQL client.
# -h 127.0.0.1       → connect to the local end of the tunnel.
# -p 15432           → the tunnel port.
# -U app             → connect as user `app`.
# mydb               → database name.
```

Expose a local dev server to the remote host:

```bash
ssh -R 9000:localhost:3000 alice@remote
# -R REMOTE_PORT:LOCAL_HOST:LOCAL_PORT
#     forward remote:9000 → laptop:3000 (reverse direction of -L).
```

SOCKS proxy for a whole browser:

```bash
ssh -D 1080 alice@bastion
# -D                 → dynamic SOCKS forwarding on the given local port.
# → point your browser's SOCKS proxy at 127.0.0.1:1080.
```

---

## 28. Grep an error out of a compressed, rotated log set 🛠️

```bash
zgrep -H 'connection reset' /var/log/app.log*
# zgrep              → grep across gzipped AND plain files transparently.
# -H                 → print filename before each match.

zgrep -B2 -A5 'connection reset' /var/log/app.log*.gz | less
# -B2 -A5            → 2 lines before, 5 lines after each match (context window).

rg -z 'connection reset' /var/log/app.log*
# rg                 → ripgrep — same idea, much faster.
# -z                 → also search inside gzip/xz/bz2 files.
```

Per-day error count:

```bash
zcat /var/log/app.log*.gz /var/log/app.log |
    awk '/ERROR/ {print $1}' | sort | uniq -c | sort -k2
# zcat …             → decompress-and-print in order.
# awk '/ERROR/ {print $1}' → date field of every ERROR line.
# sort | uniq -c     → group and count identical lines.
# sort -k2           → sort by the date column ascending.
```

---

## 29. Top 10 error-generating clients in an access log 🛠️

nginx-style combined log:

```bash
awk '$9 >= 500 {print $1}' /var/log/nginx/access.log |
    sort | uniq -c | sort -rn | head
# $9                 → HTTP status code column in the "combined" format.
# >= 500             → server errors only.
# $1                 → remote IP column.
# sort | uniq -c     → group identical IPs, count.
# sort -rn           → reverse numeric — highest count first.
# head               → top 10.
```

Top 10 URLs returning 4xx:

```bash
awk '$9 ~ /^4/ {print $7}' /var/log/nginx/access.log |
    sort | uniq -c | sort -rn | head
# $9 ~ /^4/          → status code starts with 4 (any 4xx).
# $7                 → request URI column.
```

Requests per minute:

```bash
awk '{print substr($4,2,17)}' /var/log/nginx/access.log |
    sort | uniq -c | tail
# $4                 → "[dd/Mon/yyyy:HH:MM:SS" field.
# substr(...,2,17)   → strip leading '[' and truncate to minute precision.
```

---

## 30. Schedule a daily backup with cron and rotate output 🛠️

```bash
sudo tee /usr/local/bin/db-backup.sh >/dev/null <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
STAMP=$(date +%F)
OUT=/var/backups/db/mydb-$STAMP.sql.gz
mkdir -p "$(dirname "$OUT")"
pg_dumpall -U postgres | gzip > "$OUT"
find /var/backups/db -type f -mtime +14 -delete
EOF
# tee >/dev/null <<'EOF' … EOF → write a here-doc into the target file quietly.
# set -euo pipefail       → strict script mode.
# STAMP=$(date +%F)        → YYYY-MM-DD tag.
# pg_dumpall | gzip > OUT  → stream logical backup straight to a compressed file.
# find … -mtime +14 -delete → prune anything older than 14 days.

sudo chmod +x /usr/local/bin/db-backup.sh
# chmod +x           → make the script executable.

echo '15 2 * * *  root  /usr/local/bin/db-backup.sh >>/var/log/db-backup.log 2>&1' \
    | sudo tee /etc/cron.d/db-backup
# cron time         → 02:15 every day.
# user column       → run as root (only used for /etc/cron.d, not user crontabs).
# >>…log 2>&1       → append stdout AND stderr to the log.
```

**Verify.**

```bash
sudo run-parts --test /etc/cron.daily
# run-parts --test   → print what WOULD run under /etc/cron.daily (no execution).

sudo /usr/local/bin/db-backup.sh
# manual smoke test.

ls -lh /var/backups/db/
# confirm the .sql.gz appeared.
```

---

## 31. Set up log rotation for a custom app 🛠️

```
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily              # rotate every day.
    rotate 14          # keep 14 rotated versions.
    compress           # gzip old rotations.
    delaycompress      # keep yesterday's rotation uncompressed for easy tailing.
    missingok          # don't error if no log file is present.
    notifempty         # skip rotation if the file is empty.
    create 0640 myapp adm   # after rotation, recreate the file with these perms/owner.
    postrotate
        systemctl kill -s HUP myapp.service >/dev/null 2>&1 || true
        # systemctl kill -s HUP → send SIGHUP so the app reopens its log file.
        # || true              → ignore failure (e.g. service not running).
    endscript
}
```

Force a test run:

```bash
sudo logrotate -d /etc/logrotate.d/myapp
# -d                 → debug + DRY RUN (no changes, just prints what it would do).

sudo logrotate -f /etc/logrotate.d/myapp
# -f                 → FORCE — rotate even if the "big enough / old enough" check would skip.
```

**When to use `copytruncate`** instead of `HUP`: when the app can't be signalled to reopen its log file (some Java apps, container-in-container setups). Downside: brief race window where log lines can be lost.

---

## 32. Convert a shell-script daemon into a systemd service 🛠️

Script (`/opt/myapp/bin/server`):

```bash
#!/usr/bin/env bash
exec /opt/myapp/bin/real-binary --config /etc/myapp/config.yml
# exec …             → replace the shell with the real binary → keeps PID stable.
```

Unit file:

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My App                              # human-readable label.
After=network-online.target                     # start AFTER network is up.
Wants=network-online.target                     # explicitly pull network-online in.

[Service]
Type=simple                                     # ExecStart runs in foreground.
User=myapp                                      # drop privileges to this user.
Group=myapp
EnvironmentFile=-/etc/default/myapp             # `-` = OK if the file is missing.
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/server --config /etc/myapp/config.yml
Restart=on-failure                              # respawn on non-zero exit only.
RestartSec=5s                                   # wait 5s between restarts.
LimitNOFILE=65536                               # raise max open files.
# sandboxing:
NoNewPrivileges=true                            # child procs can't setuid.
ProtectSystem=strict                            # / read-only for the service.
ProtectHome=true                                # /home hidden.
ReadWritePaths=/var/lib/myapp /var/log/myapp    # whitelisted writable paths.
PrivateTmp=true                                 # per-service /tmp.

[Install]
WantedBy=multi-user.target                      # enable target so it starts at boot.
```

```bash
sudo systemctl daemon-reload
# daemon-reload      → tell systemd to re-scan unit files.

sudo systemctl enable --now myapp
# --now              → enable at boot AND start right now.

systemctl status myapp
journalctl -u myapp -f
# → verify + live-tail logs.
```

---

## 33. Investigate a slow boot 🛠️

```bash
systemd-analyze
# → total boot time + firmware/loader/kernel/userspace breakdown.

systemd-analyze blame | head
# blame              → each unit's activation time, slowest first.

systemd-analyze critical-chain
# → dependency chain that gates the fastest possible boot.

systemd-analyze plot > /tmp/boot.svg
# plot               → SVG timeline. scp it to your laptop and open in a browser.

journalctl -b -p err
# -b                 → this boot.
# -p err             → priority ≤ err (severe messages).

journalctl -b -1
# -1                 → the PREVIOUS boot (compare with today's).
```

Usual suspects: `NetworkManager-wait-online.service`, `apt-daily-upgrade`, `cloud-init` waiting on slow metadata endpoints.

---

## 34. Service keeps restarting — debug the loop 🔥

```bash
systemctl status myapp
# → recent Main PID exits + last few journal lines.

sudo journalctl -u myapp -n 200 --no-pager
# -n 200             → last 200 lines.
# --no-pager         → straight to stdout (no `less`).

sudo journalctl -u myapp --since '10 min ago' -o cat
# -o cat             → just the message text (no timestamps/units).

systemctl show myapp | grep -E 'Restart|NRestarts|ActiveState'
# systemctl show     → machine-readable properties (KEY=VALUE).
# NRestarts          → how many times it's respawned since load.
```

Stop the auto-restart while you debug:

```bash
sudo systemctl edit myapp
# → opens an override snippet. Add:
#     [Service]
#     Restart=no

sudo systemctl daemon-reload
sudo systemctl restart myapp
# reproduce the crash cleanly, then revert.
```

---

## 35. Detect a brute-force SSH attempt 🔥

```bash
sudo grep 'Failed password' /var/log/auth.log |
    awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head
# grep 'Failed password' → sshd failure lines.
# awk '{print $(NF-3)}' → field 4 from the RIGHT — the source IP in a typical sshd log line.
# sort | uniq -c        → group by IP + count.
# sort -rn | head       → top offenders.

# RHEL / CentOS:
sudo grep 'Failed password' /var/log/secure | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head
```

Quick temporary block via iptables:

```bash
sudo iptables -A INPUT -s 1.2.3.4 -j DROP
# -A INPUT           → append to the INPUT chain.
# -s 1.2.3.4         → source IP.
# -j DROP            → silently drop packets (they see a hang, not a rejection).
```

Long-term: install `fail2ban` — watches the same lines, bans automatically, un-bans after a cooldown.

---

## 36. Find world-writable files and SUID binaries 🛠️

```bash
sudo find / -xdev -type f -perm -0002 -not -path '/proc/*' 2>/dev/null
# find /             → walk the root.
# -xdev              → don't cross into other filesystems.
# -type f            → regular files.
# -perm -0002        → the "other-writable" bit is set.
# -not -path '/proc/*' → skip proc noise.
# 2>/dev/null        → hide permission-denied warnings.

sudo find / -xdev -type f -perm -4000 2>/dev/null
# -perm -4000        → setuid bit set → runs as OWNER regardless of caller.

sudo find / -xdev -type f -perm -2000 2>/dev/null
# -perm -2000        → setgid bit set.

sudo find / -xdev \( -nouser -o -nogroup \) 2>/dev/null
# -nouser            → owner UID doesn't map to any /etc/passwd entry (deleted user leftovers).
# -nogroup           → same for group.
# \( … -o … \)       → grouped OR.
```

---

## 37. Audit what a user can `sudo` 🛠️

```bash
sudo -l -U alice
# -l                 → list allowed sudo commands.
# -U alice           → for THIS user (not you).

sudo cat /etc/sudoers
# master sudoers file.

sudo ls   /etc/sudoers.d/
# drop-in dir — each file has its own rules.

sudo cat  /etc/sudoers.d/*
# concatenated view of every drop-in.

sudo grep -rE '^\s*[^#]' /etc/sudoers /etc/sudoers.d/
# grep -r            → recurse.
# -E                 → extended regex.
# '^\s*[^#]'         → skip comment-only lines and blank lines.
```

Red flags to look for:

- `NOPASSWD: ALL`.
- Wildcards in command paths.
- `!requiretty` combined with `!authenticate`.
- Group entries like `%wheel ALL=(ALL) NOPASSWD:ALL`.
- Editors on the allow-list (`/usr/bin/vi`) — shell escape from inside vim.

---

## 38. Make `/etc/resolv.conf` tamper-resistant 🛠️

```bash
sudo cp /etc/resolv.conf /etc/resolv.conf.bak
# cp                 → straight file copy for backup.

# edit /etc/resolv.conf to the DNS servers you want, then:
sudo chattr +i /etc/resolv.conf
# chattr +i          → set the "immutable" attribute. Even root can't edit/delete/rename
#                      until the flag is removed.

# undo:
sudo chattr -i /etc/resolv.conf
```

Long-term (correct) fix: configure the DHCP client or `systemd-resolved` so nothing keeps rewriting the file.

---

## 39. Replace a config value across many files atomically 🛠️

```bash
grep -RIn 'timeout: 30' src/
# grep -R            → recurse into subdirs.
# -I                 → skip binary files.
# -n                 → include line numbers.
# → preview matches before editing.

sed -i.bak 's/timeout: 30/timeout: 60/g' $(grep -RIl 'timeout: 30' src/)
# grep -RIl          → list ONLY filenames containing the pattern (no lines).
# $(…)               → command substitution → pass those filenames to sed.
# sed -i.bak         → in-place edit, leaves .bak backup per file.
# 's/A/B/g'          → substitute all occurrences per line.

grep -R 'timeout:' src/ | grep -v \\.bak
# → verify: show current values, hiding the backup files.

find src -name '*.bak' -delete
# once you're happy, remove backups.
```

If the tree is a git repo, prefer restricting sed to tracked files:

```bash
git ls-files -z | xargs -0 sed -i 's/timeout: 30/timeout: 60/g'
# git ls-files -z    → tracked files, NUL-separated.
# xargs -0           → NUL-safe pass to sed.
```

---

## 40. Sum the 5th column, group by the 2nd, for a big TSV 🛠️

```bash
awk -F'\t' 'NR>1 {sum[$2]+=$5} END {for (k in sum) print k"\t"sum[k]}' data.tsv |
    sort -k2 -nr | head
# awk -F'\t'         → tab-separated input.
# NR>1               → skip header row.
# sum[$2]+=$5        → accumulate col 5 into an associative array keyed by col 2.
# END { for … print} → after reading all lines, dump the totals.
# sort -k2 -nr | head → biggest groups first.
```

With `datamash` (if installed):

```bash
datamash -H -t$'\t' groupby 2 sum 5 < data.tsv | sort -k2 -nr | head
# datamash           → dedicated aggregation tool.
# -H                 → input HAS a header.
# -t$'\t'            → field separator = tab.
# groupby 2 sum 5    → group by column 2, sum column 5.
```

---

## 41. Extract every URL from a JSON payload with jq 🛠️

```bash
jq -r '.. | .url? // empty' payload.json | sort -u
# jq -r              → raw output (no quotes around strings).
# ..                 → recursive descent — visit every node in the JSON tree.
# .url?              → the `.url` field if present (`?` suppresses errors).
# // empty           → default: emit nothing when null/absent.
# sort -u            → dedupe.

jq -r '.items[].url' payload.json
# → for a KNOWN shape: iterate .items, extract .url from each.

jq -r '.. | strings | select(startswith("http"))' payload.json | sort -u
# strings            → keep only string values.
# select(startswith("http")) → keep only http/https-looking strings.
```

---

## 42. Hard link vs symbolic link 🎓

|  | Hard link (`ln target link`) | Symlink (`ln -s target link`) |
|---|---|---|
| Points to | Same **inode**. | A **path string**. |
| Survives target rename? | Yes. | No — dangles. |
| Cross-filesystem? | No. | Yes. |
| To a directory? | Only root, and inadvisable. | Yes, everyday tool. |
| `ls -l` marker | Looks like a normal file. | `l` at the start, `-> target`. |

Demo:

```bash
echo hi > a
# > a                → create file `a` with content "hi".

ln    a  hard
# ln                 → HARD link. `hard` and `a` share the same inode.

ln -s a  soft
# ln -s              → SYMBOLIC (soft) link. `soft` stores the string "a".

ls -li
# -l                 → long listing.
# -i                 → show inode number (first column).
# → `hard` and `a` share an inode number; `soft` has its own.

mv a a.moved
# rename the target.

cat hard              # → still prints "hi" (inode unchanged).
cat soft              # → ENOENT: symlink still points to path "a" which no longer exists.
```

---

## 43. What is an inode? 🎓

An **inode** is the filesystem's metadata record for a file: owner, group, perms, timestamps, size, block pointers. It does NOT contain the filename — the name lives in a directory entry that maps `name → inode number`.

Consequences:

- Rename doesn't change the inode; only the directory entry does.
- Deleting a file removes one link to its inode. The inode is only freed when link count → 0 AND no process holds the file open.
- Running out of inodes can make a disk "full" with GB of bytes still free (`df -i`).

Poke at it:

```bash
stat file
# stat               → per-inode dump (mode, uid, size, atime/mtime/ctime, inode #).

ls -li file
# -i                 → prepend the inode number.

df -i
# df -i              → inode usage per filesystem.
```

---

## 44. Process vs thread 🎓

- **Process** — own address space, own FD table, own PID.
- **Thread** — shares address space, FDs, and PID with siblings; owns its own stack, registers, TID.
- On Linux both are created by `clone()`; the flags decide what's shared.

Observe threads:

```bash
ps -eLf | grep myapp
# ps -e              → all processes.
# -L                 → one row PER THREAD.
# -f                 → full format.

ps -o pid,tid,psr,pcpu,comm -T -p <PID>
# -o …               → custom columns (pid, tid, running CPU, cpu %, name).
# -T                 → threads of the given PID.
# -p <PID>           → the process.

top -H -p <PID>
# -H                 → threads mode.
# -p <PID>           → only this process.

ls /proc/<PID>/task/
# → one directory per thread; each looks like a mini /proc/<TID>.
```

---

## 45. Foreground vs background vs daemon 🎓

- **Foreground.** Attached to the controlling terminal; receives Ctrl-C.
- **Background** (`cmd &`). Detached from terminal input; still a child of the shell — dies when the shell exits (unless `disown` or `nohup`).
- **Daemon.** No controlling terminal at all; adopted by `init`/`systemd`.
  Classic recipe: `fork` → `setsid` → `fork` → chdir `/` → close FDs → reopen stdin/out/err on `/dev/null`. Modern answer: let `systemd` do it (`Type=simple`).

---

## 46. `/etc/passwd` vs `/etc/shadow` 🎓

- `/etc/passwd` — world-readable, 7 fields per line:
  `username:x:UID:GID:GECOS:home:shell`. The `x` is a placeholder; the real password hash is NOT here.
- `/etc/shadow` — readable only by root:
  `username:hash:lastchange:min:max:warn:inactive:expire:reserved`.
  Hash prefix identifies the algorithm: `$6$` = SHA-512, `$y$` = yescrypt, `$2b$` = bcrypt.

```bash
head -1 /etc/passwd
# → world-readable format.

sudo head -1 /etc/shadow
# → root-only format.
```

---

## 47. What happens when you type `ls` and press Enter? 🎓

1. Shell reads the line, tokenises it, expands aliases/globs/variables.
2. Shell calls `fork()` → a child process is created.
3. Child calls `execve("/usr/bin/ls", ["ls"], envp)` — its process image is replaced by the `ls` binary.
4. Kernel loads the ELF; the dynamic linker (`ld-linux.so`) resolves shared libs (`libc`, etc.).
5. `ls` calls `getdents64()` on the current directory's FD, formats output, writes to FD 1 (stdout, your tty).
6. `ls` calls `_exit(status)`.
7. Kernel wakes the parent shell (blocked in `wait4()`); shell reaps the child, prints the next prompt.

If stdout were a pipe instead of a tty, `ls` skips column layout and colour because `isatty(1) == 0`.

---

## 48. SIGTERM vs SIGKILL vs SIGHUP 🎓

| Signal | Number | Catchable? | Typical use |
|---|---|---|---|
| `SIGTERM` | 15 | Yes | Polite shutdown; default of `kill`. |
| `SIGKILL` | 9  | **No** | Force-kill; no cleanup; last resort. |
| `SIGHUP`  | 1  | Yes | Historically "hang up"; many daemons treat as reload. |
| `SIGINT`  | 2  | Yes | Ctrl-C. |
| `SIGSTOP` | 19 | **No** | Pause (Ctrl-Z sends `SIGTSTP` which IS catchable). |
| `SIGCONT` | 18 | Yes | Continue after stop. |

Rule of thumb: `kill <PID>` first → wait 5–10 s → `kill -9 <PID>` only if it's truly stuck.

---

## 49. `>` vs `>>` vs `2>&1` vs `&>` 🎓

```bash
cmd >  out            # stdout → out (TRUNCATE).
cmd >> out            # stdout → out (APPEND).
cmd 2> err            # stderr → err.
cmd > out 2> err      # split streams.
cmd > out 2>&1        # merge stderr into stdout AFTER redirecting stdout.
cmd &> out            # bash shortcut: BOTH streams → out (truncate).
cmd &>> out           # BOTH streams → out (append).
cmd > /dev/null 2>&1  # swallow everything.
cmd 2>&1 > out        # ⚠️ WRONG ORDER — sends stderr to OLD stdout (terminal),
                      #     then stdout to `out`. Order matters!
```

`2>&1` means "make FD 2 a copy of whatever FD 1 currently points at" — so its position on the line changes the meaning.

---

## 50. `chmod 644` vs `chmod u=rw,go=r` — same thing? 🎓

Same effective permission bits (`rw-r--r--`), but two subtleties:

- Numeric form is **absolute** and overwrites ALL bits, INCLUDING special bits (setuid/setgid/sticky). `chmod 644 file` clears them.
- Symbolic form can be relative (`+`, `-`) or absolute (`=`). `chmod u=rw,go=r file` is absolute only for the classes it names, and leaves special bits untouched.

Demo:

```bash
touch demo && chmod 4755 demo && ls -l demo
# 4755                → setuid + rwxr-xr-x.

chmod 644 demo && ls -l demo
# → setuid GONE (numeric = absolute for ALL bits).

chmod 4755 demo && chmod u=rw,go=r demo && ls -l demo
# → rw-r--r-- (bits changed) but setuid STILL SET.
```

---

## Where to go next

- Practice inside the sandbox: `docker run -it --rm linux-practice`.
- Print [linux-commands.md](linux-commands.md) and [scenarios.md](scenarios.md); annotate as you work.
- Rebuild the image any time you want a clean slate — the container is disposable by design.

