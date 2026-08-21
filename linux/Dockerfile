# syntax=docker/dockerfile:1.7
# =============================================================================
# Linux Practice Sandbox — bare, lean platform
# =============================================================================
# A slim Ubuntu image tuned for interactive Linux / DevOps / SRE practice.
# You land as **root** on a fresh box — no pre-created users, no seeded data —
# exactly like SSHing into a brand-new EC2 instance. You create users, groups,
# swap files, services, etc. as part of the exercises.
#
# Design goals:
#   * Broad command coverage (shells, text, net, proc, disk, scheduling, ssh…)
#   * NO compilers / dev headers / build-essential  (huge, not needed to
#     practice Linux commands — install ad-hoc inside the container if wanted)
#   * NO duplicate tools (kept `less` not `most`, `htop` not `atop`, etc.)
#   * BuildKit apt cache mounts → repeat builds skip the download entirely
#
# Build (BuildKit is on by default with modern Docker Desktop):
#   docker build -t linux-practice .
#
# Run (root shell, behaves like a fresh VM):
#   docker run -it --rm --name lab -h lab \
#       --cap-add=NET_ADMIN --cap-add=SYS_PTRACE \
#       -v "$PWD/workdir:/root/workdir" \
#       linux-practice
#
# Capabilities:
#   --cap-add=NET_ADMIN   → play with `ip`, `iptables`, `nftables`, `tc`
#   --cap-add=SYS_PTRACE  → let `strace` / `gdb` attach to other processes
#
# Reference material at /opt/practice/ (read-only):
#   README.md  linux-commands.md  scenarios.md  hello.sh  employees.csv
# =============================================================================

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# ---------------------------------------------------------------------------
# 1. Core tool install (single layer, BuildKit apt cache, no recommends)
#    Grouped by intent so it is easy to prune / extend.
# ---------------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        # --- shells & session ---
        bash bash-completion zsh tmux sudo \
        # --- editors & pagers ---
        vim nano less \
        # --- base userland / archives ---
        ca-certificates locales tzdata tree file \
        tar gzip bzip2 xz-utils zip unzip \
        # --- text processing ---
        grep sed gawk jq ripgrep fd-find bat dos2unix moreutils \
        # --- process / system observability ---
        procps psmisc htop lsof strace ncdu sysstat \
        # --- networking (client + admin) ---
        iproute2 iputils-ping net-tools dnsutils \
        traceroute mtr-tiny tcpdump netcat-openbsd curl wget whois \
        iptables nftables \
        # --- scheduling ---
        cron at logrotate \
        # --- ssh + rsync ---
        openssh-client openssh-server rsync \
        # --- vcs + scripting runtime ---
        git python3 python3-pip \
        # --- man pages & misc quality-of-life ---
        man-db manpages bsdmainutils bsdextrautils \
        acl attr uuid-runtime \
    && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# Ubuntu ships `fd` and `bat` under alt binary names — symlink for muscle memory.
RUN ln -sf /usr/bin/fdfind        /usr/local/bin/fd  \
 && ln -sf /usr/bin/batcat        /usr/local/bin/bat \
 && ln -sf /usr/bin/python3       /usr/local/bin/python

# ---------------------------------------------------------------------------
# 2. `yq` — Mike Farah's Go binary (single static file, ~10 MB).
#    Detects arch so the image builds on both Apple Silicon and amd64.
# ---------------------------------------------------------------------------
ARG YQ_VERSION=v4.44.3
RUN set -eux; \
    arch="$(dpkg --print-architecture)"; \
    case "$arch" in \
        amd64) yq_arch=amd64 ;; \
        arm64) yq_arch=arm64 ;; \
        *) echo "unsupported arch: $arch" >&2; exit 1 ;; \
    esac; \
    curl -fsSL "https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_${yq_arch}" \
        -o /usr/local/bin/yq; \
    chmod +x /usr/local/bin/yq; \
    yq --version

# ---------------------------------------------------------------------------
# 3. Reference material — read-only sample data under /opt/practice/
# ---------------------------------------------------------------------------
RUN install -d -m 0755 /opt/practice
COPY README.md            /opt/practice/README.md
COPY linux-commands.md    /opt/practice/linux-commands.md
COPY scenarios.md         /opt/practice/scenarios.md
COPY practice/            /opt/practice/
RUN chmod -R a+rX /opt/practice \
 && ( chmod +x /opt/practice/*.sh 2>/dev/null || true )

# ---------------------------------------------------------------------------
# 4. Minimal root-shell niceties (only touches /root — no other users exist)
# ---------------------------------------------------------------------------
RUN cat >> /root/.bashrc <<'EOF'

# ---- practice env ----
export EDITOR=vim
export PAGER=less
export LESS='-R -F -X'

alias ll='ls -alh --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias ports='ss -tulpn'
alias myip='hostname -I'

if [ -t 1 ] && [ -z "${PRACTICE_BANNER_SHOWN:-}" ]; then
    export PRACTICE_BANNER_SHOWN=1
    echo
    echo "Linux Practice Sandbox — you are root on a fresh box."
    echo "  * Reference : /opt/practice/linux-commands.md"
    echo "  * Scenarios : /opt/practice/scenarios.md"
    echo "  * Samples   : /opt/practice/hello.sh, /opt/practice/employees.csv"
    echo "  * No users, no data — build the system yourself (like a fresh EC2)."
    echo
fi
EOF

# ---------------------------------------------------------------------------
# 5. sshd is installed but NOT started. After you create a user inside the
#    container (useradd / passwd / usermod -aG sudo …), start it with:
#        service ssh start          # or:  /usr/sbin/sshd -D
# ---------------------------------------------------------------------------
RUN mkdir -p /var/run/sshd
EXPOSE 22

# ---------------------------------------------------------------------------
# 6. Entry — root login shell, like a freshly-provisioned VM
# ---------------------------------------------------------------------------
WORKDIR /root
CMD ["/bin/bash", "-l"]
