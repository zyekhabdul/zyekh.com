# ARTICLE-CONTENT-DRIVEN AI IMAGE PROMPTS (NO-TEXT POLICY)

This document defines unique, content-driven AI image generation prompts derived directly from the technical mechanisms explained inside each article on `zyekh.com`.

---

## CORE STRATEGY & NO-TEXT RULES

1. **Content-Driven Visual Metaphors**: Prompts are derived directly from the core technical mechanism of each article (e.g. eBPF kernel hooks, WireGuard laser tunnels, PAM access gates), avoiding repetitive template layouts.
2. **Strict No-Text Policy**: Every prompt explicitly instructs the AI generator to exclude all text, labels, letters, and typography (`no text, no words, no letters, no logos`). Teks judul dan badge akan disajikan 100% oleh HTML/CSS yang tajam dan responsive.
3. **Aspect Ratio**: `16:9` (`--ar 16:9`).

---

## PROMPT COLLECTION DERIVED FROM ARTICLE CONTENT

### 1. Nginx Reverse Proxy Hardening
- **Topic**: TLS 1.3, Rate Limiting, & Buffer Overflow Defense.
- **Visual Metaphor**: A high-tech glowing green digital shield gateway filtering incoming HTTP traffic streams, letting clean packets pass while reflecting malicious payload waves.
- **Prompt**:
```text
3D isometric view of a high-performance Nginx reverse proxy gateway node with glowing emerald green energy shields filtering a high-speed data stream, dark cybernetic background, cinematic volumetric lighting, deep shadows, ultra-detailed 8k render, no text, no words, no letters, no logos --ar 16:9
```

### 2. UFW Firewall Hardening & Rate Limiting
- **Topic**: Default-Deny Policies & Native Port Rate Limiting.
- **Visual Metaphor**: A futuristic neon-orange fortress wall dropping unrequested connection probes and enforcing IP connection limits at the network edge.
- **Prompt**:
```text
3D isometric illustration of a massive glowing orange digital firewall fortress wall protecting a server cluster, dropping red unauthorized connection probes at the border, dark slate environment, vibrant orange and electric blue lighting, ultra clean render, no text, no words, no letters, no logos --ar 16:9
```

### 3. Fail2ban Intrusion Prevention & SSH Abuse
- **Topic**: Log-based IP Banning & Recidive Jails.
- **Visual Metaphor**: An automated cyber sentinel mechanism locking an electric red security vault door when brute-force SSH password attempts occur.
- **Prompt**:
```text
3D isometric view of an automated security lock vault sealing shut against glowing red botnet entry probes, dark server infrastructure background, glowing crimson red and gold security barriers, high-detail cyber defense art, no text, no words, no letters, no logos --ar 16:9
```

### 4. Linux Kernel Sysctl Hardening
- **Topic**: TCP/IP Stack Security, SYN Cookies, & Reverse Path Filtering.
- **Visual Metaphor**: A central Linux kernel processor core routing TCP data highways while absorbing SYN flood waves with cryptographic cookies.
- **Prompt**:
```text
3D isometric view of a Linux kernel micro-processor engine managing blue TCP data highways, absorbing SYN flood waves with glowing cryptographic energy cookies, dark metallic circuit grid, electric cyan and deep blue illumination, no text, no words, no letters, no logos --ar 16:9
```

### 5. Systemd Service Sandboxing
- **Topic**: Seccomp Syscall Filtering & Read-Only Mount Namespaces.
- **Visual Metaphor**: A transparent indigo glass containment cube isolating a service process from raw system call pathways.
- **Prompt**:
```text
3D isometric illustration of a transparent violet glass isolation cube encapsulating a glowing micro-service process core, blocking dangerous system call rays from reaching the host motherboard, dark cyber setting, neon purple and blue lighting, no text, no words, no letters, no logos --ar 16:9
```

### 6. Linux Auditd Event Monitoring & DFIR Logging
- **Topic**: Real-Time Execve Tracking & File Integrity Audit Rules.
- **Visual Metaphor**: A holographic digital scanner tracing binary execution paths and file access operations in real-time.
- **Prompt**:
```text
3D isometric view of a holographic audit scanner beam inspecting a glowing file system hierarchy, capturing process execution events in real-time, dark navy blue and magenta security operations backdrop, ultra-crisp render, no text, no words, no letters, no logos --ar 16:9
```

### 7. WireGuard Mesh VPN Tunnels
- **Topic**: Encrypted Multi-Cloud VPS Interconnect & Noise Protocol.
- **Visual Metaphor**: Laser-encrypted private mesh tunnels linking multi-region cloud server nodes across a dark digital globe.
- **Prompt**:
```text
3D isometric view of glowing amber laser beam tunnels connecting private cloud server nodes across a dark digital globe, invisible from public network space, dark space environment, golden amber and ruby red lighting, no text, no words, no letters, no logos --ar 16:9
```

### 8. eBPF / XDP High-Speed Packet Filtering
- **Topic**: Driver-Level Zero-Copy Packet Drop at Network RX Buffer.
- **Visual Metaphor**: A high-speed network driver card dropping DDoS packets directly at the hardware ingestion ring buffer before memory allocation.
- **Prompt**:
```text
3D isometric illustration of a high-speed fiber optic network interface card dropping malicious traffic packets directly at the driver ring buffer level, dark metallic cyber circuit, electric teal and cyan laser lighting, no text, no words, no letters, no logos --ar 16:9
```

### 9. PAM Faillock Lockout Policy
- **Topic**: Pluggable Authentication Account Lockout & Root Protection.
- **Visual Metaphor**: A high-tech biometric access gate closing automatically after repeated failed password attempts.
- **Prompt**:
```text
3D isometric view of a futuristic biometric access control portal locking down automatically after unauthorized entry attempts, dark obsidian background, warm red and cyan neon indicator lights, high-detail security gate, no text, no words, no letters, no logos --ar 16:9
```

### 10. Process Isolation & Unprivileged User Namespaces
- **Topic**: Namespace Resource Virtualization & Chroot Jail Sandboxing.
- **Visual Metaphor**: A layered sandbox environment virtualizing UID/GID mappings and keeping unprivileged processes contained without root privileges.
- **Prompt**:
```text
3D isometric illustration of a multi-layered sandbox chamber isolating an unprivileged application process from host system directories, dark slate environment, emerald green and slate blue lighting, clean architectural 3D render, no text, no words, no letters, no logos --ar 16:9
```

---

## WORKFLOW

1. Salin prompt di atas ke Gemini Web (`gemini.google.com`).
2. Simpan file gambar hasil generasi ke `assets/img/` dengan nama berkas target (`.jpg` dan `.webp`).
3. Jalankan `python3 run_pipeline.py --deploy`.
