# Linux Practice Sandbox

A batteries-included Ubuntu 22.04 container with every common Linux / DevOps /
SRE tool pre-installed. **No pre-created users, no seeded data** — you land at
a `root` prompt on a fresh box, just like SSHing into a brand-new EC2
instance. Create users, groups, swap files, services, cron jobs, etc.
yourself as you work through the exercises.

## Contents

| File | Purpose |
|---|---|
| [Dockerfile](Dockerfile) | The sandbox image |
| [linux-commands.md](linux-commands.md) | Command reference — basic → advanced |
| [scenarios.md](scenarios.md) | Interview + real-world hands-on scenarios with solutions |
| `practice/` | Sample scripts and files copied into the container at `/opt/practice/` |

## Build

```bash
cd "Common Files/linux-practice"
docker build -t linux-practice .
```

## Run

Interactive shell as `root`:

```bash
docker run -it --rm \
  --name lab -h lab \
  --cap-add=NET_ADMIN --cap-add=SYS_PTRACE \
  -v "$PWD/workdir:/root/workdir" \
  linux-practice
```

Flags explained:

- `--cap-add=NET_ADMIN` — needed for `ip link`, `iptables`, `nftables`, `tc`
- `--cap-add=SYS_PTRACE` — needed so `strace` / `gdb` can attach to other PIDs
- `-v "$PWD/workdir:/root/workdir"` — host-mounted folder that survives
  container restarts (put your scratch files here)

You're `root` from the start — like a fresh EC2 or a freshly-provisioned VM.
Everything else (users, groups, sudoers, cron, sshd, log files, swap, mounts…)
is yours to build with the commands in [linux-commands.md](linux-commands.md)
and the drills in [scenarios.md](scenarios.md).

## First-boot tour (optional)

Inside the container:

```bash
cat /etc/os-release        # confirm distro
uname -a                   # kernel
ls /opt/practice/          # reference docs + sample files
less /opt/practice/scenarios.md
```

## Where the reference docs live inside the container

```
/opt/practice/
├── README.md
├── linux-commands.md
├── scenarios.md
├── hello.sh           # sample script
└── employees.csv      # sample TSV/CSV for text-processing drills
```

They are read-only for regular users; edit them from the host if you want
to change them.

## Persist your work

Anything under `/root/workdir` is bind-mounted from `./workdir/` on the host,
so files you create there survive `docker rm`. Anywhere else in the container
is throw-away — kill the container to reset to a pristine box.

## Optional: SSH mode

`sshd` is installed but **not started by default**. Once you've created a
user inside the container (`useradd`, `passwd`, `usermod -aG sudo …`),
start the daemon and connect from another terminal:

Terminal 1 (inside the container):

```bash
service ssh start
ss -tulpn | grep :22
```

Terminal 2 (on your host — publish port 22 first when you `run` the
container: add `-p 2222:22` to the `docker run` command above):

```bash
ssh -p 2222 <the-user-you-just-created>@localhost
```

## Reset the sandbox

```bash
docker rm -f lab               # kill this instance
docker run … linux-practice    # fresh box again
```

## Tear down completely

```bash
docker rm -f lab
docker rmi linux-practice      # reclaim the image
```
