# ARTICLE-CONTENT-DRIVEN AI IMAGE PROMPTS & FILE MAPPING

This document defines unique, content-driven AI image generation prompts and target image filenames for all technical articles on `zyekh.com`.

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

## COMPLETE ARTICLE IMAGE FILE MAPPING & PROMPT COLLECTION

### 1. Nginx Reverse Proxy Hardening
- **Target Filenames**: `assets/img/nginx-security.jpg` & `assets/img/nginx-security.webp`
- **Article**: `blog/nginx-reverse-proxy-security-hardening-blueprint-2026.html`
- **Topic**: TLS 1.3, Rate Limiting, & Buffer Overflow Defense.
- **Prompt**:
```text
3D isometric architecture visual of a central Nginx reverse proxy server node featuring a subtle Nginx emblem, positioned between incoming internet traffic streams on the left and protected backend app servers on the right. A glowing emerald green security barrier filters incoming data, dark cyber environment, sleek technical rendering, subtle decorative UI code accents, cinematic lighting, 8k --ar 16:9
```

### 2. UFW Firewall Hardening & Rate Limiting
- **Target Filenames**: `assets/img/ufw-firewall.jpg` & `assets/img/ufw-firewall.webp`
- **Article**: `blog/ufw-firewall-hardening-and-rate-limiting-blueprint-2026.html`
- **Topic**: Default-Deny Policies & Native Port Rate Limiting.
- **Prompt**:
```text
3D isometric illustration of a glowing orange UFW network firewall gate protecting a Linux server rack cluster, blocking red unauthorized connection probes at port boundaries while allowing green data packets through, dark slate cyber setting, vibrant orange and electric blue lighting, clean technical detail --ar 16:9
```

### 3. Fail2ban Intrusion Prevention & SSH Abuse
- **Target Filenames**: `assets/img/fail2ban-defense.jpg` & `assets/img/fail2ban-defense.webp`
- **Article**: `blog/fail2ban-intrusion-prevention-and-ssh-abuse-mitigation.html`
- **Topic**: Log-based IP Banning & Recidive Jails.
- **Prompt**:
```text
3D isometric view of an automated Fail2ban security lock mechanism sealing an SSH port gate shut against glowing red brute-force login attempts, dark server infrastructure environment, glowing crimson red and gold security lock indicators, high-detail cyber defense --ar 16:9
```

### 4. Linux Kernel Sysctl Hardening
- **Target Filenames**: `assets/img/sysctl-hardening.jpg` & `assets/img/sysctl-hardening.webp`
- **Article**: `blog/linux-kernel-sysctl-hardening-network-stack-security.html`
- **Topic**: TCP/IP Stack Security, SYN Cookies, & Reverse Path Filtering.
- **Prompt**:
```text
3D isometric view of a central Linux kernel processor core with subtle Tux Linux symbol, managing blue TCP network data highways and absorbing SYN flood waves with glowing cryptographic energy barriers, dark metallic circuit grid, electric cyan and deep blue illumination --ar 16:9
```

### 5. Systemd Service Sandboxing
- **Target Filenames**: `assets/img/systemd-sandboxing.jpg` & `assets/img/systemd-sandboxing.webp`
- **Article**: `blog/systemd-service-sandboxing-and-security-hardening.html`
- **Topic**: Seccomp Syscall Filtering & Read-Only Mount Namespaces.
- **Prompt**:
```text
3D isometric illustration of a transparent violet glass isolation container encapsulating a systemd service process core, blocking unauthorized system call rays from reaching the underlying host Linux kernel, dark cyber setting, neon purple and blue lighting --ar 16:9
```

### 6. Linux Auditd Event Monitoring & DFIR Logging
- **Target Filenames**: `assets/img/auditd-monitoring.jpg` & `assets/img/auditd-monitoring.webp`
- **Article**: `blog/auditd-kernel-event-monitoring-and-dfir-logging.html`
- **Topic**: Real-Time Execve Tracking & File Integrity Audit Rules.
- **Prompt**:
```text
3D isometric view of a holographic audit scanner beam tracing a Linux file system directory tree, capturing real-time process execution events onto a dark DFIR security monitoring console, navy blue and magenta security operations backdrop, ultra-crisp render --ar 16:9
```

### 7. WireGuard Mesh VPN Tunnels
- **Target Filenames**: `assets/img/wireguard-mesh.jpg` & `assets/img/wireguard-mesh.webp`
- **Article**: `blog/wireguard-vpn-tunneling-for-secure-vps-mesh-networks.html`
- **Topic**: Encrypted Multi-Cloud VPS Interconnect & Noise Protocol.
- **Prompt**:
```text
3D isometric view of glowing golden amber laser VPN tunnels connecting private VPS server nodes across a dark digital globe map, completely isolated from public internet traffic, dark space backdrop, amber and ruby red security lighting --ar 16:9
```

### 8. eBPF / XDP High-Speed Packet Filtering
- **Target Filenames**: `assets/img/ebpf-xdp.jpg` & `assets/img/ebpf-xdp.webp`
- **Article**: `blog/ebpf-xdp-packet-filtering-and-ddos-mitigation.html`
- **Topic**: Driver-Level Zero-Copy Packet Drop at Network RX Buffer.
- **Prompt**:
```text
3D isometric illustration of a high-speed fiber optic network interface card (NIC) dropping malicious DDoS packet bursts directly at the hardware driver ring buffer, dark metallic circuit board, electric teal and cyan laser lighting --ar 16:9
```

### 9. PAM Faillock Lockout Policy
- **Target Filenames**: `assets/img/pam-faillock.jpg` & `assets/img/pam-faillock.webp`
- **Article**: `blog/pam-tally2-faillock-account-lockout-policy-guide.html`
- **Topic**: Pluggable Authentication Account Lockout & Root Protection.
- **Prompt**:
```text
3D isometric view of a futuristic Linux PAM authentication access portal locking down automatically with a red lockout indicator after failed password attempts, dark obsidian background, cyan and crimson neon indicator lights, high-detail security gate --ar 16:9
```

### 10. Process Isolation & Unprivileged User Namespaces
- **Target Filenames**: `assets/img/chroot-isolation.jpg` & `assets/img/chroot-isolation.webp`
- **Article**: `blog/chroot-jail-and-unprivileged-namespaces-isolation.html`
- **Topic**: Namespace Resource Virtualization & Chroot Jail Sandboxing.
- **Prompt**:
```text
3D isometric illustration of a multi-layered sandbox container isolating an unprivileged application process from host system root directories, virtualizing user namespaces, dark slate environment, emerald green and slate blue lighting, clean architectural render --ar 16:9
```

### 11. Linux VPS Hardening Guide 2026
- **Target Filenames**: `assets/img/vps-hardening.jpg` & `assets/img/vps-hardening.webp`
- **Article**: `blog/linux-vps-hardening-guide-2026.html`
- **Topic**: Comprehensive VPS Security Lockdown Blueprint.
- **Prompt**:
```text
3D isometric architecture visual of a heavily fortified Linux VPS server node enclosed in glowing cyber security barriers, emerald green security indicators, dark cyber environment, cinematic lighting --ar 16:9
```

### 12. Minimalist Server Architecture
- **Target Filenames**: `assets/img/static-architecture.jpg` & `assets/img/static-architecture.webp`
- **Article**: `blog/minimalist-server-architecture-pure-css-and-static-hosting.html`
- **Topic**: Static Architecture vs Monolithic Server Security.
- **Prompt**:
```text
3D isometric illustration of a sleek minimalist static server architecture vs a complex monolithic stack, ultra-clean slate blue and neon white lighting, modern server visual --ar 16:9
```

### 13. Content Security Policy (CSP) & Headers
- **Target Filenames**: `assets/img/csp-security.jpg` & `assets/img/csp-security.webp`
- **Article**: `blog/securing-web-applications-with-strict-content-security-policy.html`
- **Topic**: Strict Content Security Policy & Security Headers.
- **Prompt**:
```text
3D isometric view of a web application browser window protected by a glowing laser security grid blocking untrusted inline script injection, dark cyber backdrop, electric blue lighting --ar 16:9
```

### 14. Understanding Linux eBPF Security Monitoring
- **Target Filenames**: `assets/img/ebpf-monitoring.jpg` & `assets/img/ebpf-monitoring.webp`
- **Article**: `blog/understanding-linux-ebpf-security-monitoring.html`
- **Topic**: eBPF Kernel Hooks & Real-Time Security Monitoring.
- **Prompt**:
```text
3D isometric visual of eBPF bytecode probes attached to Linux kernel system call hooks, capturing security events in real-time, dark magenta and cyan cyber environment --ar 16:9
```

### 15. Zero-Trust SSH Access with FIDO2 & SSH CA
- **Target Filenames**: `assets/img/ssh-zero-trust.jpg` & `assets/img/ssh-zero-trust.webp`
- **Article**: `blog/zero-trust-ssh-access-with-fido2-and-ssh-ca.html`
- **Topic**: FIDO2 Hardware Key Authentication & Short-Lived SSH Certificates.
- **Prompt**:
```text
3D isometric view of a YubiKey FIDO2 hardware token authenticating short-lived SSH certificates at a secure server gateway, dark obsidian and gold security lighting --ar 16:9
```

---

## WORKFLOW

1. Salin prompt di atas ke Gemini Web (`gemini.google.com`).
2. Simpan file gambar hasil generasi ke `assets/img/` dengan nama berkas target (`.jpg` dan `.webp`).
3. Jalankan `python3 run_pipeline.py --deploy`.
