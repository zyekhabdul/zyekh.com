# ARTICLE-CONTENT-DRIVEN AI IMAGE PROMPTS (RECOGNIZABLE TECHNICAL VISUAL METAPHOR STRATEGY)

This document defines unique, content-driven AI image generation prompts for technical article thumbnails and hero graphics on `zyekh.com`.

---

## OPERATIONAL PROTOCOL (MANDATORY FOR GEMINI WEB)

- **CRITICAL OPERATIONAL RULE**: **1 PROMPT = 1 NEW CHAT SESSION (NEW CHAT)**.
- Never generate multiple article thumbnails within the *same* Gemini Web chat thread. In-session context causes Gemini to inherit layout biases and duplicate object angles across images.
- Always open a **Fresh New Chat** (`New Chat`) in Gemini Web for each article prompt to guarantee 100% unique composition.

---

## CORE STRATEGY: RECOGNIZABLE VISUAL ARCHITECTURE (NO CLUTTERED TEXT)

1. **Immediate Technical Recognition**: The image must clearly depict the specific technical mechanism (e.g. Nginx server proxying traffic to backend app servers, UFW firewall gate blocking IP probes, WireGuard mesh laser tunnels). A developer looking at the thumbnail must immediately understand the subject matter without guessing.
2. **Minimal / Decorative Text Only**: Reject heavy title banners, text headers, or cluttered labels that distract the viewer. Text/symbols (if any) are minimal decorative accessories only (e.g. a subtle Nginx emblem, minor UI code accent, or small port number). Article titles and badges are rendered sharply by HTML/CSS on the web page.
3. **High-Contrast Developer Aesthetic**: Sleek 3D isometric architecture renders, dark theme backdrop, vibrant accent lighting (emerald green for Nginx/security, orange for UFW, amber for WireGuard, etc.), and clean composition.
4. **Aspect Ratio**: `16:9` (`--ar 16:9`).

---

## PROMPT COLLECTION DERIVED FROM ARTICLE CONTENT

### 1. Nginx Reverse Proxy Hardening
- **Topic**: TLS 1.3, Rate Limiting, & Buffer Overflow Defense.
- **Visual Concept**: Central Nginx proxy server chassis with a subtle Nginx emblem, receiving incoming internet traffic on the left and routing clean packets to protected backend app servers on the right through an emerald green security filter.
- **Prompt**:
```text
3D isometric architecture visual of a central Nginx reverse proxy server node featuring a subtle Nginx emblem, positioned between incoming internet traffic streams on the left and protected backend app servers on the right. A glowing emerald green security barrier filters incoming data, dark cyber environment, sleek technical rendering, subtle decorative UI code accents, cinematic lighting, 8k --ar 16:9
```

### 2. UFW Firewall Hardening & Rate Limiting
- **Topic**: Default-Deny Policies & Native Port Rate Limiting.
- **Visual Concept**: Glowing orange digital UFW firewall gate at the perimeter of a Linux server rack, dropping red unauthorized connection probes while letting green packets pass into port 22/443.
- **Prompt**:
```text
3D isometric illustration of a glowing orange UFW network firewall gate protecting a Linux server rack cluster, blocking red unauthorized connection probes at port boundaries while allowing green data packets through, dark slate cyber setting, vibrant orange and electric blue lighting, clean technical detail --ar 16:9
```

### 3. Fail2ban Intrusion Prevention & SSH Abuse
- **Topic**: Log-based IP Banning & Recidive Jails.
- **Visual Concept**: Automated security vault lock mechanism dynamically sealing an SSH access port after detecting red brute-force password attempts.
- **Prompt**:
```text
3D isometric view of an automated Fail2ban security lock mechanism sealing an SSH port gate shut against glowing red brute-force login attempts, dark server infrastructure environment, glowing crimson red and gold security lock indicators, high-detail cyber defense --ar 16:9
```

### 4. Linux Kernel Sysctl Hardening
- **Topic**: TCP/IP Stack Security, SYN Cookies, & Reverse Path Filtering.
- **Visual Concept**: Central Linux kernel CPU core receiving TCP data highways and absorbing SYN flood traffic waves with cryptographic cookie energy barriers.
- **Prompt**:
```text
3D isometric view of a central Linux kernel processor core with subtle Tux Linux symbol, managing blue TCP network data highways and absorbing SYN flood waves with glowing cryptographic energy barriers, dark metallic circuit grid, electric cyan and deep blue illumination --ar 16:9
```

### 5. Systemd Service Sandboxing
- **Topic**: Seccomp Syscall Filtering & Read-Only Mount Namespaces.
- **Visual Concept**: Transparent violet glass isolation container encapsulating a systemd service process, blocking unauthorized system call rays from reaching the host Linux kernel below.
- **Prompt**:
```text
3D isometric illustration of a transparent violet glass isolation container encapsulating a systemd service process core, blocking unauthorized system call rays from reaching the underlying host Linux kernel, dark cyber setting, neon purple and blue lighting --ar 16:9
```

### 6. Linux Auditd Event Monitoring & DFIR Logging
- **Topic**: Real-Time Execve Tracking & File Integrity Audit Rules.
- **Visual Concept**: Holographic security scanner beam inspecting a Linux file system folder tree, logging process execution events in real-time onto a dark DFIR security telemetry screen.
- **Prompt**:
```text
3D isometric view of a holographic audit scanner beam tracing a Linux file system directory tree, capturing real-time process execution events onto a dark DFIR security monitoring console, navy blue and magenta security operations backdrop, ultra-crisp render --ar 16:9
```

### 7. WireGuard Mesh VPN Tunnels
- **Topic**: Encrypted Multi-Cloud VPS Interconnect & Noise Protocol.
- **Visual Concept**: Glowing amber laser VPN tunnels connecting private cloud server nodes across a dark digital globe map, bypassing public internet routes.
- **Prompt**:
```text
3D isometric view of glowing golden amber laser VPN tunnels connecting private VPS server nodes across a dark digital globe map, completely isolated from public internet traffic, dark space backdrop, amber and ruby red security lighting --ar 16:9
```

### 8. eBPF / XDP High-Speed Packet Filtering
- **Topic**: Driver-Level Zero-Copy Packet Drop at Network RX Buffer.
- **Visual Concept**: High-speed network interface card (NIC) dropping DDoS packets directly at the hardware driver ring buffer layer before CPU memory allocation.
- **Prompt**:
```text
3D isometric illustration of a high-speed fiber optic network interface card (NIC) dropping malicious DDoS packet bursts directly at the hardware driver ring buffer, dark metallic circuit board, electric teal and cyan laser lighting --ar 16:9
```

### 9. PAM Faillock Lockout Policy
- **Topic**: Pluggable Authentication Account Lockout & Root Protection.
- **Visual Concept**: Futuristic Linux PAM authentication portal locking down automatically with a red status indicator after 3 consecutive failed password attempts.
- **Prompt**:
```text
3D isometric view of a futuristic Linux PAM authentication access portal locking down automatically with a red lockout indicator after failed password attempts, dark obsidian background, cyan and crimson neon indicator lights, high-detail security gate --ar 16:9
```

### 10. Process Isolation & Unprivileged User Namespaces
- **Topic**: Namespace Resource Virtualization & Chroot Jail Sandboxing.
- **Visual Concept**: Multi-layered container sandbox virtualizing UID/GID user mappings and isolating unprivileged processes from host system root directories.
- **Prompt**:
```text
3D isometric illustration of a multi-layered sandbox container isolating an unprivileged application process from host system root directories, virtualizing user namespaces, dark slate environment, emerald green and slate blue lighting, clean architectural render --ar 16:9
```

---

## WORKFLOW

1. Salin prompt di atas ke Gemini Web (`gemini.google.com`).
2. Simpan file gambar hasil generasi ke `assets/img/` dengan nama berkas target (`.jpg` dan `.webp`).
3. Jalankan `python3 run_pipeline.py --deploy`.
