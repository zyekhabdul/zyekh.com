# ARTICLE-CONTENT-DRIVEN AI IMAGE PROMPTS (TECH INFOGRAPHIC & TYPOGRAPHY STRATEGY)

This document defines unique, content-driven AI image generation prompts for technical article thumbnails and hero graphics on `zyekh.com`.

---

## OPERATIONAL PROTOCOL (MANDATORY FOR GEMINI WEB)

- **CRITICAL OPERATIONAL RULE**: **1 PROMPT = 1 NEW CHAT SESSION (NEW CHAT)**.
- Never generate multiple article thumbnails within the *same* Gemini Web chat thread. In-session context causes Gemini to inherit layout biases and duplicate object angles across images.
- Always open a **Fresh New Chat** (`New Chat`) in Gemini Web for each article prompt to guarantee 100% unique composition.

---

## REVISED CORE STRATEGY: TECHNICAL INFOGRAPHIC & CLEAR TYPOGRAPHY

1. **Rejection of Pure Abstract Renders**: Pure abstract 3D sci-fi shapes without text create visual ambiguity ("what is this image?"). Images must look like high-tech developer infographics, architecture diagrams, or technical hero banners.
2. **Explicit Technical Headers & Labels**: Prompts explicitly include clear, bold technical text (article title, software name, protocol badges) to immediately convey the subject matter.
3. **High-Legibility Developer Aesthetic**: Visual style combines dark cyber/terminal themes, crisp vector diagram overlays, server architecture elements, and legible technical typography.
4. **Aspect Ratio**: `16:9` (`--ar 16:9`).

---

## PROMPT COLLECTION DERIVED FROM ARTICLE CONTENT

### 1. Nginx Reverse Proxy Hardening
- **Topic**: TLS 1.3, Rate Limiting, & Buffer Overflow Defense.
- **Header Text**: `"NGINX REVERSE PROXY HARDENING"`
- **Badges**: `"TLS 1.3 | RATE LIMITING | WAF"`
- **Prompt**:
```text
High-tech developer infographic banner for Nginx Reverse Proxy Security Hardening. 3D isometric server gateway node with glowing emerald green data streams and security shields. Bold, crisp, legible white technical title text at the top reading "NGINX REVERSE PROXY HARDENING" and sub-header "TLS 1.3 | RATE LIMITING | WAF". Dark cybernetic background, clean architecture diagram overlays, ultra-detailed 8k render --ar 16:9
```

### 2. UFW Firewall Hardening & Rate Limiting
- **Topic**: Default-Deny Policies & Native Port Rate Limiting.
- **Header Text**: `"UFW FIREWALL BLUEPRINT"`
- **Badges**: `"DEFAULT-DENY | PORT RATE LIMITING"`
- **Prompt**:
```text
Futuristic cybersecurity infographic hero graphic. Glowing orange digital firewall fortress wall protecting server racks, dropping unauthorized IP probes. Clear, bold, highly legible white technical text header reading "UFW FIREWALL BLUEPRINT" with subtitle "DEFAULT-DENY | PORT RATE LIMITING". Dark slate environment, vibrant electric blue and orange lighting, clean technical diagram UI --ar 16:9
```

### 3. Fail2ban Intrusion Prevention & SSH Abuse
- **Topic**: Log-based IP Banning & Recidive Jails.
- **Header Text**: `"FAIL2BAN INTRUSION PREVENTION"`
- **Badges**: `"SSH BRUTE-FORCE DEFENSE"`
- **Prompt**:
```text
Cyber Incident Response dashboard banner. High-tech security vault door sealing shut against red brute-force entry probes. Bold, crisp, highly legible white technical title reading "FAIL2BAN INTRUSION PREVENTION" and badge "SSH BRUTE-FORCE DEFENSE". Dark server room background, glowing crimson red and gold telemetry UI overlays, 8k render --ar 16:9
```

### 4. Linux Kernel Sysctl Hardening
- **Topic**: TCP/IP Stack Security, SYN Cookies, & Reverse Path Filtering.
- **Header Text**: `"LINUX SYSCTL HARDENING"`
- **Badges**: `"TCP/IP STACK SECURITY | SYN COOKIES"`
- **Prompt**:
```text
Linux kernel architecture technical diagram graphic. 3D microprocessor engine routing blue TCP data highways and absorbing SYN floods with cryptographic energy badges. Bold, sharp, legible white typography reading "LINUX SYSCTL HARDENING" and sub-header "TCP/IP STACK SECURITY | SYN COOKIES". Dark metallic circuit grid, electric cyan lighting --ar 16:9
```

### 5. Systemd Service Sandboxing
- **Topic**: Seccomp Syscall Filtering & Read-Only Mount Namespaces.
- **Header Text**: `"SYSTEMD SERVICE SANDBOXING"`
- **Badges**: `"SECCOMP | NAMESPACES | READ-ONLY"`
- **Prompt**:
```text
Process isolation technical blueprint hero graphic. Transparent violet glass containment cube isolating a glowing process core from system calls. Clear, bold, legible white text header reading "SYSTEMD SERVICE SANDBOXING" and badges "SECCOMP | NAMESPACES | READ-ONLY". Dark cyber background, neon purple lighting --ar 16:9
```

### 6. Linux Auditd Event Monitoring & DFIR Logging
- **Topic**: Real-Time Execve Tracking & File Integrity Audit Rules.
- **Header Text**: `"LINUX AUDITD MONITORING"`
- **Badges**: `"REAL-TIME KERNEL EVENTS | DFIR"`
- **Prompt**:
```text
Digital Forensics & Incident Response telemetry console graphic. Holographic scanner beam inspecting a file system tree and capturing execve events in real-time. Crisp, highly legible white technical typography reading "LINUX AUDITD MONITORING" and sub-text "REAL-TIME KERNEL EVENTS | DFIR". Dark navy blue and magenta security UI backdrop --ar 16:9
```

### 7. WireGuard Mesh VPN Tunnels
- **Topic**: Encrypted Multi-Cloud VPS Interconnect & Noise Protocol.
- **Header Text**: `"WIREGUARD MESH VPN"`
- **Badges**: `"NOISE PROTOCOL | VPS ENCRYPTION"`
- **Prompt**:
```text
Global VPS network topology infographic banner. Glowing amber laser tunnels interconnecting private cloud server nodes across a dark digital globe. Bold, sharp, legible white technical title reading "WIREGUARD MESH VPN" and badge "NOISE PROTOCOL | VPS ENCRYPTION". Dark space backdrop, golden amber lighting --ar 16:9
```

### 8. eBPF / XDP High-Speed Packet Filtering
- **Topic**: Driver-Level Zero-Copy Packet Drop at Network RX Buffer.
- **Header Text**: `"eBPF / XDP PACKET FILTERING"`
- **Badges**: `"DRIVER RING BUFFER | DDOS MITIGATION"`
- **Prompt**:
```text
High-speed network architecture technical hero graphic. Fiber optic network card dropping malicious DDoS packets directly at the driver ring buffer. Clear, bold, crisp white technical title reading "eBPF / XDP PACKET FILTERING" and sub-header "DRIVER RING BUFFER | DDOS MITIGATION". Dark metallic circuit, electric teal lighting --ar 16:9
```

### 9. PAM Faillock Lockout Policy
- **Topic**: Pluggable Authentication Account Lockout & Root Protection.
- **Header Text**: `"PAM FAILLOCK POLICY"`
- **Badges**: `"ACCOUNT LOCKOUT | ROOT DEFENSE"`
- **Prompt**:
```text
Linux PAM security architecture infographic graphic. Biometric access control gate locking down automatically after repeated failed logins. Bold, crisp, highly legible white technical text header reading "PAM FAILLOCK POLICY" and badge "ACCOUNT LOCKOUT | ROOT DEFENSE". Dark obsidian background, neon cyan and red indicator UI --ar 16:9
```

### 10. Process Isolation & Unprivileged User Namespaces
- **Topic**: Namespace Resource Virtualization & Chroot Jail Sandboxing.
- **Header Text**: `"LINUX PROCESS ISOLATION"`
- **Badges**: `"USER NAMESPACES | CHROOT JAIL"`
- **Prompt**:
```text
Multi-layered sandbox container architecture blueprint. Layered isolation chamber keeping unprivileged application processes isolated from host system root directories. Bold, legible white technical typography reading "LINUX PROCESS ISOLATION" and sub-header "USER NAMESPACES | CHROOT JAIL". Dark slate environment, emerald green lighting --ar 16:9
```

---

## WORKFLOW

1. Salin prompt di atas ke Gemini Web (`gemini.google.com`).
2. Simpan file gambar hasil generasi ke `assets/img/` dengan nama berkas target (`.jpg` dan `.webp`).
3. Jalankan `python3 run_pipeline.py --deploy`.
