#!/usr/bin/env python3
import json

b1 = [
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
          "Suppressing server tokens is the first step in reducing information leakage across public endpoints. When server_tokens is disabled, Nginx strips the version number from all HTTP response headers and standard error pages.",
          "In production environments with headers-more-nginx-module installed, you can also completely purge the 'Server' header string to prevent fingerprinting."
        ],
        "code_block": "# Place inside /etc/nginx/nginx.conf http block\nhttp {\n    server_tokens off;\n    more_clear_headers Server;\n}",
        "code_language": "nginx"
      },
      {
        "id": "buffer-overflow-defense",
        "h2_title": "2. Buffer Size Allocation & HTTP Request Body Limits",
        "content_paragraphs": [
          "Unrestricted buffer sizes expose Nginx worker processes to memory exhaustion and buffer overflow exploits. Excessive client payload sizes allow attackers to fill RAM buffers, triggering kernel OOM (Out Of Memory) killers.",
          "To defend against large payload POST attacks and slowloris attempts, enforce explicit limits on client body buffers, header buffers, and max payload sizes.",
          "If a client sends a request larger than client_max_body_size, Nginx immediately returns HTTP status 413 (Payload Too Large) without attempting to buffer data to disk."
        ],
        "code_block": "# Restrict request sizes in http or server block\nclient_body_buffer_size 16k;\nclient_header_buffer_size 1k;\nclient_max_body_size 8M;\nlarge_client_header_buffers 2 1k;",
        "code_language": "nginx"
      },
      {
        "id": "rate-limiting-http-floods",
        "h2_title": "3. Mitigating HTTP Floods via Rate Limiting Zones",
        "content_paragraphs": [
          "Layer 7 HTTP flood attacks attempt to exhaust Nginx worker connections by sending thousands of requests per second. Configuring rate-limiting zones using limit_req_zone enforces request thresholds per IP address.",
          "The limit_req_zone directive uses the leaky bucket algorithm. Requests exceeding the defined rate are buffered up to the burst limit; additional requests above burst are dropped immediately with HTTP status 503 (Service Unavailable).",
          "Using $binary_remote_addr instead of $remote_addr saves memory, requiring only 64 bytes per IP address in shared memory storage."
        ],
        "code_block": "# Define rate limit zone in http context\nlimit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;\n\n# Apply to server location context\nlocation / {\n    limit_req zone=one burst=20 nodelay;\n    proxy_pass http://127.0.0.1:8080;\n}",
        "code_language": "nginx"
      },
      {
        "id": "tls-hardening-ciphers",
        "h2_title": "4. TLS 1.3 Enforcement & Cipher Suite Hardening",
        "content_paragraphs": [
          "Legacy TLS protocols (TLS 1.0 and TLS 1.1) and weak ciphers (RC4, 3DES) contain cryptographic flaws vulnerable to POODLE, BEAST, and SWEET32 attacks. Production reverse proxies must enforce TLS 1.2 and TLS 1.3 exclusively.",
          "Mandating modern ciphers ensures Perfect Forward Secrecy (PFS), protecting intercepted traffic from decryption even if the server's private key is compromised in the future.",
          "Configure strict session caching and enable OCSP stapling to minimize TLS handshake latency for mobile clients."
        ],
        "code_block": "# Strict TLS 1.2 / TLS 1.3 configuration\nssl_protocols TLSv1.2 TLSv1.3;\nssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;\nssl_prefer_server_ciphers off;\nssl_session_timeout 1d;\nssl_session_cache shared:SSL:10m;\nssl_stapling on;\nssl_stapling_verify on;",
        "code_language": "nginx"
      },
      {
        "id": "security-headers-setup",
        "h2_title": "5. Injecting Mandatory HTTP Security Headers",
        "content_paragraphs": [
          "HTTP security headers instruct client browsers to enforce strict security policies, blocking XSS, clickjacking, MIME-sniffing, and credential interception.",
          "Add strict headers across all server blocks using the add_header directive with the always flag to ensure headers are sent on error responses as well."
        ],
        "code_block": "# Mandatory Security Headers\nadd_header X-Frame-Options \"DENY\" always;\nadd_header X-Content-Type-Options \"nosniff\" always;\nadd_header Referrer-Policy \"strict-origin-when-cross-origin\" always;\nadd_header Strict-Transport-Security \"max-age=63072000; includeSubDomains; preload\" always;\nadd_header Permissions-Policy \"camera=(), microphone=(), geolocation=()\" always;",
        "code_language": "nginx"
      },
      {
        "id": "verification-and-audit",
        "h2_title": "6. Verification & Security Audit Checklist",
        "content_paragraphs": [
          "After applying Nginx security hardening configurations, verify syntax correctness using nginx -t before reloading the daemon.",
          "Use cURL to audit response headers and SSL Labs to verify TLS cipher suite compliance."
        ],
        "code_block": "# Test configuration syntax and reload Nginx\nsystemctl reload nginx\n\n# Audit HTTP response headers with cURL\ncurl -I https://zyekh.com/",
        "code_language": "bash"
      }
    ],
    "faqs": [
      {
        "question": "What is the difference between limit_req and limit_conn in Nginx?",
        "answer": "limit_req limits the rate of incoming HTTP requests per second, while limit_conn limits the total number of simultaneous active TCP connections per IP."
      },
      {
        "question": "Why use ssl_prefer_server_ciphers off in TLS 1.3?",
        "answer": "In TLS 1.3, cipher negotiation is simplified and setting ssl_prefer_server_ciphers off allows clients to choose their most optimized cipher suite safely."
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
          "When default-deny incoming is enforced, Linux drops all TCP SYN requests and UDP packets to closed ports without sending ICMP unreachable responses, preventing port scanning reconnaissance.",
          "Execute the following baseline initialization sequence on production Debian and Ubuntu instances:"
        ],
        "code_block": "# Reset UFW to clean state\nufw --force reset\n\n# Set default traffic policies\nufw default deny incoming\nufw default allow outgoing\n\n# Allow SSH on custom port with rate limiting\nufw limit 22/tcp comment 'SSH Rate Limited'\n\n# Enable UFW logging\nufw logging low\nufw --force enable",
        "code_language": "bash"
      },
      {
        "id": "ufw-rate-limiting-ssh",
        "h2_title": "2. Advanced SSH Rate Limiting & Brute-Force Prevention",
        "content_paragraphs": [
          "Automated bots scan IPv4 CIDR blocks continuously for open port 22. Standard ufw allow 22/tcp leaves the SSH port vulnerable to sustained password guessing and handshake attacks.",
          "The ufw limit directive leverages iptables recent module to track connection attempts per IP address. If an IP address attempts 6 or more connections within a 30-second window, UFW automatically drops packets from that IP address.",
          "For maximum security, combine ufw limit with custom SSH listening ports to eliminate 99% of automated scanner noise."
        ],
        "code_block": "# Restrict custom SSH port with rate limiting\nufw limit 2222/tcp comment 'Custom SSH Port Limited'\n\n# Inspect UFW active rules with rule numbers\nufw status numbered",
        "code_language": "bash"
      },
      {
        "id": "ufw-app-profiles",
        "h2_title": "3. Defining Custom Application Profiles",
        "content_paragraphs": [
          "Instead of specifying raw port numbers directly in shell scripts, define structured application profiles in /etc/ufw/applications.d/. Profiles standardize firewall configurations across fleet management tooling.",
          "Application profiles specify the title, description, and exact TCP/UDP ports required by a service.",
          "Reload UFW application profiles and verify profile syntax using ufw app list."
        ],
        "code_block": "# Create /etc/ufw/applications.d/custom-web.ini\n[CustomWebserver]\ntitle=Custom Production Web Server\ndescription=Allows HTTP and HTTPS traffic on standard web ports\nports=80,443/tcp\n\n# Apply application profile\nufw allow CustomWebserver",
        "code_language": "ini"
      },
      {
        "id": "ufw-interface-isolation",
        "h2_title": "4. Interface Isolation & Subnet Access Control",
        "content_paragraphs": [
          "Multi-homed cloud instances connected to public internet interfaces and private VPC networks must restrict management access strictly to private interfaces.",
          "Configuring interface-specific rules prevents administrative ports (e.g., Redis on 6379, Postgres on 5432) from exposing bindings to public IPv4 addresses.",
          "Use in on <interface> directives to bind rules to specific network interfaces like eth1 or wireguard wg0."
        ],
        "code_block": "# Allow PostgreSQL strictly on private VPC interface eth1\nufw allow in on eth1 to any port 5432 proto tcp comment 'Private DB Access'\n\n# Allow WireGuard VPN traffic on public interface eth0\nufw allow in on eth0 to any port 51820 proto udp comment 'WireGuard Public VPN'",
        "code_language": "bash"
      },
      {
        "id": "ufw-logging-tuning",
        "h2_title": "5. Logging Calibration & Logrotate Management",
        "content_paragraphs": [
          "Uncalibrated firewall logging can fill server root disks rapidly during heavy DDoS attacks. UFW supports five logging levels: off, low, medium, high, and full.",
          "Logging level low records all blocked packets that violate default policy, plus matching logged rules. Logs are saved to /var/log/ufw.log.",
          "Ensure logrotate compresses UFW log files daily to preserve disk headroom."
        ],
        "code_block": "# Set optimal production logging level\nufw logging low\n\n# Tail live UFW blocked packets\ntail -f /var/log/ufw.log | grep '[UFW BLOCK]'",
        "code_language": "bash"
      },
      {
        "id": "ufw-audit-verification",
        "h2_title": "6. Verification & Security Audit Checklist",
        "content_paragraphs": [
          "Verify UFW active status, rule numbers, and default policies using verbose status outputs.",
          "Test firewall rule enforcement from an external client using nmap port scans."
        ],
        "code_block": "# Verify UFW status and rules\nufw status verbose\n\n# External port audit with nmap\nnmap -sS -p 22,80,443,5432 <SERVER_IP>",
        "code_language": "bash"
      }
    ],
    "faqs": [
      {
        "question": "Does UFW override iptables rules defined by Docker?",
        "answer": "Docker bypasses standard UFW user rules by inserting iptables rules directly into the DOCKER chain. Use ufw-docker or configure daemon.json iptables: false for strict isolation."
      },
      {
        "question": "What is the difference between ufw allow and ufw limit?",
        "answer": "ufw allow permits unlimited connections, while ufw limit denies connections if an IP address attempts 6+ connections within 30 seconds."
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
    "read_time_mins": 14,
    "word_count": 1550,
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
        "id": "fail2ban-architecture",
        "h2_title": "1. Fail2ban Architecture & Log Parsing Engine",
        "content_paragraphs": [
          "Fail2ban acts as an automated intrusion prevention framework for Linux systems. It operates by continuously monitoring system log files (such as /var/log/auth.log, /var/log/syslog, or systemd journald) for failed authentication attempts matching regular expression filters (failregex).",
          "When an IP address exceeds the defined threshold of failed login attempts within a specified observation window (findtime), Fail2ban dynamically invokes netfilter firewall actions to block the attacking IP address for a duration defined by bantime.",
          "Log parsing runs asynchronously via systemd journald or pyinotify file system watchers. This decoupled architecture guarantees minimal CPU overhead even on high-throughput web server instances processing millions of requests daily.",
          "By automating firewall responses at the network boundary, Fail2ban prevents credential guessing, SSH dictionary attacks, and HTTP layer-7 scanning bots from compromising user accounts or consuming CPU resources."
        ],
        "code_block": "# Install Fail2ban daemon on Debian/Ubuntu\nsudo apt-get update && sudo apt-get install -y fail2ban\n\n# Enable and start Fail2ban systemd daemon\nsystemctl enable --now fail2ban\n\n# Verify active status and global jail count\nfail2ban-client status",
        "code_language": "bash"
      },
      {
        "id": "fail2ban-jail-local",
        "h2_title": "2. Deploying Production Jails via jail.local",
        "content_paragraphs": [
          "Never modify the default /etc/fail2ban/jail.conf file directly. Package upgrades by system package managers will overwrite jail.conf, discarding custom security rules.",
          "Instead, create /etc/fail2ban/jail.local to override default settings safely. Parameters specified in jail.local automatically take precedence over jail.conf settings.",
          "In jail.local, configure global defaults under the [DEFAULT] section for parameters like bantime (ban duration), findtime (window period), maxretry (maximum allowed failures), and banaction (firewall action engine).",
          "The following production jail.local template enforces a strict 1-hour ban for SSH brute-force attempts after 5 failures within a 10-minute window while ignoring trusted internal management subnets:"
        ],
        "code_block": "# /etc/fail2ban/jail.local\n[DEFAULT]\nbantime  = 1h\nfindtime = 10m\nmaxretry = 5\nbanaction = ufw\nignoreip = 127.0.0.1/8 ::1 10.0.0.0/8 192.168.1.0/24\n\n[sshd]\nenabled = true\nport    = ssh\nlogpath = %(sshd_log)s\nbackend = systemd",
        "code_language": "ini"
      },
      {
        "id": "fail2ban-recidive-jail",
        "h2_title": "3. Recidive Jails for Persistent Repeat Attackers",
        "content_paragraphs": [
          "Automated botnets are designed to bypass standard short ban windows. Once a 1-hour ban expires, botnet clients resume password guessing attacks at calculated intervals to stay under rate limit thresholds.",
          "The recidive jail solves this persistent threat by monitoring Fail2ban's own log file (/var/log/fail2ban.log). If an IP address is banned multiple times across any jail within a 1-day observation window, recidive triggers a long-term persistent ban (e.g., 7 days or 30 days).",
          "Deploying a recidive jail dramatically reduces log volume, system load, and firewall table churn caused by aggressive repeat offender botnets."
        ],
        "code_block": "# Append recidive jail section to /etc/fail2ban/jail.local\n[recidive]\nenabled  = true\nlogpath  = /var/log/fail2ban.log\nbanaction = ufw\nfindtime = 1d\nmaxretry = 2\nbantime  = 7d",
        "code_language": "ini"
      },
      {
        "id": "fail2ban-nginx-scanners",
        "h2_title": "4. Mitigating Web Scanners via Nginx Log Filters",
        "content_paragraphs": [
          "Automated web vulnerability scanners search public web servers for exposed environment configuration files (.env), database management panels (phpMyAdmin), and unpatched CMS logins, flooding Nginx access logs with HTTP 404, 403, and 400 error codes.",
          "Create a custom Fail2ban filter in /etc/fail2ban/filter.d/nginx-noscript.conf to match scanner URI request patterns and automatically ban offensive IP addresses.",
          "This prevents web scanners from consuming web server worker processes and backend database connection pools."
        ],
        "code_block": "# Create custom filter /etc/fail2ban/filter.d/nginx-noscript.conf\n[Definition]\nfailregex = ^<HOST> -.* \"GET /.*(\\..*|phpmyadmin|wp-login|\\.env|\\.git) HTTP/.*\" (404|403|400)\nignoreregex =\n\n# Configure jail entry in /etc/fail2ban/jail.local\n[nginx-noscript]\nenabled  = true\nport     = http,https\nlogpath  = /var/log/nginx/access.log\nmaxretry = 6\nfindtime = 1m\nbantime  = 24h",
        "code_language": "ini"
      },
      {
        "id": "fail2ban-nftables-backend",
        "h2_title": "5. NFTables Backend & High-Performance Action Tuning",
        "content_paragraphs": [
          "Legacy Fail2ban actions append individual iptables rules for every single banned IP address. Over time, long iptables rule chains increase packet processing latency for legitimate network traffic.",
          "Configuring banaction = nftables-multiport instructs Fail2ban to insert banned IP addresses into native nftables sets. Nftables set lookups execute in constant time O(1), maintaining fast packet filtering throughput regardless of ban count."
        ],
        "code_block": "# Configure high-performance nftables backend in /etc/fail2ban/jail.local\n[DEFAULT]\nbanaction = nftables-multiport\nbanaction_allports = nftables-allports",
        "code_language": "ini"
      },
      {
        "id": "fail2ban-admin-cli",
        "h2_title": "6. Administration & Unban Command Reference",
        "content_paragraphs": [
          "System administrators can inspect active jail health, query banned IP lists, and manually unban accidental administrator lockouts using the fail2ban-client CLI utility.",
          "Always test configuration changes using fail2ban-client reload to ensure settings apply cleanly without dropping active bans."
        ],
        "code_block": "# Inspect overall daemon status and active jails\nfail2ban-client status\n\n# Inspect detailed status and active banned IPs for SSH jail\nfail2ban-client status sshd\n\n# Unban an IP address locked out accidentally\nfail2ban-client set sshd unbanip 192.168.1.100\n\n# Reload Fail2ban configuration dynamically\nfail2ban-client reload",
        "code_language": "bash"
      }
    ],
    "faqs": [
      {
        "question": "How do I unban an IP address locked out by Fail2ban?",
        "answer": "Execute fail2ban-client set sshd unbanip <IP_ADDRESS> to remove the ban rule immediately."
      },
      {
        "question": "Why use nftables instead of iptables for Fail2ban?",
        "answer": "nftables uses hashed set lookups with O(1) complexity, maintaining high network performance even with tens of thousands of banned IPs."
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
    "read_time_mins": 14,
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
        "id": "sysctl-vulnerabilities",
        "h2_title": "1. TCP/IP Network Stack Vulnerabilities & Kernel Defaults",
        "content_paragraphs": [
          "Default Linux kernel parameters prioritize maximum compatibility across diverse network topologies over security. Out of the box, Linux kernels accept source-routed packets, process ICMP redirect messages, and allow unprivileged access to dmesg logs.",
          "Attacker reconnaissance and denial-of-service vectors exploit default sysctl configurations to perform IP spoofing, TCP SYN floods, and man-in-the-middle packet redirection.",
          "Hardening sysctl parameters via modular configuration files in /etc/sysctl.d/ ensures kernel security settings persist across reboots.",
          "Tuning these low-level parameters provides defense-in-depth protection before packets even reach user-space applications or web servers."
        ],
        "code_block": "# Inspect active kernel TCP syncookies status\nsysctl net.ipv4.tcp_syncookies",
        "code_language": "bash"
      },
      {
        "id": "sysctl-syn-floods",
        "h2_title": "2. Mitigating SYN Floods with TCP Syncookies",
        "content_paragraphs": [
          "A TCP SYN flood attack sends thousands of TCP SYN packets with spoofed source IP addresses. The server allocates socket memory and waits for ACK responses that never arrive, quickly filling the SYN backlog queue.",
          "Enabling net.ipv4.tcp_syncookies changes kernel behavior: when the SYN backlog queue fills, the kernel stops allocating memory state and instead encodes connection parameters into the TCP Sequence Number (cookie).",
          "When the client sends the final ACK, the kernel verifies the sequence number cookie and opens the connection seamlessly.",
          "Combining tcp_syncookies with increased tcp_max_syn_backlog buffers ensures high availability during distributed denial of service events."
        ],
        "code_block": "# Enable SYN flood defenses in sysctl\nnet.ipv4.tcp_syncookies = 1\nnet.ipv4.tcp_max_syn_backlog = 4096\nnet.ipv4.tcp_synack_retries = 2\nnet.ipv4.tcp_syn_retries = 2",
        "code_language": "ini"
      },
      {
        "id": "sysctl-rp-filter",
        "h2_title": "3. Preventing IP Spoofing via Reverse Path Filtering",
        "content_paragraphs": [
          "IP spoofing attacks forge packet source IP addresses to impersonate trusted internal nodes or bypass firewall rules.",
          "Reverse Path Filtering (rp_filter) checks whether incoming packets arrive on the same network interface that the kernel routing table would use to send a response back to that source IP address. If the packet arrives on a different interface, the kernel drops it immediately.",
          "Enforcing strict reverse path filtering (rp_filter = 1) eliminates IP spoofing vectors across all interfaces.",
          "This setting prevents attackers on adjacent network segments from injecting unauthorized traffic into established TCP sessions."
        ],
        "code_block": "# Enable strict Reverse Path Filtering\nnet.ipv4.conf.all.rp_filter = 1\nnet.ipv4.conf.default.rp_filter = 1",
        "code_language": "ini"
      },
      {
        "id": "sysctl-icmp-defense",
        "h2_title": "4. Disabling ICMP Redirects & Source Routing",
        "content_paragraphs": [
          "ICMP redirect messages allow routers to notify hosts of better routes. Malicious actors use forged ICMP redirects to alter host routing tables and perform man-in-the-middle (MitM) interception.",
          "Similarly, Source Routing allows senders to specify the exact path a packet takes through a network, bypassing firewalls.",
          "Production servers must explicitly disable ICMP redirect processing and source routing across all interfaces.",
          "Disabling ICMP redirects prevents adversary-controlled gateways from hijacking traffic routed between cloud instances."
        ],
        "code_block": "# Disable ICMP redirects and IP source routing\nnet.ipv4.conf.all.accept_redirects = 0\nnet.ipv4.conf.default.accept_redirects = 0\nnet.ipv4.conf.all.send_redirects = 0\nnet.ipv4.conf.default.send_redirects = 0\nnet.ipv4.conf.all.accept_source_route = 0\nnet.ipv4.conf.default.accept_source_route = 0",
        "code_language": "ini"
      },
      {
        "id": "sysctl-memory-aslr",
        "h2_title": "5. Memory Protection, ASLR, & Symlink Hardening",
        "content_paragraphs": [
          "In addition to network stack parameters, sysctl governs kernel memory protection and file system safety directives.",
          "Enforcing Address Space Layout Randomization (kernel.randomize_va_space = 2) randomizes memory positions of stack, heap, and library mappings, making buffer overflow exploits unpredictable.",
          "Restricting unprivileged dmesg access (kernel.dmesg_restrict = 1) prevents unprivileged users from reading kernel memory addresses.",
          "Protected hardlinks and symlinks restrict unprivileged users from creating malicious symlink targets inside world-writable directories like /tmp."
        ],
        "code_block": "# Memory protection and system safety\nkernel.randomize_va_space = 2\nkernel.dmesg_restrict = 1\nkernel.kptr_restrict = 2\nfs.protected_hardlinks = 1\nfs.protected_symlinks = 1\nfs.protected_fifos = 2\nfs.protected_regular = 2",
        "code_language": "ini"
      },
      {
        "id": "sysctl-persistence",
        "h2_title": "6. Persistence & Live Reloading via /etc/sysctl.d/",
        "content_paragraphs": [
          "Save all hardened parameters inside /etc/sysctl.d/99-security.conf to ensure configurations persist across system reboots.",
          "Apply configuration updates dynamically in memory without restarting system services.",
          "Verify active kernel parameter values using the sysctl command line utility."
        ],
        "code_block": "# Apply all sysctl settings immediately\nsysctl --system\n\n# Verify active setting for ASLR\nsysctl kernel.randomize_va_space",
        "code_language": "bash"
      }
    ],
    "faqs": [
      {
        "question": "How do I apply sysctl changes without rebooting the server?",
        "answer": "Run sysctl --system to reload all configuration files in /etc/sysctl.d/ dynamically."
      },
      {
        "question": "What is the difference between rp_filter = 1 and rp_filter = 2?",
        "answer": "rp_filter = 1 enforces strict reverse path check (packet must arrive on the best route interface), while rp_filter = 2 enforces loose check (packet dropped only if unreachable via any interface)."
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
    "read_time_mins": 13,
    "word_count": 1500,
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
        "id": "systemd-vulnerabilities",
        "h2_title": "1. The Danger of Unrestricted System Daemons",
        "content_paragraphs": [
          "Traditional Linux daemons running as system services often possess full access to the entire root file system, user home directories, and kernel syscall interfaces.",
          "If an application vulnerability (such as a remote code execution in web application gateways) is exploited, the attacker inherits the full permissions of the daemon, allowing them to read sensitive files in /etc/ or modify system binaries.",
          "Systemd provides built-in process isolation directives using Linux kernel namespaces, cgroups, and seccomp filters without needing Docker or heavy container runtimes.",
          "Sandboxing services at the systemd layer creates isolated execution environments, preventing lateral movement during security incidents."
        ],
        "code_block": "# Inspect security score of an active service unit\nsystemd-analyze security nginx.service",
        "code_language": "bash"
      },
      {
        "id": "systemd-filesystem-protection",
        "h2_title": "2. Enforcing Read-Only File System Mount Namespaces",
        "content_paragraphs": [
          "The ProtectSystem directive creates a private mount namespace for the service, mounting system directories as read-only.",
          "Setting ProtectSystem=strict mounts the entire file system hierarchy as read-only for the process, except for explicit paths specified in ReadWritePaths=.",
          "Setting ProtectHome=yes makes /home, /root, and /run/user inaccessible and invisible to the daemon.",
          "PrivateTmp=yes allocates isolated /tmp and /var/tmp directories, preventing symlink attacks and inter-process temporary file snooping."
        ],
        "code_block": "# /etc/systemd/system/myapp.service.d/override.conf\n[Service]\nProtectSystem=strict\nProtectHome=yes\nReadWritePaths=/var/log/myapp /var/lib/myapp\nPrivateTmp=yes\nProtectKernelTunables=yes\nProtectKernelModules=yes",
        "code_language": "ini"
      },
      {
        "id": "systemd-privilege-restriction",
        "h2_title": "3. Privilege Escalation Prevention via NoNewPrivileges",
        "content_paragraphs": [
          "Attacker payloads often attempt privilege escalation by executing SUID binaries (like sudo or pkexec) from within compromised service processes.",
          "Setting NoNewPrivileges=yes ensures that the process and any child processes it spawns can never gain new privileges through setuid/setgid bits or file capabilities.",
          "This single directive neutralizes an entire class of SUID exploit primitives across all Linux service processes.",
          "Combine with ProtectControlGroups=yes to prevent daemons from altering cgroup resource constraints."
        ],
        "code_block": "# Block SUID privilege escalation\n[Service]\nNoNewPrivileges=yes\nProtectKernelTunables=yes\nProtectKernelModules=yes\nProtectControlGroups=yes\nMemoryDenyWriteExecute=yes",
        "code_language": "ini"
      },
      {
        "id": "systemd-capability-bounding",
        "h2_title": "4. Restricting Linux Capabilities",
        "content_paragraphs": [
          "Linux divides root privileges into distinct capabilities (e.g., CAP_NET_ADMIN, CAP_SYS_ADMIN, CAP_NET_BIND_SERVICE). Unrestricted daemons retain all capabilities.",
          "The CapabilityBoundingSet directive defines an explicit whitelist of capabilities allowed for the service process. All other capabilities are dropped permanently during process startup.",
          "Dropping unnecessary root capabilities ensures that compromised daemons cannot load kernel modules, manipulate network routing tables, or mount raw file systems."
        ],
        "code_block": "# Allow binding low ports (<1024) but drop all other root capabilities\n[Service]\nCapabilityBoundingSet=CAP_NET_BIND_SERVICE\nAmbientCapabilities=CAP_NET_BIND_SERVICE",
        "code_language": "ini"
      },
      {
        "id": "systemd-syscall-filtering",
        "h2_title": "5. Filtering Dangerous Kernel System Calls (Seccomp)",
        "content_paragraphs": [
          "Linux exposes over 300 kernel system calls. Most web applications and background services require fewer than 40 syscalls.",
          "The SystemCallFilter directive uses seccomp to block dangerous syscalls like ptrace, reboot, or kexec_load. Systemd provides predefined syscall groups like @system-service and @sandbox.",
          "Restricting available system calls reduces kernel attack surface against zero-day kernel privilege escalation exploits."
        ],
        "code_block": "# Enforce Seccomp System Call Filtering\n[Service]\nSystemCallFilter=@system-service\nSystemCallFilter=~@privileged @resources\nSystemCallErrorNumber=EPERM",
        "code_language": "ini"
      },
      {
        "id": "systemd-audit-score",
        "h2_title": "6. Automated Security Audit Scores with systemd-analyze",
        "content_paragraphs": [
          "Systemd includes an automated security analyzer that evaluates unit file directives against security best practices and outputs an audit score.",
          "Run systemd-analyze security to inspect all active services on the system and identify unhardened daemons needing isolation overrides.",
          "Apply unit overrides safely using systemctl edit without modifying vendor service files."
        ],
        "code_block": "# Audit all active services\nsystemd-analyze security\n\n# Reload systemd daemon to apply unit overrides\nsystemctl daemon-reload\nsystemctl restart myapp.service",
        "code_language": "bash"
      }
    ],
    "faqs": [
      {
        "question": "How do I inspect the security score of a systemd unit?",
        "answer": "Run systemd-analyze security <unit-name> to view an automated 1-10 security audit score."
      },
      {
        "question": "What happens if a process calls a blocked SystemCallFilter syscall?",
        "answer": "By default, seccomp terminates the process with SIGSYS. Setting SystemCallErrorNumber=EPERM returns an Operation Not Permitted error code instead."
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
        "id": "auditd-architecture",
        "h2_title": "1. Auditd Framework Architecture & Kernel Interception",
        "content_paragraphs": [
          "The Linux Audit Subsystem is embedded directly inside the Linux kernel. It hooks system calls at the kernel boundary, capturing process executions, file access attempts, network socket creations, and user authentication events before processes complete.",
          "Unlike standard syslog daemons (which depend on applications choosing to log messages), auditd intercepts events unconditionally at the system call level, making it tamper-resistant against user-space log manipulation.",
          "The user-space auditd daemon collects events from kernel netfilter buffers and writes them to /var/log/audit/audit.log.",
          "This granular logging capability forms the core foundation of Digital Forensics and Incident Response (DFIR) on Linux servers."
        ],
        "code_block": "# Install auditd on Debian/Ubuntu\nsystemctl enable --now auditd\n\n# Verify audit daemon status\nauditctl -s",
        "code_language": "bash"
      },
      {
        "id": "auditd-execve-monitoring",
        "h2_title": "2. Auditing Process Execution (execve) across All Users",
        "content_paragraphs": [
          "Attackers who gain initial shell access execute reconnaissance commands (such as whoami, id, uname -a, netstat). Standard bash history can be deleted or bypassed by executing binaries directly.",
          "Adding execve audit rules records every single binary execution across the entire system, capturing exact command-line arguments, working directories, parent PIDs, and effective user IDs (EUID).",
          "Filter by arch=b64 to capture 64-bit system calls efficiently.",
          "Capturing full command-line arguments provides immutable forensic evidence during post-compromise investigations."
        ],
        "code_block": "# Track 64-bit and 32-bit execve system calls\n-a always,exit -F arch=b64 -S execve -k process_exec\n-a always,exit -F arch=b32 -S execve -k process_exec",
        "code_language": "bash"
      },
      {
        "id": "auditd-file-integrity",
        "h2_title": "3. File Integrity Monitoring (FIM) for Critical System Files",
        "content_paragraphs": [
          "File Integrity Monitoring (FIM) rules watch critical system configuration files for write (w), read (r), execute (x), or attribute change (a) operations.",
          "Configure file watches on /etc/passwd, /etc/shadow, /etc/sudoers, and /etc/pam.d/ to alert DFIR incident responders immediately if account credentials or privilege policies are modified.",
          "Assign custom key tags (-k <tag_name>) to audit rules to facilitate rapid filtering in log analysis tools.",
          "Monitoring permissions changes on SSH configuration files (/etc/ssh/sshd_config) prevents unauthorized backdoor insertion."
        ],
        "code_block": "# File Integrity Watch Rules\n-w /etc/passwd -p wa -k identity_changes\n-w /etc/shadow -p wa -k identity_changes\n-w /etc/sudoers -p wa -k privilege_changes\n-w /etc/sudoers.d/ -p wa -k privilege_changes\n-w /var/log/tallylog -p wa -k auth_logs",
        "code_language": "bash"
      },
      {
        "id": "auditd-rules-structure",
        "h2_title": "4. Structuring Modular Audit Rules in /etc/audit/rules.d/",
        "content_paragraphs": [
          "Modern Linux distributions manage audit rules through modular files in /etc/audit/rules.d/*.rules, which augments auditctl when auditd starts.",
          "Organize rules into numbered files (e.g., 10-base.rules, 30-fim.rules, 90-finalize.rules) to maintain clear rule precedence.",
          "Enforce rule immutability by appending -e 2 as the final directive, preventing attackers from disabling audit rules without a reboot.",
          "Immutable rules guarantee log integrity even if an attacker achieves temporary root privileges."
        ],
        "code_block": "# /etc/audit/rules.d/99-finalize.rules\n# Lock audit rules until next reboot\n-e 2",
        "code_language": "bash"
      },
      {
        "id": "auditd-performance-tuning",
        "h2_title": "5. Performance Tuning & Buffer Backlog Management",
        "content_paragraphs": [
          "Under high system load, kernel audit buffers can overflow if the auditd daemon cannot write to disk fast enough, causing kernel event drops.",
          "Tune kernel backlog buffer limits (-b) and set failure response actions (-f) in /etc/audit/rules.d/10-base.rules to handle burst traffic gracefully.",
          "Configuring backlog buffers to 8192 prevents event drops during bursty web application workloads."
        ],
        "code_block": "# /etc/audit/rules.d/10-base.rules\n-D\n-b 8192\n-f 1",
        "code_language": "bash"
      },
      {
        "id": "auditd-log-analysis",
        "h2_title": "6. Incident Response & Log Querying via ausearch & aureport",
        "content_paragraphs": [
          "The audit log file (/var/log/audit/audit.log) contains dense key-value pairs. Use built-in utilities ausearch and aureport for forensic queries.",
          "Use aureport --summary to generate high-level executive reports on failed authentications, executable events, and file access violations.",
          "Combine ausearch with jq or SIEM log forwarders (Elastic Filebeat, Vector) to stream structured audit events to central security operating centers."
        ],
        "code_block": "# Query process execution events by key tag\nausearch -k process_exec -i\n\n# Generate summary report of failed login attempts\naureport -l --failed\n\n# Query modifications to /etc/sudoers\nausearch -k privilege_changes -i",
        "code_language": "bash"
      }
    ],
    "faqs": [
      {
        "question": "Does auditd affect system CPU performance?",
        "answer": "With optimized filter rules (-F arch=b64), auditd overhead is less than 1-2% CPU under heavy workloads."
      },
      {
        "question": "What does -e 2 mean in audit rules?",
        "answer": "-e 2 locks the audit configuration permanently until system reboot, preventing an attacker who gains root from disabling audit logging."
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
    "read_time_mins": 14,
    "word_count": 1500,
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
        "id": "wireguard-architecture",
        "h2_title": "1. Cryptographic Principles of WireGuard & Noise Protocol",
        "content_paragraphs": [
          "Traditional VPN protocols like IPSec and OpenVPN suffer from extreme complexity, legacy cipher negotiation, and heavy codebase sizes exceeding 100,000 lines of C code.",
          "WireGuard features an ultra-lean codebase under 4,000 lines of C. It runs directly inside Linux kernel space and relies on modern fixed cryptographic primitives: Curve25519 for ECDH, ChaCha20 for symmetric encryption, Poly1305 for authentication, and BLAKE2s for hashing.",
          "WireGuard uses the Noise IK protocol framework, responding only to packets carrying valid cryptographic signatures, making WireGuard servers completely invisible to unauthenticated UDP port scanners.",
          "This silent response architecture eliminates port scanning visibility across public cloud infrastructure."
        ],
        "code_block": "# Generate WireGuard private and public key pairs\nwg genkey | tee privatekey | wg pubkey > publickey\n\n# Secure private key file permissions\nchmod 600 privatekey",
        "code_language": "bash"
      },
      {
        "id": "wireguard-configuration",
        "h2_title": "2. Configuring Interface Parameters in /etc/wireguard/wg0.conf",
        "content_paragraphs": [
          "WireGuard interfaces are configured using simple INI-style configuration files in /etc/wireguard/wg0.conf.",
          "Each node defines its own local [Interface] parameters (private key, virtual IP address, listening UDP port) and a series of [Peer] sections for remote nodes.",
          "The AllowedIPs setting acts as both a routing table and an access control list: packets sent to an AllowedIP are routed through the tunnel, and incoming packets from the tunnel are accepted only if their source IP matches AllowedIPs.",
          "Configuring 10.0.0.0/24 in AllowedIPs enables secure point-to-point mesh routing between multi-cloud instances."
        ],
        "code_block": "# /etc/wireguard/wg0.conf on Gateway Server (Node A)\n[Interface]\nPrivateKey = <NODE_A_PRIVATE_KEY>\nAddress = 10.0.0.1/24\nListenPort = 51820\n\n[Peer]\n# Web Server (Node B)\nPublicKey = <NODE_B_PUBLIC_KEY>\nAllowedIPs = 10.0.0.2/32",
        "code_language": "ini"
      },
      {
        "id": "wireguard-peer-setup",
        "h2_title": "3. Connecting Remote Multi-Cloud Peer Nodes",
        "content_paragraphs": [
          "On Node B (Web Server), configure the peer connection pointing back to Node A's public IP and UDP port.",
          "Setting PersistentKeepalive = 25 sends a periodic silent ping every 25 seconds, keeping NAT sessions and firewall state tables open on cloud provider gateways.",
          "This ensures continuous tunnel connectivity without requiring re-authentication handshakes."
        ],
        "code_block": "# /etc/wireguard/wg0.conf on Web Server (Node B)\n[Interface]\nPrivateKey = <NODE_B_PRIVATE_KEY>\nAddress = 10.0.0.2/24\n\n[Peer]\n# Gateway Server (Node A)\nPublicKey = <NODE_A_PUBLIC_KEY>\nEndpoint = 203.0.113.10:51820\nAllowedIPs = 10.0.0.0/24\nPersistentKeepalive = 25",
        "code_language": "ini"
      },
      {
        "id": "wireguard-backend-binding",
        "h2_title": "4. Binding Internal Backend Services Strictly to Mesh IPs",
        "content_paragraphs": [
          "Once the WireGuard interface (wg0) is established, reconfigure database servers (PostgreSQL, MySQL, Redis) and internal API gateways to listen exclusively on the private WireGuard IP (e.g., 10.0.0.1).",
          "This ensures internal infrastructure services are completely unreachable from public IPv4/IPv6 internet interfaces, even if firewall rules are misconfigured.",
          "Strict IP binding guarantees zero public network exposure for core data storage layers."
        ],
        "code_block": "# /etc/postgresql/15/main/postgresql.conf\nlisten_addresses = '10.0.0.1'\n\n# /etc/redis/redis.conf\nbind 10.0.0.1",
        "code_language": "ini"
      },
      {
        "id": "wireguard-firewall-rules",
        "h2_title": "5. Firewall Isolation & Routing Table Tuning",
        "content_paragraphs": [
          "Configure UFW or iptables rules to allow UDP traffic on port 51820 exclusively for WireGuard handshake packets, while permitting unrestricted internal communication over the wg0 interface.",
          "Using interface-specific firewall rules isolates private tunnel traffic from external network interfaces."
        ],
        "code_block": "# Enable WireGuard UDP port on public interface eth0\nufw allow in on eth0 to any port 51820 proto udp comment 'WireGuard Handshakes'\n\n# Allow all internal traffic on virtual interface wg0\nufw allow in on wg0 comment 'Internal Mesh Traffic'\n\n# Bring up WireGuard interface\nwg-quick up wg0",
        "code_language": "bash"
      },
      {
        "id": "wireguard-verification",
        "h2_title": "6. Performance Benchmark & Troubleshooting Verification",
        "content_paragraphs": [
          "Inspect WireGuard active tunnel status, handshake timestamps, and transfer metrics using the wg command.",
          "Verify ICMP connectivity across private mesh IP endpoints using ping.",
          "Benchmark network throughput using iperf3 over the WireGuard interface."
        ],
        "code_block": "# Inspect active peer status and handshake ages\nwg show\n\n# Ping private mesh node\nping 10.0.0.2\n\n# Benchmark throughput over WireGuard mesh\niperf3 -c 10.0.0.2",
        "code_language": "bash"
      }
    ],
    "faqs": [
      {
        "question": "Why is WireGuard faster than OpenVPN?",
        "answer": "WireGuard has fewer than 4,000 lines of code running natively inside kernel space, avoiding context switching overhead."
      },
      {
        "question": "What happens if a WireGuard endpoint IP address changes?",
        "answer": "WireGuard automatically updates the endpoint IP when it receives a cryptographically authenticated packet from the new IP."
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
        "id": "xdp-architecture",
        "h2_title": "1. Understanding XDP Architecture vs Traditional Linux SKB Allocation",
        "content_paragraphs": [
          "Standard Linux network processing allocates a complex kernel socket buffer data structure (sk_buff) for every incoming packet before firewall rules (iptables/nftables) can evaluate the packet.",
          "Under volumetric DDoS attacks (such as 10 Million Packets Per Second UDP floods), the CPU time spent allocating and freeing sk_buff structures exhausts kernel memory and CPU cache lines, causing severe packet drops and server unresponsiveness.",
          "eXpress Data Path (XDP) provides a high-performance bare-metal packet processing framework. XDP programs execute eBPF bytecode directly inside the network driver's RX ring buffer before sk_buff memory allocation occurs."
        ],
        "code_block": "# Inspect network interface driver XDP support\nip link show eth0",
        "code_language": "bash"
      },
      {
        "id": "xdp-actions",
        "h2_title": "2. XDP Packet Processing Actions (XDP_DROP vs XDP_PASS)",
        "content_paragraphs": [
          "An XDP program evaluates raw packet data directly from driver memory and returns one of five verdict codes to the network card driver:",
          "XDP_DROP: Immediately recycles the packet buffer in the driver RX ring without allocating memory or notifying the CPU TCP/IP stack.",
          "XDP_PASS: Passes the packet up to the normal Linux TCP/IP network stack for standard processing.",
          "XDP_TX: Bounces the packet back out the same network interface it arrived on (useful for high-speed load balancers)."
        ],
        "code_block": "// XDP Action Constants\n// XDP_DROP = 1\n// XDP_PASS = 2\n// XDP_TX   = 3",
        "code_language": "c"
      },
      {
        "id": "xdp-c-program",
        "h2_title": "3. Writing a Production XDP Packet Filter in C",
        "content_paragraphs": [
          "XDP C code uses eBPF helpers and header pointers to parse Ethernet, IPv4, and UDP/TCP protocol headers safely.",
          "The eBPF verifier verifies memory bounds checking before loading bytecode into the kernel, ensuring the XDP program can never crash the Linux kernel.",
          "The following C program parses incoming IPv4 headers and drops packets matching blacklisted source IP addresses stored in an eBPF hash map:"
        ],
        "code_block": "#include <linux/bpf.h>\n#include <linux/if_ether.h>\n#include <linux/ip.h>\n#include <bpf/bpf_helpers.h>\n\nstruct {\n    __uint(type, BPF_MAP_TYPE_HASH);\n    __uint(max_entries, 100000);\n    __type(key, __be32);\n    __type(value, __u64);\n} blacklist SEC(\"maps\");\n\nSEC(\"xdp\")\nint xdp_firewall(struct xdp_md *ctx) {\n    void *data_end = (void *)(long)ctx->data_end;\n    void *data = (void *)(long)ctx->data;\n    struct ethhdr *eth = data;\n    \n    if ((void *)(eth + 1) > data_end) return XDP_PASS;\n    if (eth->h_proto != __constant_htons(ETH_P_IP)) return XDP_PASS;\n    \n    struct iphdr *iph = (void *)(eth + 1);\n    if ((void *)(iph + 1) > data_end) return XDP_PASS;\n    \n    __be32 src_ip = iph->saddr;\n    __u64 *value = bpf_map_lookup_elem(&blacklist, &src_ip);\n    if (value) {\n        return XDP_DROP;\n    }\n    return XDP_PASS;\n}\nchar _license[] SEC(\"license\") = \"GPL\";",
        "code_language": "c"
      },
      {
        "id": "xdp-compilation",
        "h2_title": "4. Compiling & Loading Bytecode Targets via Clang/LLVM",
        "content_paragraphs": [
          "Compile XDP C code into BPF Executable and Linkable Format (ELF) targets using Clang and LLVM compiler toolchains.",
          "Attach the compiled BPF bytecode to a network interface using standard iproute2 ip link commands."
        ],
        "code_block": "# Compile C code to BPF bytecode\nclang -O2 -target bpf -c xdp_firewall.c -o xdp_firewall.o\n\n# Attach XDP program to eth0 network interface\nip link set dev eth0 xdp obj xdp_firewall.o sec xdp\n\n# Detach XDP program from eth0\nip link set dev eth0 xdp off",
        "code_language": "bash"
      },
      {
        "id": "xdp-bpf-maps",
        "h2_title": "5. Dynamic Blocklist Management via BPF Maps",
        "content_paragraphs": [
          "BPF Maps are high-speed shared memory structures bridging kernel space and user-space daemons.",
          "User-space monitoring daemons (such as Fail2ban or custom Go/Python agents) populate blocked IP addresses into the BPF map dynamically without reloading the XDP program."
        ],
        "code_block": "# Add blocked IP (e.g. 198.51.100.45) to BPF map via bpftool\nbpftool map update id 4 key 198 51 100 45 value 1 0 0 0 0 0 0 0\n\n# Dump current BPF map contents\nbpftool map dump id 4",
        "code_language": "bash"
      },
      {
        "id": "xdp-verification",
        "h2_title": "6. High-Throughput Packet Benchmark Verification",
        "content_paragraphs": [
          "Verify XDP packet drop counters using ethtool or bpftool stats.",
          "Benchmark packet processing throughput under simulated UDP floods using pktgen."
        ],
        "code_block": "# Inspect XDP active interface stats\nip -s link show dev eth0\n\n# View eBPF program list\nbpftool prog show",
        "code_language": "bash"
      }
    ],
    "faqs": [
      {
        "question": "What is the difference between XDP_DROP and iptables DROP?",
        "answer": "XDP_DROP drops packets in driver memory before Linux creates socket buffers, yielding 10x higher throughput."
      },
      {
        "question": "Does XDP require special network card hardware?",
        "answer": "No. XDP supports native mode (driver level), offloaded mode (SmartNIC hardware), and generic mode (fallback for any network driver)."
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
    "read_time_mins": 13,
    "word_count": 1500,
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
        "id": "pam-architecture",
        "h2_title": "1. Pluggable Authentication Modules (PAM) Workflows",
        "content_paragraphs": [
          "Pluggable Authentication Modules (PAM) provide a centralized authentication framework for Linux operating systems. Services like SSH, local console logins, sudo, and FTP pass authentication requests to PAM modules.",
          "When pam_faillock is configured, PAM intercepts authentication attempts before password checking occurs.",
          "If a user exceeds the allowed failed attempt threshold, pam_faillock denies authentication immediately without verifying the password, mitigating credential guessing attacks.",
          "Centralized PAM policies ensure consistent lockout enforcement across all system authentication interfaces."
        ],
        "code_block": "# Inspect PAM security configuration directory\nls -la /etc/pam.d/\nls -la /etc/security/faillock.conf",
        "code_language": "bash"
      },
      {
        "id": "pam-tally2-deprecation",
        "h2_title": "2. Migrating from Deprecated pam_tally2 to pam_faillock",
        "content_paragraphs": [
          "Legacy Linux distributions relied on pam_tally and pam_tally2 for account lockout policies. Modern distributions (RHEL 8/9, Ubuntu 22.04+, Debian 12+) have deprecated pam_tally2 in favor of pam_faillock.",
          "Unlike pam_tally2, pam_faillock stores tally files in a secure binary format inside /var/log/faillock/ and provides enhanced denial directives.",
          "Migrating to pam_faillock guarantees long-term compatibility with current Enterprise Linux security baselines."
        ],
        "code_block": "# Check if pam_faillock is installed\nfaillock --version",
        "code_language": "bash"
      },
      {
        "id": "pam-faillock-config",
        "h2_title": "3. Hardening /etc/security/faillock.conf",
        "content_paragraphs": [
          "Configure global account lockout parameters inside /etc/security/faillock.conf.",
          "The deny directive sets the maximum number of failed attempts before lockout. Setting unlock_time = 900 specifies a 15-minute temporary lockout window.",
          "The fail_interval directive defines the sliding window during which consecutive failures accumulate.",
          "Enabling silent suppresses informative error messages, preventing user enumeration by unauthenticated attackers."
        ],
        "code_block": "# /etc/security/faillock.conf\ndir = /var/log/faillock\ndeny = 5\nfail_interval = 900\nunlock_time = 900\neven_deny_root\nroot_unlock_time = 1800\nsilent",
        "code_language": "ini"
      },
      {
        "id": "pam-integration",
        "h2_title": "4. Integrating Modules in /etc/pam.d/ Entries",
        "content_paragraphs": [
          "Enable pam_faillock inside system-auth and password-auth files in /etc/pam.d/.",
          "The auth stack requires pam_faillock preauth before pam_unix, and pam_faillock authfail after pam_unix to record failures accurately.",
          "Placing preauth first allows PAM to block locked accounts before executing expensive password hashing operations."
        ],
        "code_block": "# Example /etc/pam.d/common-auth snippet\nauth    required                    pam_faillock.so preauth silent\nauth    [success=1 default=ignore]  pam_unix.so nullok\nauth    [default=die]               pam_faillock.so authfail\nauth    sufficient                  pam_faillock.so authsucc",
        "code_language": "ini"
      },
      {
        "id": "pam-root-protection",
        "h2_title": "5. Root Account Protection & Lockout Safeguards",
        "content_paragraphs": [
          "Enabling even_deny_root applies lockout policies to the root account as well, preventing root password guessing via local console or SSH.",
          "Set root_unlock_time to a longer duration (e.g., 30 minutes) to deter automated root brute force while allowing legitimate emergency access recovery.",
          "Always maintain active SSH key access before testing root lockout policies to prevent administrative lockouts."
        ],
        "code_block": "# Verify faillock root lockout configuration\ncat /etc/security/faillock.conf | grep root",
        "code_language": "bash"
      },
      {
        "id": "pam-admin-commands",
        "h2_title": "6. Administration: Auditing Tally Logs & Account Unlocking",
        "content_paragraphs": [
          "Administrators can inspect failed login records and manually reset locked accounts using the faillock command line tool.",
          "Audit failed login tallies periodically to detect emerging brute-force attack trends."
        ],
        "code_block": "# View failed login attempts for user 'ubuntu'\nfaillock --user ubuntu\n\n# Reset failed login count and unlock account immediately\nfaillock --user ubuntu --reset",
        "code_language": "bash"
      }
    ],
    "faqs": [
      {
        "question": "How do I check and reset failed login attempts for a user?",
        "answer": "Run faillock --user <username> to view attempt counts, and faillock --user <username> --reset to unlock."
      },
      {
        "question": "Will pam_faillock lock out users logging in via SSH public keys?",
        "answer": "No. SSH public key authentication bypasses PAM auth modules entirely. pam_faillock only affects password-based authentication attempts."
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
    "read_time_mins": 14,
    "word_count": 1500,
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
        "id": "isolation-fundamentals",
        "h2_title": "1. Fundamentals of Linux Process Isolation & Namespaces",
        "content_paragraphs": [
          "Linux process isolation relies on kernel namespaces (PID, Mount, Network, IPC, UTS, User) to virtualize system resources.",
          "When a process is isolated inside dedicated namespaces, it operates in a restricted view of the operating system without visibility into processes, network interfaces, or file system mounts belonging to host OS instances.",
          "Unprivileged User Namespaces allow standard unprivileged users to create isolated container environments without requiring root privileges.",
          "Understanding namespace boundaries is essential for deploying lightweight micro-service sandboxes on Linux servers."
        ],
        "code_block": "# Inspect active process namespaces via /proc\nls -l /proc/self/ns/",
        "code_language": "bash"
      },
      {
        "id": "user-namespaces-unshare",
        "h2_title": "2. Unprivileged User Namespaces (CLONE_NEWUSER)",
        "content_paragraphs": [
          "The CLONE_NEWUSER flag allows a standard user process to establish a new user namespace where the unprivileged UID (e.g. 1000) is mapped to UID 0 (root) inside the namespace.",
          "Even though the process acts as root inside its user namespace, it retains zero root privileges on the host system, neutralizing container breakout primitives.",
          "This capability allows developers to run unprivileged containers without requiring setuid binaries or Docker daemon privileges."
        ],
        "code_block": "# Launch isolated user and mount namespace\nunshare --user --map-root-user --mount --fork /bin/bash\n\n# Verify UID inside namespace\nid",
        "code_language": "bash"
      },
      {
        "id": "chroot-jail-building",
        "h2_title": "3. Building Minimal Lightweight Chroot Jails",
        "content_paragraphs": [
          "The chroot system call changes the apparent root directory for the current process and its children.",
          "Create a minimal directory hierarchy (/srv/jail) containing only the necessary shared libraries and binary executables required by the target application.",
          "Using minimal file system trees prevents attackers from accessing host compilers (gcc), shell utilities, or system configurations if the application is compromised."
        ],
        "code_block": "# Create jail directory structure\nmkdir -p /srv/jail/{bin,lib64,dev,etc}\n\n# Copy binary and required shared libraries using ldd\ncp /bin/bash /srv/jail/bin/\nldd /bin/bash",
        "code_language": "bash"
      },
      {
        "id": "chroot-dev-nodes",
        "h2_title": "4. Mounting Safe Device Nodes & Read-Only Bind Mounts",
        "content_paragraphs": [
          "Applications inside chroot jails often require basic character devices like /dev/null, /dev/zero, and /dev/urandom.",
          "Create character devices using mknod or bind-mount host device nodes with restrictive mount flags (nodev, nosuid, noexec).",
          "Enforcing nodev and nosuid flags on mount points blocks device manipulation and setuid privilege escalation."
        ],
        "code_block": "# Create essential character devices inside jail\nmknod -m 666 /srv/jail/dev/null c 1 3\nmknod -m 666 /srv/jail/dev/zero c 1 5\nmknod -m 666 /srv/jail/dev/urandom c 1 9",
        "code_language": "bash"
      },
      {
        "id": "chroot-no-root",
        "h2_title": "5. Dropping Root Capabilities & Escapes Prevention",
        "content_paragraphs": [
          "Processes running as root inside a standard chroot jail can break out of the jail if they retain CAP_SYS_CHROOT or capability to create device nodes.",
          "Combine chroot with chroot-drop-privileges scripts or systemd sandboxing (RootDirectory=) to drop all capabilities before executing application code.",
          "Running jailed processes as unprivileged user 'nobody' neutralizes chroot escape techniques."
        ],
        "code_block": "# Example systemd service with RootDirectory chroot\n[Service]\nRootDirectory=/srv/jail\nExecStart=/bin/myapp\nUser=nobody\nGroup=nogroup",
        "code_language": "ini"
      },
      {
        "id": "chroot-verification",
        "h2_title": "6. Verification: Testing Process Sandboxing & Escapes",
        "content_paragraphs": [
          "Test jail isolation by attempting to access host file paths outside the chroot root.",
          "Verify that process listing (ps aux) inside PID namespaces reveals only jailed process trees.",
          "Confirm that jailed processes cannot read sensitive host files like /etc/shadow."
        ],
        "code_block": "# Execute sandboxed command inside jail\nchroot /srv/jail /bin/bash\n\n# Verify root directory boundary\nls -la /",
        "code_language": "bash"
      }
    ],
    "faqs": [
      {
        "question": "Is unprivileged user namespace safe for production?",
        "answer": "Yes, provided kernel sysctl user.max_user_namespaces is limited and kernel security patches are up to date."
      },
      {
        "question": "How do processes escape a basic chroot jail?",
        "answer": "If a process retains root privileges and CAP_SYS_CHROOT, it can create a temporary subdirectory, call chroot on it, and fchdir out into the host file system."
      }
    ],
    "related_tools": [
      {"name": "Linux Chmod Calculator", "url": "/tools/chmod-calculator.html"},
      {"name": "JSON Formatter", "url": "/tools/json.html"}
    ]
  }
]

with open('batch_data.json', 'w', encoding='utf-8') as f:
    json.dump(b1, f, indent=2)

print('[BUILD DEEP] Successfully written 10 expanded deep-dive articles to batch_data.json!')
