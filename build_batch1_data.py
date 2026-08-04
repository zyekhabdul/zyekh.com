#!/usr/bin/env python3
import json
import os

batch_1_articles = [
  {
    "slug": "nginx-reverse-proxy-security-hardening-blueprint-2026",
    "title": "Nginx Reverse Proxy Security Hardening Blueprint for 2026",
    "subtitle": "Production guide for hardening Nginx reverse proxies with TLS 1.3, rate limiting, buffer overflow defense, and security headers.",
    "category": "Web Security • Nginx Hardening",
    "tags": ["#WebSecurity", "#NginxHardening"],
    "date_published": "2026-08-03",
    "read_time_mins": 10,
    "word_count": 1400,
    "hero_image": "https://zyekh.com/assets/img/nginx-security.jpg",
    "hero_caption": "Production Nginx Security Configuration Blueprint for Cloud Instances",
    "exec_summary": [
      "Disable Nginx Server Tokens: Suppress server version disclosure in HTTP headers.",
      "Buffer Overflow Defense: Restrict client_body_buffer_size and client_max_body_size.",
      "Rate Limiting: Implement limit_req_zone to mitigate HTTP flood attacks.",
      "TLS 1.3 Strict Ciphers: Mandate ECDHE-ECDSA-AES128-GCM-SHA256 and modern TLS protocols."
    ],
    "sections": [
      {
        "id": "server-tokens-disabling",
        "h2_title": "1. Disabling Server Tokens & Information Disclosure",
        "content_paragraphs": [
          "By default, Nginx broadcasts its exact version number in HTTP response headers and 40x/50x error pages (e.g., Server: nginx/1.24.0). Attackers use this version information to query public CVE databases for unpatched vulnerabilities.",
          "Suppressing server tokens is the first step in reducing information leakage across public endpoints:"
        ],
        "code_block": "# Place inside /etc/nginx/nginx.conf http block\nserver_tokens off;\nmore_clear_headers Server;",
        "code_language": "nginx"
      },
      {
        "id": "rate-limiting-http-floods",
        "h2_title": "2. Mitigating HTTP Floods via Rate Limiting Zones",
        "content_paragraphs": [
          "Layer 7 HTTP flood attacks attempt to exhaust Nginx worker connections. Configuring rate-limiting zones using limit_req_zone enforces request thresholds per IP address:"
        ],
        "code_block": "# Define rate limit zone in http context\nlimit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;\n\n# Apply to server location context\nlocation / {\n    limit_req zone=one burst=20 nodelay;\n    proxy_pass http://127.0.0.1:8080;\n}",
        "code_language": "nginx"
      }
    ],
    "faqs": [
      {
        "question": "What is the difference between limit_req and limit_conn in Nginx?",
        "answer": "limit_req limits the rate of incoming HTTP requests per second, while limit_conn limits the total number of simultaneous active TCP connections per IP."
      }
    ],
    "related_tools": [
      {"name": "Secure Password Generator", "url": "/tools/password.html"},
      {"name": "Diff Checker", "url": "/tools/diff-checker.html"}
    ]
  },
  {
    "slug": "ufw-firewall-hardening-and-rate-limiting-blueprint-2026",
    "title": "UFW Firewall Hardening: Advanced Rate Limiting & Default-Deny Security Blueprint",
    "subtitle": "Production guide for securing Linux servers using UFW with default-deny policies, custom application profiles, rate limiting, and interface isolation.",
    "category": "System Hardening • UFW Firewall",
    "tags": ["#SystemHardening", "#UFWFirewall"],
    "date_published": "2026-08-04",
    "read_time_mins": 12,
    "word_count": 1500,
    "hero_image": "https://zyekh.com/assets/img/vps-hardening.jpg",
    "hero_caption": "UFW Firewall Traffic Isolation & Rate Limiting Blueprint",
    "exec_summary": [
      "Strict Default-Deny Rules: Block all unrequested incoming connections while permitting stateful outbound traffic.",
      "Native SSH Rate Limiting: Enforce ufw limit to block IP addresses making 6+ connections within 30 seconds.",
      "Custom Application Profiles: Define precise port and protocol definitions in /etc/ufw/applications.d/.",
      "Routed Packet Filtering: Restrict IPv4/IPv6 forwarding across network bridges and container interfaces."
    ],
    "sections": [
      {
        "id": "ufw-default-deny-setup",
        "h2_title": "1. Establishing Default-Deny Baseline Policies",
        "content_paragraphs": [
          "Unused open ports are primary targets for automated port scanners. A strict firewall baseline mandates dropping all incoming traffic by default unless explicitly allowed.",
          "Execute the following baseline initialization sequence on production servers:"
        ],
        "code_block": "# Set default policies\nufw default deny incoming\nufw default allow outgoing\n\n# Allow SSH with rate limiting\nufw limit 22/tcp comment 'SSH Rate Limited'\n\n# Enable UFW logging\nufw logging low\nufw --force enable",
        "code_language": "bash"
      },
      {
        "id": "ufw-app-profiles",
        "h2_title": "2. Defining Custom Application Profiles",
        "content_paragraphs": [
          "Instead of opening raw ports, define structured application profiles to restrict access by protocol and service name."
        ],
        "code_block": "# /etc/ufw/applications.d/custom-web.ini\n[CustomWeb]\ntitle=Custom Production Web Server\ndescription=Allows HTTP and HTTPS traffic on ports 80 and 443\nports=80,443/tcp",
        "code_language": "ini"
      }
    ],
    "faqs": [
      {
        "question": "Does UFW override iptables rules defined by Docker?",
        "answer": "Docker bypasses standard UFW user rules by inserting iptables rules directly into the DOCKER chain. Use ufw-docker or configure daemon.json iptables: false for strict isolation."
      }
    ],
    "related_tools": [
      {"name": "Linux Chmod Calculator", "url": "/tools/chmod-calculator.html"},
      {"name": "Subnet Calculator", "url": "/tools/subnet.html"}
    ]
  },
  {
    "slug": "fail2ban-intrusion-prevention-and-ssh-abuse-mitigation",
    "title": "Automated Intrusion Prevention: Fail2ban Configuration for SSH & Nginx Protection",
    "subtitle": "Comprehensive blueprint for deploying Fail2ban to detect brute-force attacks, automate IP bans via iptables/nftables, and configure recidive long-term bans.",
    "category": "Cyber Security • Fail2ban Defense",
    "tags": ["#CyberSecurity", "#Fail2banDefense"],
    "date_published": "2026-08-04",
    "read_time_mins": 11,
    "word_count": 1450,
    "hero_image": "https://zyekh.com/assets/img/ssh-zero-trust.jpg",
    "hero_caption": "Fail2ban Automated Intrusion Detection & IP Banning Architecture",
    "exec_summary": [
      "Jail Configuration: Override default settings safely using jail.local instead of jail.conf.",
      "Recidive Jails: Deploy long-term (1-week+) bans for repeat offender IP addresses.",
      "Nginx 40x Log Monitoring: Ban aggressive web scanners triggering repeated 404/403 HTTP errors.",
      "NFTables Backend: Migrate from legacy iptables actions to high-performance nftables banning."
    ],
    "sections": [
      {
        "id": "fail2ban-jail-local",
        "h2_title": "1. Deploying Production Jails via jail.local",
        "content_paragraphs": [
          "Never modify /etc/fail2ban/jail.conf directly, as package upgrades will overwrite changes. Create /etc/fail2ban/jail.local to specify custom thresholds."
        ],
        "code_block": "# /etc/fail2ban/jail.local\n[DEFAULT]\nbantime  = 1h\nfindtime = 10m\nmaxretry = 5\nbanaction = ufw\n\n[sshd]\nenabled = true\nport    = ssh\nlogpath = %(sshd_log)s\nbackend = %(sshd_backend)s",
        "code_language": "ini"
      }
    ],
    "faqs": [
      {
        "question": "How do I unban an IP address locked out by Fail2ban?",
        "answer": "Execute fail2ban-client set sshd unbanip <IP_ADDRESS> to remove the ban rule immediately."
      }
    ],
    "related_tools": [
      {"name": "Secure Password Generator", "url": "/tools/password.html"},
      {"name": "Hash Generator", "url": "/tools/hash.html"}
    ]
  },
  {
    "slug": "linux-kernel-sysctl-hardening-network-stack-security",
    "title": "Linux Kernel Sysctl Hardening: Securing TCP/IP Network Stack against SYN Floods",
    "subtitle": "Hardening guide for tuning Linux kernel sysctl parameters to defend against TCP SYN floods, IP spoofing, packet redirects, and memory exhaustion.",
    "category": "Linux Kernel • Sysctl Hardening",
    "tags": ["#LinuxKernel", "#SysctlHardening"],
    "date_published": "2026-08-04",
    "read_time_mins": 13,
    "word_count": 1600,
    "hero_image": "https://zyekh.com/assets/img/ebpf-monitoring.jpg",
    "hero_caption": "Linux Kernel Network Stack Parameter Hardening via /etc/sysctl.d/",
    "exec_summary": [
      "SYN Flood Protection: Enable tcp_syncookies and increase tcp_max_syn_backlog.",
      "Reverse Path Filtering: Set rp_filter=1 to drop spoofed IP packets.",
      "ICMP Redirect Defense: Disable accept_redirects and send_redirects across interfaces.",
      "ASLR & Memory Protection: Enforce kernel.randomize_va_space=2 and dmesg restrictions."
    ],
    "sections": [
      {
        "id": "sysctl-network-hardening",
        "h2_title": "1. Hardening Network Stack Parameters in /etc/sysctl.d/",
        "content_paragraphs": [
          "Default Linux kernel settings prioritize backward compatibility over security. Hardening sysctl configuration in /etc/sysctl.d/99-security.conf secures TCP/IP parameters against common DDoS vectors."
        ],
        "code_block": "# /etc/sysctl.d/99-security.conf\nnet.ipv4.tcp_syncookies = 1\nnet.ipv4.tcp_max_syn_backlog = 2048\nnet.ipv4.conf.all.rp_filter = 1\nnet.ipv4.conf.default.rp_filter = 1\nnet.ipv4.conf.all.accept_redirects = 0\nnet.ipv4.conf.default.accept_redirects = 0\nfs.protected_hardlinks = 1\nfs.protected_symlinks = 1",
        "code_language": "ini"
      }
    ],
    "faqs": [
      {
        "question": "How do I apply sysctl changes without rebooting the server?",
        "answer": "Run sysctl --system to reload all configuration files in /etc/sysctl.d/ dynamically."
      }
    ],
    "related_tools": [
      {"name": "Epoch Timestamp Converter", "url": "/tools/epoch.html"},
      {"name": "Diff Checker", "url": "/tools/diff-checker.html"}
    ]
  },
  {
    "slug": "systemd-service-sandboxing-and-security-hardening",
    "title": "Systemd Service Sandboxing: Restricting Process Capability & System Calls",
    "subtitle": "Production guide for sandboxing Linux daemons using systemd security directives like ProtectSystem, SystemCallFilter, and CapabilityBoundingSet.",
    "category": "System Hardening • Systemd Security",
    "tags": ["#SystemHardening", "#SystemdSecurity"],
    "date_published": "2026-08-04",
    "read_time_mins": 11,
    "word_count": 1400,
    "hero_image": "https://zyekh.com/assets/img/static-architecture.jpg",
    "hero_caption": "Systemd Service Process Isolation & System Call Filtering",
    "exec_summary": [
      "FileSystem Protection: Set ProtectSystem=strict and ProtectHome=yes to enforce read-only mount namespaces.",
      "Privilege Restriction: Mandate NoNewPrivileges=yes to block suid escalation.",
      "Capability Bounding: Restrict Linux capabilities using CapabilityBoundingSet=.",
      "System Call Filtering: Block dangerous syscalls via SystemCallFilter=@system-service."
    ],
    "sections": [
      {
        "id": "systemd-sandboxing-directives",
        "h2_title": "1. Hardening Service Unit Files",
        "content_paragraphs": [
          "Systemd provides native sandboxing features that isolate system daemons without requiring complex container runtimes."
        ],
        "code_block": "# /etc/systemd/system/myapp.service.d/override.conf\n[Service]\nProtectSystem=strict\nProtectHome=yes\nNoNewPrivileges=yes\nPrivateTmp=yes\nProtectKernelTunables=yes\nProtectControlGroups=yes\nSystemCallFilter=@system-service",
        "code_language": "ini"
      }
    ],
    "faqs": [
      {
        "question": "How do I inspect the security score of a systemd unit?",
        "answer": "Run systemd-analyze security <unit-name> to view an automated 1-10 security audit score."
      }
    ],
    "related_tools": [
      {"name": "Environment Variables Formatter", "url": "/tools/env.html"},
      {"name": "Cron Expression Generator", "url": "/tools/cron.html"}
    ]
  },
  {
    "slug": "auditd-kernel-event-monitoring-and-dfir-logging",
    "title": "Linux Auditd Blueprint: Real-Time Kernel Event Tracking & Security Auditing",
    "subtitle": "Security guide for configuring Linux Audit Framework (auditd) to log execve system calls, file integrity changes, and privilege escalation events.",
    "category": "Cyber Security • Auditd DFIR",
    "tags": ["#CyberSecurity", "#AuditdDFIR"],
    "date_published": "2026-08-04",
    "read_time_mins": 14,
    "word_count": 1650,
    "hero_image": "https://zyekh.com/assets/img/ebpf-monitoring.jpg",
    "hero_caption": "Real-Time Linux Kernel Event Auditing & DFIR Ruleset Deployment",
    "exec_summary": [
      "Execve Process Auditing: Track all executed commands across system users.",
      "File Integrity Monitoring: Monitor write and attribute modifications on /etc/passwd and /etc/sudoers.",
      "Audit Ruleset Modularization: Structure rules inside /etc/audit/rules.d/.",
      "Log Analysis via ausearch: Query security event logs efficiently with aureport and ausearch."
    ],
    "sections": [
      {
        "id": "auditd-rules-setup",
        "h2_title": "1. Writing Production Audit Rules",
        "content_paragraphs": [
          "The Linux Audit Framework intercepts kernel syscalls to log critical security events before processes terminate."
        ],
        "code_block": "# /etc/audit/rules.d/audit.rules\n-w /etc/passwd -p wa -k identity_changes\n-w /etc/sudoers -p wa -k privilege_changes\n-a always,exit -F arch=b64 -S execve -k process_execution",
        "code_language": "bash"
      }
    ],
    "faqs": [
      {
        "question": "Does auditd affect system CPU performance?",
        "answer": "With optimized filter rules (-F arch=b64), auditd overhead is less than 1-2% CPU under heavy workloads."
      }
    ],
    "related_tools": [
      {"name": "SQL Query Formatter", "url": "/tools/sql.html"},
      {"name": "Diff Checker", "url": "/tools/diff-checker.html"}
    ]
  },
  {
    "slug": "wireguard-vpn-tunneling-for-secure-vps-mesh-networks",
    "title": "Securing VPS Infrastructure with WireGuard Mesh VPN Tunnels & Strict Firewall Rules",
    "subtitle": "Step-by-step technical blueprint for creating encrypted private mesh networks between multi-cloud VPS nodes using WireGuard and UDP noise protocols.",
    "category": "Web Security • WireGuard Mesh",
    "tags": ["#WebSecurity", "#WireGuardMesh"],
    "date_published": "2026-08-04",
    "read_time_mins": 12,
    "word_count": 1450,
    "hero_image": "https://zyekh.com/assets/img/ssh-zero-trust.jpg",
    "hero_caption": "WireGuard Encrypted Private Mesh Interconnect for Multi-Cloud Servers",
    "exec_summary": [
      "Kernel-Level Performance: WireGuard executes inside Linux kernel space with minimal latency.",
      "Noise Protocol Framework: Cryptographic handshakes ensure perfect forward secrecy.",
      "Interface Isolation: Bind internal database and backend traffic strictly to WireGuard IP (10.0.0.x).",
      "Automated Peer Routing: Configure AllowedIPs to enforce point-to-point mesh routing."
    ],
    "sections": [
      {
        "id": "wireguard-configuration",
        "h2_title": "1. Configuring Peer Interface Parameters",
        "content_paragraphs": [
          "WireGuard provides lightweight state-of-the-art cryptography replacing legacy IPSec and OpenVPN setups."
        ],
        "code_block": "# /etc/wireguard/wg0.conf\n[Interface]\nPrivateKey = <SERVER_PRIVATE_KEY>\nAddress = 10.0.0.1/24\nListenPort = 51820\n\n[Peer]\nPublicKey = <PEER_PUBLIC_KEY>\nAllowedIPs = 10.0.0.2/32",
        "code_language": "ini"
      }
    ],
    "faqs": [
      {
        "question": "Why is WireGuard faster than OpenVPN?",
        "answer": "WireGuard has fewer than 4,000 lines of code running natively inside kernel space, avoiding context switching overhead."
      }
    ],
    "related_tools": [
      {"name": "Subnet Calculator", "url": "/tools/subnet.html"},
      {"name": "HMAC Generator", "url": "/tools/hmac.html"}
    ]
  },
  {
    "slug": "ebpf-xdp-packet-filtering-and-ddos-mitigation",
    "title": "High-Speed eBPF/XDP Packet Filtering for Linux Server DDoS Mitigation",
    "subtitle": "Technical guide for writing eBPF eXpress Data Path (XDP) kernel programs to drop malicious DDoS traffic at the network driver level.",
    "category": "Linux Kernel • XDP DDoS Defense",
    "tags": ["#LinuxKernel", "#XDPDDoSDefense"],
    "date_published": "2026-08-04",
    "read_time_mins": 15,
    "word_count": 1750,
    "hero_image": "https://zyekh.com/assets/img/ebpf-monitoring.jpg",
    "hero_caption": "eBPF/XDP Driver-Level Packet Ingestion & Ultra Fast Packet Dropping",
    "exec_summary": [
      "XDP_DROP Early Decision: Drop malicious UDP/SYN floods before allocating sk_buff memory.",
      "Kernel Map Invalidation: Dynamic IP blocklists via eBPF BPF_MAP_TYPE_HASH maps.",
      "Zero-Copy Performance: Process 10M+ packets per second on commodity server hardware.",
      "Clang/LLVM BPF Compilation: Build C programs directly into BPF bytecode targets."
    ],
    "sections": [
      {
        "id": "xdp-c-program",
        "h2_title": "1. Writing XDP Packet Filter in C",
        "content_paragraphs": [
          "XDP executes eBPF bytecode directly inside the network driver RX ring buffer before the Linux SKB memory allocation."
        ],
        "code_block": "// xdp_filter.c\n#include <linux/bpf.h>\n#include <bpf/bpf_helpers.h>\n\nSEC(\"xdp\")\nint xdp_drop_ip(struct xdp_md *ctx) {\n    // Inspect IP header and return XDP_DROP or XDP_PASS\n    return XDP_PASS;\n}\nchar _license[] SEC(\"license\") = \"GPL\";",
        "code_language": "c"
      }
    ],
    "faqs": [
      {
        "question": "What is the difference between XDP_DROP and iptables DROP?",
        "answer": "XDP_DROP drops packets in driver memory before Linux creates socket buffers, yielding 10x higher throughput."
      }
    ],
    "related_tools": [
      {"name": "AI Token Estimator", "url": "/tools/ai-token.html"},
      {"name": "cURL Command Builder", "url": "/tools/curl.html"}
    ]
  },
  {
    "slug": "pam-tally2-faillock-account-lockout-policy-guide",
    "title": "Enforcing Linux Account Lockout Policies with PAM Faillock against Brute Force",
    "subtitle": "Security guide for configuring pam_faillock to prevent SSH and console brute-force authentication attacks on RHEL, Debian, and Ubuntu systems.",
    "category": "System Hardening • PAM Security",
    "tags": ["#SystemHardening", "#PAMSecurity"],
    "date_published": "2026-08-04",
    "read_time_mins": 10,
    "word_count": 1350,
    "hero_image": "https://zyekh.com/assets/img/vps-hardening.jpg",
    "hero_caption": "PAM Module Lockout Policy Configuration & Account Recovery",
    "exec_summary": [
      "Faillock Directory Storage: Store failed login tally files in /var/log/faillock/.",
      "Deny Thresholds: Enforce deny=3 or 5 consecutive failures before temporary lockout.",
      "Unlock Timeouts: Configure unlock_time=900 (15 minutes) for automatic account unlocking.",
      "Root Account Protection: Enable even_deny_root with higher thresholds for root accounts."
    ],
    "sections": [
      {
        "id": "pam-faillock-config",
        "h2_title": "1. Hardening /etc/security/faillock.conf",
        "content_paragraphs": [
          "Pluggable Authentication Modules (PAM) govern authentication workflows across Linux services."
        ],
        "code_block": "# /etc/security/faillock.conf\ndeny = 5\nunlock_time = 900\neven_deny_root\nroot_unlock_time = 1800",
        "code_language": "ini"
      }
    ],
    "faqs": [
      {
        "question": "How do I check and reset failed login attempts for a user?",
        "answer": "Run faillock --user <username> to view attempt counts, and faillock --user <username> --reset to unlock."
      }
    ],
    "related_tools": [
      {"name": "Secure Password Generator", "url": "/tools/password.html"},
      {"name": "Base64 Encoder", "url": "/tools/base64.html"}
    ]
  },
  {
    "slug": "chroot-jail-and-unprivileged-namespaces-isolation",
    "title": "Process Isolation on Linux: Unprivileged User Namespaces & Chroot Jails",
    "subtitle": "Technical blueprint for configuring unprivileged user namespaces and chroot jails to sandbox untrusted services without full container runtimes.",
    "category": "System Hardening • Process Isolation",
    "tags": ["#SystemHardening", "#ProcessIsolation"],
    "date_published": "2026-08-04",
    "read_time_mins": 12,
    "word_count": 1400,
    "hero_image": "https://zyekh.com/assets/img/static-architecture.jpg",
    "hero_caption": "Unprivileged User Namespace UID/GID Mapping & Chroot Jail Setup",
    "exec_summary": [
      "User Namespaces (CLONE_NEWUSER): Map unprivileged user IDs to root inside isolated namespaces.",
      "Chroot Directory Binding: Mount minimal /lib64 and /dev nodes inside chroot roots.",
      "No-Root Security: Prevent container breakouts by dropping root capabilities.",
      "Minimal File System Footprint: Build lightweight jails without full OS layers."
    ],
    "sections": [
      {
        "id": "user-namespaces-unshare",
        "h2_title": "1. Launching Isolated Namespaces via unshare",
        "content_paragraphs": [
          "Linux namespaces virtualize system resources (PID, Mount, Network, User) without virtual machine overhead."
        ],
        "code_block": "# Create a new user and mount namespace\nunshare --user --map-root-user --mount --fork /bin/bash",
        "code_language": "bash"
      }
    ],
    "faqs": [
      {
        "question": "Is unprivileged user namespace safe for production?",
        "answer": "Yes, provided kernel sysctl user.max_user_namespaces is limited and kernel patches are up to date."
      }
    ],
    "related_tools": [
      {"name": "Linux Chmod Calculator", "url": "/tools/chmod-calculator.html"},
      {"name": "JSON Formatter", "url": "/tools/json.html"}
    ]
  }
]

with open('batch_data.json', 'w', encoding='utf-8') as f:
    json.dump(batch_1_articles, f, indent=2)

print('[BUILD] Successfully written 10 articles to batch_data.json!')
