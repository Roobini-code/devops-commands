# Linux Command Reference — Basic to Advanced

Every section is a `Command → What it does` table. Same layout front to back
so you can grep it, print it, or read it end-to-end.

> Convention: `#` prompt = must be root · `$` prompt = normal user is fine.
> Replace anything in `<angle brackets>` with your real value.

---

## Table of contents

1. [Shell survival kit](#1-shell-survival-kit)
2. [Filesystem navigation](#2-filesystem-navigation)
3. [File & directory operations](#3-file--directory-operations)
4. [Reading & viewing files](#4-reading--viewing-files)
5. [Permissions, ownership, ACLs](#5-permissions-ownership-acls)
6. [Text processing — grep, sed, awk, cut, sort, uniq](#6-text-processing)
7. [Searching for files & content](#7-searching-for-files--content)
8. [Users, groups, sudo](#8-users-groups-sudo)
9. [Processes & job control](#9-processes--job-control)
10. [Memory, CPU, load](#10-memory-cpu-load)
11. [Disks, partitions, filesystems, LVM](#11-disks-partitions-filesystems-lvm)
12. [Networking](#12-networking)
13. [Package management](#13-package-management)
14. [Archives & compression](#14-archives--compression)
15. [Redirection, pipes, subshells](#15-redirection-pipes-subshells)
16. [Environment variables & shell config](#16-environment-variables--shell-config)
17. [Scheduling — cron, at, systemd timers](#17-scheduling)
18. [Services — systemd, journalctl](#18-services--systemd-journalctl)
19. [Logs & log rotation](#19-logs--log-rotation)
20. [SSH, SCP, rsync](#20-ssh-scp-rsync)
21. [Performance & tracing](#21-performance--tracing)
22. [Kernel & boot](#22-kernel--boot)
23. [Security hygiene](#23-security-hygiene)
24. [Shell scripting essentials](#24-shell-scripting-essentials)
25. [Bonus one-liners](#25-bonus-one-liners)

---

## 1. Shell survival kit

| Command | What it does |
|---|---|
| `whoami` | Prints the current username. |
| `id` | Shows your UID, primary GID, and all secondary group memberships. |
| `hostname` | Prints the machine's short hostname. |
| `hostname -I` | Prints every IPv4/IPv6 address bound to this host. |
| `uname -a` | Kernel name, hostname, kernel version, architecture — all in one line. |
| `uptime` | How long since boot plus 1/5/15-minute load averages. |
| `date` | Current local date/time. |
| `date -u` | Current UTC date/time. |
| `cal` | This month's calendar. |
| `history` | List previously-run commands from `~/.bash_history`. |
| `!n` | Re-runs command number `n` from `history`. |
| `!!` | Re-runs the previous command (great as `sudo !!`). |
| `Ctrl-R` | Interactive reverse search of history — type to filter. |
| `clear` / `Ctrl-L` | Clears the visible terminal buffer. |
| `man <cmd>` | Opens the manual page for `<cmd>`. |
| `<cmd> --help` | Short, one-screen usage summary (most GNU tools). |
| `type <cmd>` | Tells you if `<cmd>` is a builtin, alias, function, or file. |
| `which <cmd>` | Prints the first match for `<cmd>` in `$PATH`. |
| `whereis <cmd>` | Prints binary, source, and man-page paths for `<cmd>`. |
| `exit` / `Ctrl-D` | Leaves the current shell. |

---

## 2. Filesystem navigation

| Command | What it does |
|---|---|
| `pwd` | Prints the current working directory (absolute path). |
| `cd /var/log` | Jumps to that absolute path. |
| `cd ../etc` | Moves relatively — up one, then into `etc`. |
| `cd -` | Jumps back to the previous directory (toggle). |
| `cd ~` (or just `cd`) | Jumps to your home directory. |
| `pushd /tmp` | Pushes the current dir onto the stack and cd's to `/tmp`. |
| `popd` | Pops the top of the stack and cd's back to it. |
| `dirs -v` | Prints the current directory stack, one per line. |
| `ls` | Lists files in the current directory (names only). |
| `ls -l` | Long listing — mode, links, owner, group, size, mtime, name. |
| `ls -lah` | Long + all (including dotfiles) + human-readable sizes. |
| `ls -lt` | Long listing sorted by mtime, newest first. |
| `ls -lS` | Long listing sorted by size, largest first. |
| `ls -laR /etc` | Recursive long listing of `/etc`. |
| `tree -L 2 /etc` | Visual tree of `/etc`, limited to 2 levels deep. |

### Filesystem Hierarchy Standard (FHS)

| Path | Contents |
|---|---|
| `/bin`, `/sbin`, `/usr/bin`, `/usr/sbin` | System binaries (common vs. admin). |
| `/etc` | System-wide configuration files. |
| `/home/<user>` | Regular users' home directories. |
| `/root` | The `root` user's home. |
| `/var/log` | Log files. |
| `/var/lib` | Persistent state written by daemons (databases, package DBs). |
| `/tmp`, `/var/tmp` | Temp files (`/tmp` is usually wiped on reboot). |
| `/opt` | Third-party or manually installed software. |
| `/srv` | Data served by this host (websites, FTP, etc.). |
| `/proc` | Virtual FS — kernel + per-process info. |
| `/sys` | Virtual FS — kernel objects (devices, tunables). |
| `/dev` | Device nodes (block, character). |
| `/boot` | Kernel, initramfs, GRUB. |
| `/mnt`, `/media` | Mount points for temporary and removable media. |

---

## 3. File & directory operations

| Command | What it does |
|---|---|
| `touch file.txt` | Creates the file if missing; otherwise updates its mtime. |
| `mkdir dir` | Creates a directory. |
| `mkdir -p a/b/c` | Creates the whole path, no error if pieces already exist. |
| `cp src dst` | Copies a single file. |
| `cp -r srcdir dstdir` | Copies a directory tree recursively. |
| `cp -a srcdir dstdir` | Archive copy — preserves perms, timestamps, and symlinks. |
| `mv old new` | Renames or moves a file/dir. |
| `rm file` | Deletes a file. |
| `rm -r dir` | Recursively deletes a directory. **Danger.** |
| `rm -rf /path` | Recursive, force, no prompt. **Serious danger.** |
| `rmdir dir` | Deletes a directory only if it's empty. |
| `ln -s /target /link` | Creates a symbolic (soft) link pointing to `/target`. |
| `ln     /target /link` | Creates a hard link — same inode, same content. |
| `readlink -f /link` | Resolves any chain of symlinks and prints the real path. |
| `stat file` | Shows inode, size, mode, atime/mtime/ctime, links. |
| `file file` | Reports the file type based on magic bytes (not extension). |
| `truncate -s 0 big.log` | Truncates the file to zero bytes in place. |
| `truncate -s 10M new.bin` | Creates a sparse file exactly 10 MiB long. |
| `install -m 0644 src /etc/x.conf` | Copies + sets mode/owner in one step (safer than `cp`+`chmod`). |
| `shred -u secret` | Overwrites the file then deletes it (best-effort — worthless on SSDs). |

Defensive delete idiom:

```bash
rm -rf -- "${TARGET:?refuse to run with unset TARGET}"
# The :? blocks the command if TARGET is empty or unset.
```

---

## 4. Reading & viewing files

| Command | What it does |
|---|---|
| `cat file` | Dumps the whole file to stdout. |
| `cat -n file` | Same, but with line numbers. |
| `tac file` | Dumps the file line-reversed. |
| `less file` | Interactive pager: `q` quit, `/` search, `n`/`N` next/prev. |
| `less +F file` | Like `tail -f` but you can `Ctrl-C` back to browsing. |
| `more file` | Simpler pager (space to page, `q` to quit). |
| `head file` | First 10 lines. |
| `head -n 50 file` | First 50 lines. |
| `tail file` | Last 10 lines. |
| `tail -n 100 file` | Last 100 lines. |
| `tail -f file` | Follows the file — new appends appear live. Ctrl-C stops. |
| `tail -F file` | Like `-f` but also reopens the file if it rotates. |
| `wc -l file` | Counts lines. |
| `wc -w file` | Counts words. |
| `wc -c file` | Counts bytes. |
| `md5sum file` | MD5 checksum. |
| `sha256sum file` | SHA-256 checksum (preferred). |
| `diff a b` | Line-by-line difference. |
| `diff -u a b` | Unified diff — same format `patch` reads. |
| `cmp a b` | Byte-by-byte compare, stops at first difference. |
| `xxd file` | Hex dump with ASCII sidebar. |
| `hexdump -C file` | Canonical hex + ASCII (BSD-flavoured). |

### Reading compressed files without touching disk

| Command | What it does |
|---|---|
| `zcat  app.log.gz` | Streams the decompressed contents of a gzip file. |
| `bzcat app.log.bz2` | Same for bzip2. |
| `xzcat app.log.xz` | Same for xz. |
| `zgrep ERROR app.log.gz` | Runs `grep` directly against gzipped file(s). |
| `zless app.log.gz` | Interactive `less` over a gzipped file. |

---

## 5. Permissions, ownership, ACLs

### 5.1 How to read a mode line

```
-rwxr-xr--   1 alice devs  1234 Aug  8 10:00 script.sh
 └┬┘└┬┘└┬┘   │  │     │
  u  g  o    │  │     │
             │  │     └─ group name
             │  └─────── owner name
             └────────── link count
```

`r=4  w=2  x=1`, applied per class (user / group / other). Numeric `755`
= user `rwx` (7) + group `r-x` (5) + other `r-x` (5).

### 5.2 Common permission commands

| Command | What it does |
|---|---|
| `chmod 755 script.sh` | Sets mode to `rwxr-xr-x` (numeric, absolute). |
| `chmod u+x,g-w,o= file` | Adds/removes bits symbolically per class. |
| `chmod -R g+rw dir` | Recursively grants group read+write. |
| `chown alice:devs file` | Changes owner to `alice`, group to `devs`. |
| `chown -R alice:devs dir` | Same, recursive. |
| `chgrp devs file` | Changes only the group. |
| `umask` | Prints your current default mask. |
| `umask 022` | New files default to `644`, new dirs to `755`. |
| `namei -mo /path/to/file` | Walks every component of the path and prints its perms. |

### 5.3 Special bits

| Bit | Number | Symbol | What it does |
|---|---|---|---|
| setuid | 4000 | `s` in user-x | Binary runs as its **owner** (e.g. `passwd`). |
| setgid | 2000 | `s` in group-x | Binary runs as its **group**; on a dir, new files inherit the dir's group. |
| sticky | 1000 | `t` in other-x | Only the file's owner can delete it (used on `/tmp`). |

| Command | What it does |
|---|---|
| `chmod 4755 /usr/bin/mytool` | Sets setuid + `rwxr-xr-x`. |
| `chmod 2775 /srv/shared` | Sets setgid on a group-writable dir. |
| `chmod 1777 /tmp` | Sets the sticky bit (world-writable but delete-protected). |

### 5.4 POSIX ACLs (fine-grained)

| Command | What it does |
|---|---|
| `getfacl file` | Shows ACL entries on the file. |
| `setfacl -m u:bob:rw file` | Grants user `bob` read+write in addition to base perms. |
| `setfacl -m g:auditors:r file` | Grants group `auditors` read. |
| `setfacl -x u:bob file` | Removes bob's ACL entry. |
| `setfacl -b file` | Strips all extended ACL entries. |
| `setfacl -Rdm g:devs:rwx dir` | Sets **default** ACL — inherited by new files under `dir`. |

### 5.5 Extended attributes / immutability

| Command | What it does |
|---|---|
| `lsattr file` | Lists ext[234]/xfs extended attributes. |
| `chattr +i file` | Marks file immutable — even root can't modify or delete. |
| `chattr -i file` | Removes the immutable flag. |
| `chattr +a file` | Append-only (useful for log files). |
| `getfattr -d file` | Dumps all user-space extended attributes. |

---

## 6. Text processing

### 6.1 grep

| Command | What it does |
|---|---|
| `grep pattern file` | Prints lines matching `pattern`. |
| `grep -i pattern file` | Case-insensitive match. |
| `grep -v pattern file` | Inverts match — prints lines that do NOT match. |
| `grep -n pattern file` | Prefixes each hit with its line number. |
| `grep -c pattern file` | Prints only the count of matching lines. |
| `grep -r pattern .` | Recurses through the tree. |
| `grep -R --include='*.py' pattern .` | Recurse but only look inside `*.py`. |
| `grep -E 'foo|bar' file` | Extended regex (alternation without escaping). |
| `grep -P '\d+ms' file` | Perl-style regex (needs pcre build). |
| `grep -A3 -B3 pattern file` | 3 lines of context After and Before each hit. |
| `grep -o 'ERROR .*' file` | Prints only the matching part, not the whole line. |
| `grep -l pattern *.log` | Prints only the filenames that contain a match. |
| `grep -L pattern *.log` | Prints only the filenames that did NOT match. |
| `grep -q pattern file` | Quiet — sets exit code, no output (great for `if`). |
| `rg pattern` | ripgrep — faster grep, respects `.gitignore` by default. |

### 6.2 sed (stream editor)

| Command | What it does |
|---|---|
| `sed -n '10,20p' file` | Prints only lines 10 through 20. |
| `sed 's/foo/bar/' file` | Replaces the FIRST `foo` on each line with `bar`. |
| `sed 's/foo/bar/g' file` | Replaces ALL `foo` on each line (global). |
| `sed -i 's/foo/bar/g' file` | Edits the file in place. |
| `sed -i.bak 's/foo/bar/g' file` | In-place edit AND keeps `file.bak` backup. |
| `sed '/pattern/d' file` | Deletes every line matching `pattern`. |
| `sed '2i\HEADER' file` | Inserts `HEADER` before line 2. |
| `sed '$a\FOOTER' file` | Appends `FOOTER` after the last line. |
| `sed -e 's/A/1/' -e 's/B/2/' file` | Chains multiple expressions. |
| `sed -n 's/.*id=\([0-9]*\).*/\1/p' file` | Extracts a capture group and prints only it. |

### 6.3 awk

| Command | What it does |
|---|---|
| `awk '{print $1}' file` | Prints the first whitespace-separated column of each line. |
| `awk -F: '{print $1, $3}' /etc/passwd` | Uses `:` as field separator; prints columns 1 and 3. |
| `awk 'NR==5' file` | Prints line 5. |
| `awk 'NR>1 && $3>1000' file` | Skips header row and filters where column 3 > 1000. |
| `awk '/ERROR/ {c++} END {print c}' app.log` | Counts lines matching `/ERROR/`. |
| `awk '{sum+=$1} END {print sum/NR}' nums` | Prints the average of column 1. |
| `awk 'length($0)>200' file` | Prints lines longer than 200 chars. |
| `awk -F, 'NR>1 {s[$2]+=$5} END {for (k in s) print k, s[k]}' data.csv` | Group-by-sum per column-2 key. |
| `awk 'seen[$0]++' file` | Prints only duplicate lines. |
| `awk '!seen[$0]++' file` | Removes duplicate lines while preserving order. |

### 6.4 cut / paste / tr / column

| Command | What it does |
|---|---|
| `cut -d: -f1,3 /etc/passwd` | Prints columns 1 and 3 using `:` as the delimiter. |
| `cut -c1-10 file` | Prints characters 1..10 of each line. |
| `paste a b` | Merges files side by side, one line each (tab-separated). |
| `paste -d, a b` | Same but comma-separated. |
| `tr 'a-z' 'A-Z' < file` | Translates every lowercase char to uppercase. |
| `tr -d '\r' < win.txt` | Deletes carriage returns (Windows → Unix line endings). |
| `tr -s ' '` | Squeezes runs of spaces down to one. |
| `column -t file` | Reformats whitespace-separated columns into an aligned table. |

### 6.5 sort / uniq / wc / tee

| Command | What it does |
|---|---|
| `sort file` | Sorts lexicographically ascending. |
| `sort -r file` | Descending order. |
| `sort -n file` | Numeric sort. |
| `sort -h file` | Sort by human-readable sizes (`1K`, `5M`, `2G`). |
| `sort -k2,2 -n file` | Sort by column 2 numerically. |
| `sort -u file` | Sort AND deduplicate. |
| `uniq -c file` | Prefixes each line with its occurrence count (needs pre-sorted input). |
| `sort file | uniq -c | sort -rn` | The classic "top-N" frequency histogram. |
| `sort file | uniq -d` | Prints only lines that are duplicated. |
| `wc -l file` | Line count. |
| `cmd | tee out.log` | Pipes stdout through `tee` — screen AND file. |
| `cmd | tee -a out.log` | Same but appends to the file. |
| `cmd | tee >(gzip > out.gz)` | Bash process substitution — pipe into a second command as if it were a file. |

### 6.6 jq / yq (JSON / YAML)

| Command | What it does |
|---|---|
| `jq '.' file.json` | Pretty-prints JSON. |
| `jq '.items[].name' file.json` | Extracts `.name` from every element of `.items`. |
| `jq -r '.token' file.json` | `-r` = raw output (no surrounding quotes). |
| `jq 'select(.level=="error")' events.json` | Filters objects where `.level == "error"`. |
| `jq '.[] | {name, age}'` | Rebuilds each element with only two fields. |
| `jq -s 'add' *.json` | Slurps multiple files into an array and adds them. |
| `yq '.metadata.name' deploy.yaml` | Same as `jq`, but for YAML. |
| `yq -o=json . deploy.yaml` | Converts YAML to JSON. |

---

## 7. Searching for files & content

| Command | What it does |
|---|---|
| `find /var/log -name '*.log'` | Finds files matching a shell pattern. |
| `find . -type f -size +100M` | Files larger than 100 MiB. |
| `find . -type f -mtime +30` | Files whose mtime is more than 30 days old. |
| `find . -type f -mtime -1` | Files modified in the last 24h. |
| `find . -type d -empty` | Empty directories. |
| `find . -type f -perm 0777` | World-writable AND world-executable files (weird — audit). |
| `find . -type f -user alice` | Files owned by `alice`. |
| `find . -type f -name '*.tmp' -delete` | Deletes them in place. |
| `find . -type f -name '*.log' -exec gzip {} \;` | Runs `gzip` once per match. |
| `find . -type f -name '*.log' -exec gzip {} +` | Runs `gzip` once for a batch (much faster). |
| `find . -type f -print0 | xargs -0 grep -l ERROR` | Null-delimited handoff — safe for weird filenames. |
| `locate nginx.conf` | Instant name search from the `updatedb` DB (may be stale). |
| `sudo updatedb` | Rebuilds `locate`'s database. |
| `which python3` | First `python3` in `$PATH`. |
| `whereis python3` | Binary, source, and man-page locations. |
| `type -a ls` | Shows every definition of `ls` — alias, builtin, and file. |
| `fd -e py test` | ripgrep-style `find` alternative (Rust). |

---

## 8. Users, groups, sudo

### 8.1 Read the system

| Command | What it does |
|---|---|
| `cat /etc/passwd` | `username:x:UID:GID:GECOS:home:shell` — user records. |
| `cat /etc/group` | `group:x:GID:members` — group records. |
| `sudo cat /etc/shadow` | Hashed passwords (root-only). |
| `sudo cat /etc/sudoers` | Master sudoers file. |
| `ls /etc/sudoers.d/` | Drop-in sudoers snippets. |
| `getent passwd alice` | User record for `alice` (respects LDAP/AD too). |
| `getent group devs` | Group record for `devs`. |
| `who` | Who is logged in right now. |
| `w` | Who + what command they're running + load average. |
| `last` | Login history (from `wtmp`). |
| `sudo lastb` | Failed login attempts (from `btmp`). |
| `finger alice` | (If installed) shows a user's basic info + login times. |

### 8.2 Create, modify, delete users & groups

| Command | What it does |
|---|---|
| `sudo useradd -m -s /bin/bash alice` | Creates `alice`, creates her home dir, sets login shell to bash. |
| `sudo passwd alice` | Sets/changes alice's password (interactive). |
| `echo 'alice:s3cret' | sudo chpasswd` | Sets alice's password in one line (batch). |
| `sudo usermod -aG docker alice` | **APPENDS** `docker` to alice's group memberships. Always use `-aG`. |
| `sudo usermod -L alice` | Locks the account (password can't be used). |
| `sudo usermod -U alice` | Unlocks it. |
| `sudo chsh -s /bin/zsh alice` | Changes alice's login shell. |
| `sudo chage -l alice` | Prints password aging info for alice. |
| `sudo chage -M 90 -W 14 alice` | Max age 90 days, warn 14 days before expiry. |
| `sudo chage -d 0 alice` | Forces password change on next login. |
| `sudo userdel -r alice` | Deletes alice AND her home directory. |
| `sudo groupadd devs` | Creates the `devs` group. |
| `sudo groupdel devs` | Deletes it. |
| `sudo gpasswd -d alice devs` | Removes alice from `devs` without touching her other groups. |

### 8.3 sudo

| Command | What it does |
|---|---|
| `sudo cmd` | Runs `cmd` as root. |
| `sudo -i` | Starts an interactive root login shell. |
| `sudo -u alice cmd` | Runs `cmd` as `alice`. |
| `sudo -l` | Shows what YOU are allowed to run via sudo. |
| `sudo -l -U alice` | Same, for another user. |
| `sudo visudo` | Edits `/etc/sudoers` safely (syntax-checked before save). |
| `sudo visudo -f /etc/sudoers.d/alice` | Same, but into a drop-in file. |

Sudoers snippet examples:

```
# Passwordless full root:
alice   ALL=(ALL)  NOPASSWD:ALL

# Only allow alice to restart nginx as root:
alice   ALL=(root) NOPASSWD:/bin/systemctl restart nginx
```

---

## 9. Processes & job control

### 9.1 Inspect

| Command | What it does |
|---|---|
| `ps` | Shows YOUR shell's processes. |
| `ps -ef` | Every process, full-format columns (System V flags). |
| `ps auxf` | Every process, forest view (BSD flags). |
| `ps -eo pid,ppid,user,stat,pcpu,pmem,cmd --sort=-pcpu | head` | Top 10 by CPU, custom columns. |
| `pgrep -a nginx` | Prints PIDs (with command line) matching `nginx`. |
| `pgrep -u alice` | Every PID owned by `alice`. |
| `pidof sshd` | Just the PIDs of `sshd`. |
| `top` | Live process table (q quit, P sort by CPU, M by memory). |
| `htop` | Nicer `top` — F5 tree, F9 kill, mouse support. |
| `atop` | Historical + live snapshots including disk and network per process. |

### 9.2 Signal / kill

| Command | What it does |
|---|---|
| `kill <PID>` | Sends `SIGTERM` (polite shutdown). |
| `kill -9 <PID>` | Sends `SIGKILL` — process cannot catch this. |
| `kill -HUP <PID>` | Sends `SIGHUP` — many daemons treat this as "reload config". |
| `killall nginx` | Sends signal to every process named `nginx`. |
| `pkill -f 'python.*worker'` | Matches against the FULL command line (not just process name). |
| `fuser -k -TERM -n tcp 8080` | Kills whatever process holds TCP port 8080. |

### 9.3 Priority

| Command | What it does |
|---|---|
| `nice -n 10 heavy_job` | Starts `heavy_job` with a niceness of +10 (lower priority). |
| `renice +10 -p <PID>` | Changes an already-running process's niceness. |
| `ionice -c 3 -p <PID>` | Puts a process in the I/O idle class (yields to everyone). |
| `chrt -f 50 cmd` | Runs `cmd` under real-time FIFO scheduler with priority 50 (needs root). |

### 9.4 Foreground / background / detach

| Command | What it does |
|---|---|
| `long_job &` | Starts `long_job` in the background. |
| `jobs` | Lists background jobs of this shell. |
| `fg %1` | Brings job 1 back to the foreground. |
| `bg %1` | Resumes a stopped job in the background. |
| `disown %1` | Detaches a job from the shell — survives shell logout. |
| `nohup ./job >out 2>&1 &` | Detached AND immune to `SIGHUP`. |
| `Ctrl-Z` | Suspends the foreground job (`SIGTSTP`). |

### 9.5 Poke around per-process

| Command | What it does |
|---|---|
| `ls -l /proc/<PID>/exe` | Symlink to the binary that was launched. |
| `cat /proc/<PID>/cmdline | tr '\0' ' '` | The original command line, arg by arg. |
| `cat /proc/<PID>/status` | Human-readable snapshot: threads, memory, capabilities, state. |
| `ls -l /proc/<PID>/fd/` | Every file descriptor the process has open. |
| `lsof -p <PID>` | Same info but formatted, with file type per fd. |
| `ss -tulpn` | Every listening TCP/UDP socket with owning PID. |

### 9.6 Signal cheat sheet

| Number | Name | Meaning |
|---|---|---|
| 1 | SIGHUP  | Hang up — many daemons reload their config. |
| 2 | SIGINT  | Ctrl-C. |
| 3 | SIGQUIT | Ctrl-\ — writes core dump on exit. |
| 9 | SIGKILL | Uncatchable, unblockable. Last resort. |
| 15 | SIGTERM | Polite ask to terminate (default of `kill`). |
| 17 | SIGCHLD | A child changed state. |
| 18 | SIGCONT | Continue (partner of SIGSTOP). |
| 19 | SIGSTOP | Pause — uncatchable. |

---

## 10. Memory, CPU, load

| Command | What it does |
|---|---|
| `free -h` | Total, used, free, buff/cache, swap — human-readable units. |
| `vmstat 1 5` | Every 1s for 5 samples: runnable/blocked queues, swap, IO, CPU %. |
| `uptime` | Load averages over 1/5/15 minutes. |
| `mpstat -P ALL 1` | Per-CPU utilisation (sysstat package). |
| `sar -u 1 5` | Historical CPU stats — depends on the sar collector. |
| `iostat -xz 1` | Per-device I/O with utilisation, await, service time. |
| `pidstat 1` | Per-process CPU/memory/IO refreshed every second. |
| `lscpu` | CPU model, socket count, cores per socket, threads per core, caches. |
| `nproc` | Number of usable CPUs (respects cgroup limits inside containers). |
| `cat /proc/cpuinfo` | Raw per-thread CPU data. |
| `cat /proc/meminfo` | Every memory statistic the kernel tracks. |
| `sudo dmidecode -t memory` | Physical DIMM slots and speeds (real hosts only). |
| `numactl --hardware` | NUMA topology on multi-socket hosts. |

Load averages = average number of runnable + uninterruptible-sleep tasks over
1/5/15 minutes. On an 8-CPU host a load of 8 = fully busy; 16 = ~2× oversubscribed.

---

## 11. Disks, partitions, filesystems, LVM

### 11.1 Inspect

| Command | What it does |
|---|---|
| `lsblk` | Block-device tree: disks → partitions → mounts. |
| `blkid` | Prints UUID and filesystem type of every block device. |
| `df -hT` | Mounted filesystems with type, sizes, use %. |
| `df -i` | Inodes used vs. free (a filesystem can be full on inodes with GB unused). |
| `du -sh *` | Size per item in current directory (recursive). |
| `du -sh -x /var/* 2>/dev/null | sort -h` | Sorted size per direct child of `/var`, staying on one filesystem. |
| `ncdu /` | Interactive drill-down disk-usage explorer. |
| `mount` | Prints every currently mounted filesystem. |
| `findmnt /var` | Shows where `/var` is mounted (source, options). |
| `cat /etc/fstab` | Persistent mounts read at boot. |

### 11.2 Mount / unmount / partition (dangerous)

| Command | What it does |
|---|---|
| `sudo mount -t ext4 /dev/sdb1 /mnt/data` | Mounts `/dev/sdb1` on `/mnt/data`. |
| `sudo umount /mnt/data` | Unmounts. |
| `sudo mount -a` | Mounts everything listed in `/etc/fstab`. |
| `sudo fdisk /dev/sdb` | Interactive MBR partition editor. |
| `sudo parted /dev/sdb` | Interactive GPT editor. |
| `sudo mkfs.ext4 /dev/sdb1` | Formats as ext4. |
| `sudo mkfs.xfs /dev/sdb1` | Formats as xfs. |
| `sudo tune2fs -l /dev/sdb1` | Prints ext[234] superblock params (label, UUID, mount count). |
| `sudo xfs_info /mnt/data` | XFS equivalent. |

### 11.3 Swap

| Command | What it does |
|---|---|
| `sudo fallocate -l 2G /swapfile` | Creates a 2 GiB file for swap. |
| `sudo chmod 600 /swapfile` | Restricts perms (kernel refuses otherwise). |
| `sudo mkswap /swapfile` | Formats it as swap. |
| `sudo swapon /swapfile` | Activates it. |
| `swapon --show` | Lists active swap devices/files. |

### 11.4 LVM

| Command | What it does |
|---|---|
| `sudo pvcreate /dev/sdb1` | Marks the partition as an LVM physical volume. |
| `sudo vgcreate data-vg /dev/sdb1` | Creates a volume group named `data-vg`. |
| `sudo lvcreate -L 10G -n app-lv data-vg` | Creates a 10 GiB logical volume `app-lv`. |
| `sudo mkfs.ext4 /dev/data-vg/app-lv` | Puts a filesystem on it. |
| `sudo lvextend -L +5G /dev/data-vg/app-lv` | Grows the LV by 5 GiB. |
| `sudo resize2fs /dev/data-vg/app-lv` | Grows an ext4 filesystem to fill the LV. |
| `sudo xfs_growfs /mnt/data` | Grows an XFS filesystem (takes the MOUNT point). |
| `sudo pvs`, `vgs`, `lvs` | One-line summaries of PVs / VGs / LVs. |

### 11.5 The "df says full, du says empty" fix

| Command | What it does |
|---|---|
| `sudo lsof +L1` | Lists every file with link-count 0 — deleted but still open. |
| `sudo bash -c ': > /proc/<PID>/fd/<N>'` | Truncates the still-open deleted file to free its blocks. |

---

## 12. Networking

### 12.1 Interfaces & routing

| Command | What it does |
|---|---|
| `ip a` | Every interface + its addresses. |
| `ip -br a` | Brief, one-line-per-interface. |
| `ip r` | The routing table. |
| `ip -s link` | Per-interface counters (rx/tx bytes, errors). |
| `sudo ip link set eth0 up` | Brings the interface up. |
| `sudo ip addr add 10.0.0.5/24 dev eth0` | Adds an address to the interface. |
| `sudo ip route add default via 10.0.0.1` | Sets the default gateway. |
| `ifconfig` | Legacy interface tool — still on many older boxes. |
| `route -n` | Legacy routing table. |

### 12.2 DNS

| Command | What it does |
|---|---|
| `dig example.com` | Full DNS response (headers, answers, authority). |
| `dig +short example.com A` | Just the answer records. |
| `dig @8.8.8.8 example.com` | Ask a specific resolver instead of `/etc/resolv.conf`. |
| `dig -x 1.1.1.1` | Reverse lookup (PTR). |
| `host example.com` | Terse "is it resolvable" tool. |
| `nslookup example.com` | Interactive legacy resolver. |
| `getent hosts example.com` | Uses the same lookup path a normal program would (nsswitch). |
| `cat /etc/resolv.conf` | Currently active resolver list. |
| `cat /etc/nsswitch.conf` | Order of hostname sources (files, dns, mdns…). |
| `cat /etc/hosts` | Local static hostname → IP overrides. |
| `resolvectl status` | Per-interface DNS config on systemd-resolved boxes. |
| `resolvectl flush-caches` | Clears the systemd-resolved DNS cache. |

### 12.3 Connectivity & path

| Command | What it does |
|---|---|
| `ping -c 4 example.com` | Sends 4 ICMP echos. |
| `mtr example.com` | Live-updating traceroute + ping combined. |
| `traceroute example.com` | Route each hop takes to reach the host. |
| `tracepath example.com` | Same idea, no root needed. |

### 12.4 Ports & sockets

| Command | What it does |
|---|---|
| `ss -tulpn` | TCP + UDP + listening + numeric + PID. Modern replacement for netstat. |
| `ss -tan state established` | Established TCP connections. |
| `ss -s` | One-line summary of socket counts by state. |
| `netstat -tulpn` | Legacy equivalent of `ss -tulpn`. |
| `sudo lsof -i :80` | Everything using port 80. |
| `sudo lsof -iTCP -sTCP:LISTEN` | Every TCP listening socket. |

### 12.5 HTTP & TCP

| Command | What it does |
|---|---|
| `curl https://example.com` | GET the URL, print body. |
| `curl -I https://example.com` | HEAD request — headers only. |
| `curl -v https://example.com` | Verbose: TLS handshake + all request/response headers. |
| `curl -sSL -o out.bin https://.../file` | Silent + show errors + follow redirects + write to file. |
| `curl -X POST -H 'Content-Type: application/json' -d '{"a":1}' URL` | JSON POST. |
| `curl --resolve api.local:443:10.0.0.5 https://api.local/` | Hard-code DNS for this call (bypass real DNS). |
| `wget -c https://.../file` | Downloads with resume support. |
| `nc -zv host 22` | TCP port-open probe (no data sent). |
| `nc -l 9999` | Listen on port 9999. |
| `nc host 9999 < file` | Sends the file over TCP. |
| `telnet host 25` | Opens a raw TCP connection — useful for banner checks. |
| `openssl s_client -connect host:443 -servername host` | TLS handshake, print certificate, keep connection open. |

### 12.6 Packet capture

| Command | What it does |
|---|---|
| `sudo tcpdump -i any port 80 -c 20` | Captures first 20 packets on port 80, any interface. |
| `sudo tcpdump -i eth0 -w cap.pcap host 10.0.0.5` | Writes a pcap file, filtering by host. |
| `sudo tcpdump -r cap.pcap -nn` | Reads a pcap back, no name resolution. |
| `sudo nmap -sT -p 22,80,443 host` | TCP connect scan of listed ports. |

### 12.7 Firewall

| Command | What it does |
|---|---|
| `sudo iptables -L -n -v` | Prints current iptables ruleset with counters. |
| `sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT` | Appends a rule allowing inbound SSH. |
| `sudo iptables -D INPUT -p tcp --dport 22 -j ACCEPT` | Deletes that same rule. |
| `sudo iptables -F` | Flushes ALL rules (dangerous — you can lock yourself out). |
| `sudo nft list ruleset` | Prints current nftables ruleset. |
| `sudo ufw status` | Prints ufw state and rules. |
| `sudo ufw allow 22/tcp` | Allows inbound SSH via ufw. |
| `sudo ufw deny from 10.1.2.3` | Blocks a source IP. |
| `sudo ufw enable` | Turns ufw on at boot. |

---

## 13. Package management

### Debian / Ubuntu

| Command | What it does |
|---|---|
| `sudo apt update` | Refreshes package indexes. |
| `sudo apt upgrade` | Upgrades installed packages. |
| `sudo apt install nginx` | Installs `nginx`. |
| `sudo apt remove nginx` | Removes the binary but keeps config. |
| `sudo apt purge nginx` | Removes binary AND config. |
| `sudo apt autoremove` | Removes packages installed as deps that nothing needs any more. |
| `apt search nginx` | Searches package index by name/description. |
| `apt show nginx` | Detailed metadata for a package. |
| `apt list --installed | grep nginx` | Installed packages matching a name. |
| `dpkg -l | grep nginx` | Same, using dpkg's low-level DB. |
| `dpkg -L nginx` | Every file installed by `nginx`. |
| `dpkg -S /usr/sbin/nginx` | Which package owns a given file. |
| `sudo dpkg -i pkg.deb` | Installs a downloaded `.deb`. |

### RHEL / Fedora / Rocky / Alma

| Command | What it does |
|---|---|
| `sudo dnf install nginx` | Installs. |
| `sudo dnf remove nginx` | Removes. |
| `sudo dnf update` | Upgrades. |
| `dnf search nginx` | Searches. |
| `dnf info nginx` | Metadata. |
| `rpm -qa | grep nginx` | Installed packages by name. |
| `rpm -ql nginx` | Files installed by a package. |
| `rpm -qf /usr/sbin/nginx` | Which package owns a file. |
| `sudo rpm -ivh pkg.rpm` | Installs a downloaded `.rpm`. |

---

## 14. Archives & compression

### tar

| Command | What it does |
|---|---|
| `tar -cf out.tar dir/` | Creates an uncompressed tar of `dir/`. |
| `tar -czf out.tgz dir/` | Creates a gzip-compressed tar. |
| `tar -cjf out.tbz2 dir/` | Bzip2-compressed. |
| `tar -cJf out.txz dir/` | Xz-compressed. |
| `tar -tf out.tgz` | Lists archive contents without extracting. |
| `tar -xf out.tgz` | Extracts (auto-detects compression). |
| `tar -xzvf out.tgz -C /opt/` | Extract verbosely into `/opt/`. |
| `tar -czf - dir | ssh host 'tar -xzf - -C /dest'` | Stream a tar over ssh — no temp file. |

### Raw compressors

| Command | What it does |
|---|---|
| `gzip file` | Compresses to `file.gz` (removes original). |
| `gzip -k file` | Compresses and keeps original. |
| `gunzip file.gz` | Decompresses. |
| `bzip2 file` / `bunzip2 file.bz2` | Bzip2 pair. |
| `xz file` / `unxz file.xz` | Xz pair. |

### zip / 7z

| Command | What it does |
|---|---|
| `zip -r out.zip dir/` | Recursive zip. |
| `unzip out.zip` | Extracts a zip. |
| `unzip -l out.zip` | Lists archive contents. |
| `7z a out.7z dir/` | Creates a 7z archive. |
| `7z x out.7z` | Extracts a 7z archive. |

---

## 15. Redirection, pipes, subshells

| Command | What it does |
|---|---|
| `cmd > out.txt` | Writes stdout to `out.txt`, TRUNCATING it first. |
| `cmd >> out.txt` | Writes stdout to `out.txt`, APPENDING. |
| `cmd 2> err.txt` | Writes stderr (fd 2) to `err.txt`. |
| `cmd &> both.txt` | Bash shortcut — stdout AND stderr into one file. |
| `cmd > out 2>&1` | Portable equivalent of `&>` — send stdout to `out`, then dup stderr to point at the same place. |
| `cmd 2>&1 > out` | **WRONG ORDER** — stderr goes to the OLD stdout (terminal), then stdout goes to `out`. Ordering matters. |
| `cmd < input.txt` | Feeds `input.txt` as stdin. |
| `cmd1 | cmd2` | Pipes stdout of `cmd1` into stdin of `cmd2`. |
| `cmd1 |& cmd2` | Pipes stdout AND stderr. |
| `cmd1 && cmd2` | Runs `cmd2` only if `cmd1` succeeded (exit 0). |
| `cmd1 || cmd2` | Runs `cmd2` only if `cmd1` failed (non-zero). |
| `cmd1 ; cmd2` | Runs both, regardless of the first's exit. |
| `$(cmd)` | Command substitution — replaced by cmd's stdout. |
| `<(cmd)` | Process substitution — cmd's stdout appears as a filename (bash/zsh). |
| `diff <(sort a) <(sort b)` | Diffs two commands' output without temp files. |
| `cmd | tee -a log` | Splits stdout so it goes to screen AND a log. |
| `cmd > /dev/null 2>&1` | Discards ALL output. |

Exit-code idioms:

| Snippet | What it does |
|---|---|
| `cmd ; echo "exit=$?"` | Prints the exit code of the previous command. |
| `if grep -q pat f; then echo yes; fi` | Uses `-q` to suppress output and just check success. |
| `set -e` (in a script) | Aborts the script on the first non-zero exit. |

---

## 16. Environment variables & shell config

| Command | What it does |
|---|---|
| `echo $HOME $PATH $SHELL $USER` | Prints those variables. |
| `env` | Prints every exported environment variable. |
| `printenv PATH` | Prints one specific variable's value. |
| `export MYVAR=value` | Exports for THIS shell AND its children. |
| `unset MYVAR` | Removes the variable. |
| `readonly PI=3.14` | Sets and marks read-only. |
| `declare -p MYVAR` | Shows the variable's attributes and value. |

Per-user startup files (bash):

| File | When it's read |
|---|---|
| `~/.bash_profile` | Login shells (once at login). |
| `~/.bashrc` | Interactive non-login shells (every new terminal tab). |
| `~/.profile` | POSIX-style login shells (bash falls back to it if there's no `.bash_profile`). |
| `~/.bash_logout` | On logout. |

System-wide:

| File | Purpose |
|---|---|
| `/etc/profile` | System-wide login-shell setup. |
| `/etc/profile.d/*.sh` | Drop-in scripts sourced by `/etc/profile`. |
| `/etc/bash.bashrc` | System-wide interactive-shell setup (Debian/Ubuntu). |
| `/etc/environment` | Simple `KEY=VALUE` pairs, no shell syntax — read by PAM. |

Add a dir to `PATH` persistently:

```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
```

---

## 17. Scheduling

### cron

| Command | What it does |
|---|---|
| `crontab -l` | Lists your current crontab. |
| `crontab -e` | Opens your crontab in `$EDITOR`, syntax-checked on save. |
| `sudo crontab -l -u alice` | Lists another user's crontab. |
| `sudo cat /etc/crontab` | System-wide crontab. |
| `ls /etc/cron.{hourly,daily,weekly,monthly}` | Drop-in dirs that run their scripts on schedule. |
| `sudo systemctl status cron` | Is the cron daemon running? |

Cron time syntax:

```
# ┌─── minute        (0-59)
# │ ┌─ hour          (0-23)
# │ │ ┌─ day of month (1-31)
# │ │ │ ┌─ month      (1-12)
# │ │ │ │ ┌─ day of week (0-6, 0=Sun)
# * * * * * command

*/5 * * * *   /usr/local/bin/health-check     # every 5 minutes
0 2 * * *     /usr/local/bin/backup.sh        # daily at 02:00
0 3 * * 0     /usr/local/bin/weekly.sh        # Sunday at 03:00
@reboot       /usr/local/bin/on-boot.sh       # once at boot
```

### at (one-shot)

| Command | What it does |
|---|---|
| `echo 'reboot' | sudo at 03:00 tomorrow` | Schedules a one-off command. |
| `atq` | Lists pending `at` jobs. |
| `atrm <id>` | Removes a queued job. |

### systemd timers

Unit + timer pair:

```
# /etc/systemd/system/backup.service
[Service]
ExecStart=/usr/local/bin/backup.sh

# /etc/systemd/system/backup.timer
[Timer]
OnCalendar=daily
Persistent=true
[Install]
WantedBy=timers.target
```

| Command | What it does |
|---|---|
| `sudo systemctl daemon-reload` | Re-reads unit files after edits. |
| `sudo systemctl enable --now backup.timer` | Enables at boot AND starts immediately. |
| `systemctl list-timers` | Every timer + its next / last run. |

---

## 18. Services — systemd, journalctl

### systemctl

| Command | What it does |
|---|---|
| `systemctl status nginx` | Current state, recent logs, main PID. |
| `sudo systemctl start nginx` | Starts the service. |
| `sudo systemctl stop nginx` | Stops it. |
| `sudo systemctl restart nginx` | Stops then starts. |
| `sudo systemctl reload nginx` | Sends the service a reload signal (SIGHUP-style) — no downtime. |
| `sudo systemctl enable nginx` | Adds symlinks so it starts on boot. |
| `sudo systemctl disable nginx` | Removes those symlinks. |
| `sudo systemctl mask nginx` | Aliases the unit to `/dev/null` — prevents anyone from ever starting it. |
| `sudo systemctl unmask nginx` | Reverses `mask`. |
| `systemctl is-active nginx` | Prints `active`/`inactive` + exits with matching code. |
| `systemctl is-enabled nginx` | Enabled at boot? |
| `systemctl list-units --type=service` | Every service unit currently loaded. |
| `systemctl list-units --state=failed` | Just the ones in failed state. |
| `systemctl show nginx | grep -E 'MainPID|ActiveState|SubState'` | Machine-readable properties. |
| `sudo systemctl edit nginx` | Creates an override snippet under `/etc/systemd/system/nginx.service.d/`. |

Unit-file template:

```
# /etc/systemd/system/myapp.service
[Unit]
Description=My App
After=network.target

[Service]
Type=simple
User=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/server
Restart=on-failure
RestartSec=5s
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

### journalctl

| Command | What it does |
|---|---|
| `journalctl -u nginx` | All logs for one unit. |
| `journalctl -u nginx -f` | Follow live (like `tail -f`). |
| `journalctl -u nginx --since '10 min ago'` | Time-window query. |
| `journalctl -u nginx --since today` | Today's logs only. |
| `journalctl -u nginx -p err` | Priority ≤ err. |
| `journalctl _PID=1234` | Every log line emitted by PID 1234. |
| `journalctl -k` | Kernel messages only (equivalent of `dmesg`). |
| `journalctl --disk-usage` | Space consumed by the journal. |
| `sudo journalctl --vacuum-time=7d` | Trims the journal to the last 7 days. |
| `journalctl -b` | Logs for this boot. |
| `journalctl -b -1` | Logs for the previous boot. |

---

## 19. Logs & log rotation

| Command | What it does |
|---|---|
| `ls /var/log/` | Overview of the log tree. |
| `tail -f /var/log/syslog` | Live-tail the system log. |
| `sudo dmesg -T | tail` | Kernel ring buffer with human timestamps. |
| `sudo dmesg -w` | Follow kernel messages live. |
| `sudo tail -f /var/log/{syslog,auth.log}` | Multi-file follow — one interleaved stream. |

logrotate config lives in `/etc/logrotate.d/`. Example:

```
/var/log/myapp/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
    postrotate
        systemctl reload myapp >/dev/null 2>&1 || true
    endscript
}
```

| Command | What it does |
|---|---|
| `sudo logrotate -d /etc/logrotate.d/myapp` | Dry-run + debug output. |
| `sudo logrotate -f /etc/logrotate.d/myapp` | Forces a rotation right now. |
| `sudo cat /var/lib/logrotate/status` | Timestamps of the last rotation per file. |

---

## 20. SSH, SCP, rsync

### ssh basics

| Command | What it does |
|---|---|
| `ssh user@host` | Opens an interactive shell. |
| `ssh -p 2222 user@host` | Non-default port. |
| `ssh -i ~/.ssh/id_ed25519 user@host` | Specific private key. |
| `ssh -J bastion user@internal-host` | Jumps through `bastion` to reach `internal-host`. |
| `ssh -L 8080:localhost:80 user@host` | Local port forward — laptop:8080 → host:80. |
| `ssh -R 9000:localhost:9000 user@host` | Remote port forward — host:9000 → laptop:9000. |
| `ssh -D 1080 user@host` | Opens a SOCKS proxy on your laptop. |
| `ssh -N -f -L …` | Sets up a tunnel and forks into the background. |
| `ssh -v user@host` | Verbose — great for auth debugging. |

### keys

| Command | What it does |
|---|---|
| `ssh-keygen -t ed25519 -C "alice@laptop"` | Generates a modern key pair. |
| `ssh-copy-id user@host` | Uploads your public key to `~user/.ssh/authorized_keys` on `host`. |
| `eval "$(ssh-agent -s)"` | Starts an agent in this shell. |
| `ssh-add ~/.ssh/id_ed25519` | Loads the key into the agent (asks for passphrase once). |
| `ssh-add -l` | Lists loaded keys. |

`~/.ssh/config` snippet:

```
Host prod
    HostName 10.0.0.5
    User deploy
    Port 2222
    IdentityFile ~/.ssh/prod_ed25519
    ForwardAgent yes
```

### scp / rsync

| Command | What it does |
|---|---|
| `scp file user@host:/tmp/` | Copies one file up. |
| `scp -r dir user@host:/tmp/` | Recursive. |
| `scp user@host:/tmp/file .` | Copies one file down. |
| `rsync -avh --progress src/ user@host:/dest/` | Efficient tree sync — only changed blocks travel. Trailing `/` matters. |
| `rsync -avh --delete src/ user@host:/dest/` | Mirrors — extras on dest are removed. |
| `rsync -avhn src/ user@host:/dest/` | Dry-run — shows what would change. |
| `rsync -avh -e 'ssh -p 2222' src/ user@host:/dest/` | Non-default SSH port. |

---

## 21. Performance & tracing

| Command | What it does |
|---|---|
| `top` / `htop` / `atop` | Live process-level CPU/mem. |
| `vmstat 1` | Runnable/blocked, swap in/out, CPU %. |
| `iostat -xz 1` | Per-device I/O: `%util`, `await`, `r/s`, `w/s`. |
| `mpstat -P ALL 1` | Per-CPU utilisation. |
| `pidstat -u 1` | Per-process CPU. |
| `pidstat -d 1` | Per-process disk I/O. |
| `sar -u -r -n DEV 1 5` | Historical CPU/mem/network — needs the sar collector. |
| `iotop` | Per-process I/O rates (needs root). |
| `iftop` | Per-connection bandwidth (needs root). |
| `nethogs` | Per-process bandwidth. |
| `lsof` | Every open file/socket on the system. |
| `lsof -p <PID>` | For one process. |
| `lsof -i :443` | For one port. |
| `lsof +D /var/lib/mysql` | Everything open under a directory. |
| `strace -p <PID>` | Live syscall trace of a process. |
| `strace -e openat,read,write -f cmd` | Trace `cmd`, follow forks, filter to a few syscalls. |
| `ltrace -p <PID>` | Library-call trace. |
| `perf top` | Sampling profiler — top hot functions. |
| `perf record -F 99 -a -g -- sleep 30` | Records a 30-second system-wide profile. |
| `perf report` | Interactive viewer for a recorded profile. |
| `bcc` / `bpftrace` tools | eBPF-based tracing (needs kernel headers). |

---

## 22. Kernel & boot

| Command | What it does |
|---|---|
| `uname -r` | Running kernel version. |
| `cat /etc/os-release` | Distro name and version. |
| `hostnamectl` | Hostname + OS + kernel + machine-id, all in one. |
| `lsmod` | Currently loaded kernel modules. |
| `modinfo <mod>` | Metadata about a module (params, license). |
| `sudo modprobe <mod>` | Loads a module (respecting dependencies). |
| `sudo modprobe -r <mod>` | Unloads it. |
| `sysctl -a` | Every kernel tunable and its current value. |
| `sudo sysctl -w net.ipv4.ip_forward=1` | Changes a tunable at runtime. |
| Drop-in file `/etc/sysctl.d/99-x.conf` | Persist a tunable across reboots. |
| `sudo dmesg | less` | Kernel ring buffer since boot. |
| `sudo journalctl -b` | Everything from this boot. |
| `sudo journalctl -b -1` | Previous boot. |
| `systemd-analyze` | Total + per-phase boot time. |
| `systemd-analyze blame` | Slowest units at boot. |
| `systemd-analyze critical-chain` | Dependency chain that blocks fastest boot. |

---

## 23. Security hygiene

| Command | What it does |
|---|---|
| `sudo lastb | head` | Recent FAILED login attempts. |
| `sudo grep -i 'Failed password' /var/log/auth.log | tail` | SSH brute-force check on Debian/Ubuntu. |
| `who ; w ; last | head` | Who is / was logged in. |
| `find / -xdev -perm -0002 -type f 2>/dev/null` | World-writable files (audit these!). |
| `find / -xdev -perm -4000 -type f 2>/dev/null` | SUID binaries (attack surface). |
| `ls -la ~/.ssh` | Own SSH key & config perms. |
| `sudo sshd -T` | Prints the sshd daemon's effective config. |
| `sudo ufw status verbose` | Firewall state and rules (or use `iptables -L -n -v`). |
| `sudo journalctl _COMM=sshd --since today` | Today's sshd activity. |
| `sudo aa-status` | AppArmor profile status (Debian/Ubuntu). |
| `sudo getsebool -a` | SELinux booleans (RHEL family). |

Baseline hardening checklist:

- Disable root SSH (`PermitRootLogin no`).
- Disable password SSH once keys work (`PasswordAuthentication no`).
- Keep OS patched (`unattended-upgrades` or `dnf-automatic`).
- Use `fail2ban` (or equivalent) for auto-bans on brute force.
- Audit sudoers — no wildcards, no `NOPASSWD` unless justified.
- Separate service users with `nologin` shells.
- Log rotation on, journald size-capped.

---

## 24. Shell scripting essentials

Template every script should start with:

```bash
#!/usr/bin/env bash
set -euo pipefail          # exit-on-error, unset-var-error, pipe-error
IFS=$'\n\t'                # safer word splitting

readonly LOG=/var/log/myjob.log
log() { printf '%(%F %T)T %s\n' -1 "$*" | tee -a "$LOG" ; }
```

| Idiom | What it does |
|---|---|
| `set -e` | Aborts the script on the first command that returns non-zero. |
| `set -u` | Errors out on use of an unset variable. |
| `set -o pipefail` | Makes a pipeline fail if ANY stage failed (not just the last). |
| `set -x` | Traces every command as it runs. |
| `trap 'rm -rf "$tmp"' EXIT` | Runs the trap when the script exits (any reason). |
| `${var:-default}` | Uses `default` if `var` is unset or empty. |
| `${var:?msg}` | Aborts with `msg` if `var` is unset/empty. |
| `$(cmd)` | Command substitution — value = stdout of `cmd`. |
| `<<<"string"` | Here-string — feeds a literal string as stdin. |
| `<<EOF ... EOF` | Here-doc — multi-line literal input. |

Test operators (with `[[ … ]]`):

| Test | Meaning |
|---|---|
| `-e path` | Exists (any type). |
| `-f path` | Regular file. |
| `-d path` | Directory. |
| `-r/-w/-x path` | Readable / writable / executable by current user. |
| `-s path` | File exists and is non-empty. |
| `-z str` | String is empty. |
| `-n str` | String is non-empty. |
| `str1 = str2` | String equality (`==` also works in `[[ ]]`). |
| `str1 != str2` | String inequality. |
| `n1 -eq n2` (`-ne -lt -le -gt -ge`) | Integer comparison. |
| `[[ str =~ regex ]]` | Regex match (bash only). |

Debugging a script:

| Command | What it does |
|---|---|
| `bash -x script.sh` | Traces every command. |
| `set -x ; ... ; set +x` | Traces just a section. |
| `PS4='+ $LINENO: '` | Prefix trace lines with the script line number. |
| `shellcheck script.sh` | Static linter — catches quoting/scope bugs. |

---

## 25. Bonus one-liners

| Command | What it does |
|---|---|
| `sudo du -ahx /var 2>/dev/null | sort -h | tail` | Top-largest files under `/var`. |
| `sudo pkill -9 -u alice` | Kills every process owned by `alice`. |
| `sudo ss -tulpn` | Every listening port + owning PID. |
| `watch -n 1 'ls -lt /var/log | head'` | Refresh a command every second. |
| `tail -n 10000 big.log | sponge big.log` | Trim a file to its last 10k lines in place (moreutils). |
| `awk '{print $1}' access.log | sort -u | wc -l` | Unique clients in an access log. |
| `awk '{print $1}' access.log | sort | uniq -c | sort -rn | head` | Top 10 clients by request count. |
| `ps -eo pid,user,pmem,rss,cmd --sort=-rss | head` | Top memory hogs right now. |
| `python3 -m http.server 8080` | Serves the current directory over HTTP on port 8080. |
| `dd if=/dev/zero of=test bs=1M count=1024 oflag=direct` | Quick sequential-write disk benchmark (1 GiB). |
