# ARTICLE-CONTENT-DRIVEN AI IMAGE PROMPTS (ARTICLE-REPRESENTATIVE STRATEGY)

This document defines rich, article-representative AI image generation prompts for all 25 technical security articles on `zyekh.com`.

---

## OPERATIONAL & DESIGN PROTOCOLS

1. **TECHNICAL REPRESENTATION**: Each prompt clearly visualizes the core technical mechanism of the article (e.g. eBPF socket bypass, WASI linear memory bounds, Vault CA certificate issuance).
2. **HIGH VISUAL QUALITY**: Uses 3D isometric cyber architecture rendering, rich HSL lighting, and clean developer aesthetics.
3. **1 PROMPT = 1 NEW CHAT SESSION**: Always open a fresh chat session in Gemini Web for each thumbnail prompt.

---

## BATCH 2 (2026 TRENDS) PROMPT COLLECTION

### 1. Rust in the Linux Kernel Security
- **Target Filenames**: `assets/img/rust-kernel-security.jpg` & `assets/img/rust-kernel-security.webp`
- **Prompt**: `3D isometric cyber architecture illustration representing Rust in Linux kernel security, showing a glowing rust-gold memory lock and safe abstraction layer isolating a microprocessor core from memory overflow spikes, dark cyber background, electric cyan and copper lighting, clean developer aesthetic, 8k render --ar 16:9`

### 2. Cilium eBPF & Tetragon Cloud-Native Security
- **Target Filenames**: `assets/img/cilium-ebpf-security.jpg` & `assets/img/cilium-ebpf-security.webp`
- **Prompt**: `3D isometric network security diagram showing Cilium eBPF packet routing bypassing traditional firewalls directly into Linux kernel sockets, with Tetragon security sensors monitoring pod processes in real-time, neon teal and electric blue lighting, dark background, 8k render --ar 16:9`

### 3. Linux Landlock LSM Unprivileged Sandboxing
- **Target Filenames**: `assets/img/landlock-sandboxing.jpg` & `assets/img/landlock-sandboxing.webp`
- **Prompt**: `3D isometric illustration of Linux Landlock LSM unprivileged sandbox, featuring an isolated application node enclosed within a transparent security glass barrier restricting filesystem directory access, emerald green and slate blue accent lighting, dark background, 8k render --ar 16:9`

### 4. Zero-Trust Microservices with Wasm Sandboxing
- **Target Filenames**: `assets/img/wasm-sandboxing.jpg` & `assets/img/wasm-sandboxing.webp`
- **Prompt**: `3D isometric visualization of WebAssembly Wasm linear memory sandbox runtime, showing microservice execution isolated inside a high-tech crystal module with WASI capability gateways, neon purple and ultra-violet lighting, dark background, 8k render --ar 16:9`

### 5. HTTP/3 & QUIC Protocol Security Hardening
- **Target Filenames**: `assets/img/http3-quic-security.jpg` & `assets/img/http3-quic-security.webp`
- **Prompt**: `3D isometric illustration of HTTP/3 QUIC protocol UDP packet pipeline, showing 0-RTT replay defense barrier blocking duplicated request vectors while allowing encrypted TLS 1.3 streams, electric blue and magenta lighting, dark infrastructure background, 8k render --ar 16:9`

### 6. Linux Seccomp-BPF Syscall Filtering
- **Target Filenames**: `assets/img/seccomp-hardening.jpg` & `assets/img/seccomp-hardening.webp`
- **Prompt**: `3D isometric diagram of Linux Seccomp-BPF system call filtering, showing a kernel gate inspecting and dropping unauthorized syscall numbers before execution, glowing crimson red and gold security locks, dark metallic background, 8k render --ar 16:9`

### 7. Kubernetes Pod Security Standards (PSS)
- **Target Filenames**: `assets/img/k8s-pod-security.jpg` & `assets/img/k8s-pod-security.webp`
- **Prompt**: `3D isometric illustration of Kubernetes Pod Security Standards admission control gate, restricting non-root pod deployments and dropping privileges at the namespace boundary, electric cyan and navy blue lighting, dark cyber background, 8k render --ar 16:9`

### 8. Linux Audit Logging with Vector & ClickHouse
- **Target Filenames**: `assets/img/audit-vector-clickhouse.jpg` & `assets/img/audit-vector-clickhouse.webp`
- **Prompt**: `3D isometric visualization of Vector Rust log forwarder streaming high-speed audit telemetry streams into a ClickHouse columnar analytical database matrix, vibrant gold and deep blue lighting, dark DFIR SOC background, 8k render --ar 16:9`

### 9. Short-Lived SSH Certificate Auth with Vault CA
- **Target Filenames**: `assets/img/ssh-vault-ca.jpg` & `assets/img/ssh-vault-ca.webp`
- **Prompt**: `3D isometric illustration of HashiCorp Vault Certificate Authority issuing short-lived 8-hour SSH user certificates for secure server gateway access, obsidian dark background, glowing amber and cyan security keys, 8k render --ar 16:9`

### 10. Container Image Signing & SLSA with Cosign
- **Target Filenames**: `assets/img/cosign-image-signing.jpg` & `assets/img/cosign-image-signing.webp`
- **Prompt**: `3D isometric illustration of Sigstore Cosign keyless container image signing, linking an OCI container image digest to an immutable Rekor transparency log ledger, mint teal and amber laser lighting, dark cyber background, 8k render --ar 16:9`
