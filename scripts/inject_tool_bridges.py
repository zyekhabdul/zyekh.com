#!/usr/bin/env python3
import glob
import re
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent

TOOL_MAPPINGS = {
    'ebpf-xdp-packet-filtering-and-ddos-mitigation': {
        'badge': '[ INTERACTIVE LAB // NETWORKING ]',
        'title': 'eBPF Packet Filter & Syscall Evaluator',
        'desc': 'Simulate XDP driver-level packet drops, evaluate BPF verdict maps, and benchmark kernel packet filtering in real time.',
        'url': '/tools/ebpf-evaluator.html',
        'btn': 'Launch eBPF Evaluator ->'
    },
    'understanding-linux-ebpf-security-monitoring': {
        'badge': '[ INTERACTIVE LAB // DFIR ]',
        'title': 'eBPF Packet Filter & Syscall Evaluator',
        'desc': 'Explore kernel probe tracepoints, ring buffer telemetry streams, and security event filtering in the browser.',
        'url': '/tools/ebpf-evaluator.html',
        'btn': 'Launch eBPF Evaluator ->'
    },
    'cilium-ebpf-cloud-native-network-security-and-cilium-tetragon': {
        'badge': '[ INTERACTIVE LAB // KUBERNETES ]',
        'title': 'eBPF Packet Filter & Syscall Evaluator',
        'desc': 'Model Cilium Tetragon runtime syscall filtering, network policy enforcement, and eBPF socket routing.',
        'url': '/tools/ebpf-evaluator.html',
        'btn': 'Launch eBPF Evaluator ->'
    },
    'vllm-pagedattention-high-throughput-inference-tuning': {
        'badge': '[ INTERACTIVE CALCULATOR // AI INFRA ]',
        'title': 'LLM VRAM & Speculative Decoding Calculator',
        'desc': 'Calculate KV-cache page table allocations, multi-GPU tensor sharding, and tokens-per-second throughput.',
        'url': '/tools/llm-calculator.html',
        'btn': 'Calculate VRAM & Tokens ->'
    },
    'kv-cache-int4-quantization-long-context': {
        'badge': '[ INTERACTIVE CALCULATOR // AI INFRA ]',
        'title': 'LLM VRAM & Memory Footprint Calculator',
        'desc': 'Estimate exact memory savings across FP16, INT8, and INT4 KV-cache quantization across 32k to 128k contexts.',
        'url': '/tools/llm-calculator.html',
        'btn': 'Calculate KV Cache VRAM ->'
    },
    'dspy-declarative-prompting-optimization': {
        'badge': '[ INTERACTIVE TOOL // PROMPT OPS ]',
        'title': 'AI Token Counter & Context Window Analyzer',
        'desc': 'Measure token density, optimize prompt payloads, and calculate per-inference API cost across LLM models.',
        'url': '/tools/ai-token.html',
        'btn': 'Analyze Token Density ->'
    },
    'slora-adapter-multiplexing-single-gpu': {
        'badge': '[ INTERACTIVE SIMULATOR // GPU OPS ]',
        'title': 'LLM Speculative Decoding & VRAM Simulator',
        'desc': 'Model multi-tenant LoRA adapter VRAM allocations and determine single-GPU concurrency saturation.',
        'url': '/tools/speculative-decoding.html',
        'btn': 'Simulate Adapter VRAM ->'
    },
    'moe-serving-mixture-of-experts-routing': {
        'badge': '[ INTERACTIVE CALCULATOR // AI INFRA ]',
        'title': 'LLM VRAM & MoE Router Calculator',
        'desc': 'Calculate active expert memory bounds, routing matrix compute overhead, and multi-GPU tensor sharding.',
        'url': '/tools/llm-calculator.html',
        'btn': 'Calculate MoE Memory ->'
    },
    'structured-output-generation-logits-constraints': {
        'badge': '[ INTERACTIVE TOOL // PARSER ]',
        'title': 'JSON Schema & Regex Validator',
        'desc': 'Test JSON Schema grammars, regex constraint patterns, and validate structured JSON token outputs.',
        'url': '/tools/json.html',
        'btn': 'Validate JSON Schema ->'
    },
    'webgpu-llm-inference-browser-sandbox': {
        'badge': '[ INTERACTIVE BENCHMARK // WEBGPU ]',
        'title': 'WebGPU Shader & Inference Latency Profiler',
        'desc': 'Measure local GPU WGSL shader compilation speed, GEMM matrix GFLOPS throughput, and VRAM memory transfer bandwidth.',
        'url': '/tools/webgpu-profiler.html',
        'btn': 'Launch WebGPU Profiler ->'
    },
    'colbert-late-interaction-advanced-rag': {
        'badge': '[ INTERACTIVE TOOL // VECTOR OPS ]',
        'title': 'AI Token & Context Window Estimator',
        'desc': 'Estimate token chunking boundaries, embedding vector index memory sizes, and query expansion token budgets.',
        'url': '/tools/ai-token.html',
        'btn': 'Estimate Token Chunks ->'
    },
    'omnirouter-llm-gateway-routing-fallback-patterns': {
        'badge': '[ INTERACTIVE CALCULATOR // AI GATEWAY ]',
        'title': 'LLM Pricing & Cost Fallback Calculator',
        'desc': 'Model tier fallback routing economics, token throughput latency SLAs, and multi-provider failover budgets.',
        'url': '/tools/llm-calculator.html',
        'btn': 'Calculate Gateway Costs ->'
    },
    'multi-agent-swarm-orchestration-patterns': {
        'badge': '[ INTERACTIVE TOOL // AGENT OPS ]',
        'title': 'AI Token & Multi-Agent Payload Analyzer',
        'desc': 'Audit multi-agent communication token overhead, message exchange payloads, and agent memory context limits.',
        'url': '/tools/ai-token.html',
        'btn': 'Analyze Agent Tokens ->'
    },
    'wireguard-vpn-tunneling-for-secure-vps-mesh-networks': {
        'badge': '[ INTERACTIVE GENERATOR // VPN ]',
        'title': 'WireGuard Mesh & Keypair Configuration Generator',
        'desc': 'Generate production wg0.conf gateway files, client peer profiles, and Curve25519 (X25519) cryptographic keypairs 100% offline.',
        'url': '/tools/wireguard-generator.html',
        'btn': 'Launch WireGuard Generator ->'
    },
    'linux-kernel-sysctl-hardening-network-stack-security': {
        'badge': '[ INTERACTIVE GENERATOR // SECURITY ]',
        'title': 'Linux sysctl & SSH Hardening Config Generator',
        'desc': 'Build production-ready 99-hardening.conf kernel parameters and OpenSSH daemon configs tailored to your workloads.',
        'url': '/tools/linux-hardening-generator.html',
        'btn': 'Build sysctl & SSH Configs ->'
    },
    'ufw-firewall-hardening-and-rate-limiting-blueprint-2026': {
        'badge': '[ INTERACTIVE CALCULATOR // SECURITY ]',
        'title': 'CIDR Subnet & IP Range Calculator',
        'desc': 'Generate precise CIDR subnet ranges for UFW firewall allow/deny rules and rate-limiting blocks.',
        'url': '/tools/subnet.html',
        'btn': 'Calculate Firewall CIDR ->'
    },
    'fail2ban-intrusion-prevention-and-ssh-abuse-mitigation': {
        'badge': '[ INTERACTIVE CALCULATOR // SECURITY ]',
        'title': 'CIDR Subnet & IP Mask Calculator',
        'desc': 'Calculate ignoreip CIDR ranges and subnet boundaries for fail2ban intrusion prevention filters.',
        'url': '/tools/subnet.html',
        'btn': 'Calculate IgnoreIP Subnets ->'
    },
    'linux-vps-hardening-guide-2026': {
        'badge': '[ INTERACTIVE GENERATOR // SYSADMIN ]',
        'title': 'Linux sysctl & SSH Hardening Config Generator',
        'desc': 'Generate hardened 99-hardening.conf and sshd_config.d drop-in configuration files for your VPS offline.',
        'url': '/tools/linux-hardening-generator.html',
        'btn': 'Generate Hardening Configs ->'
    },
    'chroot-jail-and-unprivileged-namespaces-isolation': {
        'badge': '[ INTERACTIVE UTILITY // SANDBOXING ]',
        'title': 'Linux chmod & File Permissions Calculator',
        'desc': 'Verify chroot root directory ownership (root:root 755) and unprivileged sandbox permissions.',
        'url': '/tools/chmod-calculator.html',
        'btn': 'Calculate Sandbox Permissions ->'
    },
    'systemd-service-sandboxing-and-security-hardening': {
        'badge': '[ INTERACTIVE GENERATOR // SYSTEMD ]',
        'title': 'Systemd Service Sandboxing & Security Override Generator',
        'desc': 'Build production-ready drop-in override.conf directives and calculate systemd-analyze security exposure ratings 100% offline.',
        'url': '/tools/systemd-generator.html',
        'btn': 'Generate Systemd Sandboxing ->'
    },
    'pam-tally2-faillock-account-lockout-policy-guide': {
        'badge': '[ INTERACTIVE GENERATOR // PAM & AUTH ]',
        'title': 'Linux PAM & Faillock Policy Generator',
        'desc': 'Build production-ready faillock.conf account lockout policies and PAM authentication stacks 100% offline.',
        'url': '/tools/pam-generator.html',
        'btn': 'Generate PAM & Faillock Policy ->'
    },
    'linux-audit-logging-with-vector-and-clickhouse-dfir': {
        'badge': '[ INTERACTIVE GENERATOR // AUDITD & SIEM ]',
        'title': 'Linux Auditd & DFIR Event Rule Generator',
        'desc': 'Generate production Linux audit.rules, auditd.conf configs, and Vector log shipper ingestion pipelines 100% offline.',
        'url': '/tools/auditd-generator.html',
        'btn': 'Generate Auditd & Vector Config ->'
    },
    'auditd-kernel-event-monitoring-and-dfir-logging': {
        'badge': '[ INTERACTIVE GENERATOR // KERNEL AUDIT ]',
        'title': 'Linux Auditd & DFIR Event Rule Generator',
        'desc': 'Build CIS Benchmark L2 audit.rules, immutable kernel configs (-e 2), and ausearch forensic query commands 100% offline.',
        'url': '/tools/auditd-generator.html',
        'btn': 'Generate Kernel Audit Rules ->'
    },
    'linux-seccomp-bpf-syscall-filtering-hardening-guide': {
        'badge': '[ INTERACTIVE GENERATOR // SECCOMP ]',
        'title': 'Container Security & OCI Seccomp Profile Generator',
        'desc': 'Build zero-trust OCI Seccomp JSON filter profiles and Kubernetes SecurityContext manifests with workload whitelisting 100% offline.',
        'url': '/tools/seccomp-generator.html',
        'btn': 'Build Seccomp Profile ->'
    },
    'linux-landlock-lsm-unprivileged-sandboxing-blueprint': {
        'badge': '[ INTERACTIVE UTILITY // SYSADMIN ]',
        'title': 'Linux chmod & File Permissions Calculator',
        'desc': 'Model Landlock filesystem access rights (LANDLOCK_ACCESS_FS_READ) and calculate granular directory permissions.',
        'url': '/tools/chmod-calculator.html',
        'btn': 'Calculate Landlock Permissions ->'
    },
    'rust-in-linux-kernel-security-and-memory-safety-blueprint-2026': {
        'badge': '[ INTERACTIVE LAB // SYSTEMS ]',
        'title': 'eBPF & Kernel Memory Safety Evaluator',
        'desc': 'Inspect kernel boundary abstractions, memory safety guarantees, and safe pointer lifecycle patterns.',
        'url': '/tools/ebpf-evaluator.html',
        'btn': 'Launch Kernel Evaluator ->'
    },
    'securing-web-applications-with-strict-content-security-policy': {
        'badge': '[ INTERACTIVE UTILITY // APPSEC ]',
        'title': 'Cryptographic Hash & CSP Digest Generator',
        'desc': 'Generate SHA-256 / SHA-384 script integrity hashes for strict CSP script-src digest allowlisting.',
        'url': '/tools/hash.html',
        'btn': 'Generate CSP Hashes ->'
    },
    'nginx-reverse-proxy-security-hardening-blueprint-2026': {
        'badge': '[ INTERACTIVE TOOL // WEB SEC ]',
        'title': 'cURL Command Builder & Security Header Tester',
        'desc': 'Generate hardened cURL commands to verify TLS 1.3 handshakes, HSTS, CSP, and reverse proxy upstream headers.',
        'url': '/tools/curl.html',
        'btn': 'Build cURL Header Check ->'
    },
    'http3-quic-security-hardening-and-0rtt-mitigation-blueprint': {
        'badge': '[ INTERACTIVE TOOL // WEB SEC ]',
        'title': 'cURL Command Builder & HTTP/3 Tester',
        'desc': 'Construct cURL --http3 diagnostic commands to verify QUIC transport handshakes and 0-RTT replay defenses.',
        'url': '/tools/curl.html',
        'btn': 'Build HTTP/3 cURL Test ->'
    },
    'zero-trust-ssh-access-with-fido2-and-ssh-ca': {
        'badge': '[ INTERACTIVE TOOL // CRYPTO ]',
        'title': 'Cryptographic Hash & Key Fingerprint Generator',
        'desc': 'Compute SHA-256 public key fingerprints and verify cryptographic checksums for SSH CA certificates.',
        'url': '/tools/hash.html',
        'btn': 'Generate Key Fingerprints ->'
    },
    'ssh-certificates-vault-ca-short-lived-authentication': {
        'badge': '[ INTERACTIVE TOOL // CRYPTO ]',
        'title': 'JWT Token & Cryptographic Signature Inspector',
        'desc': 'Inspect short-lived authentication token claims, verify expiration timestamps, and decode certificate payloads.',
        'url': '/tools/jwt.html',
        'btn': 'Inspect Auth Tokens ->'
    },
    'container-image-signing-and-slsa-provenance-with-cosign': {
        'badge': '[ INTERACTIVE TOOL // CRYPTO ]',
        'title': 'Cryptographic Hash & SLSA Digest Generator',
        'desc': 'Calculate SHA-256 container image digests, generate HMAC signatures, and verify SLSA supply chain provenance.',
        'url': '/tools/hash.html',
        'btn': 'Generate Image Digests ->'
    },
    'kubernetes-pod-security-standards-pss-and-admission-control': {
        'badge': '[ INTERACTIVE GENERATOR // SECCOMP & K8S ]',
        'title': 'Container Security & OCI Seccomp Profile Generator',
        'desc': 'Build Kubernetes Pod securityContext.seccompProfile manifests and OCI syscall filter whitelists 100% offline.',
        'url': '/tools/seccomp-generator.html',
        'btn': 'Build K8s SecurityContext ->'
    },
    'zero-trust-microservices-with-wasm-runtime-sandboxing': {
        'badge': '[ INTERACTIVE UTILITY // CRYPTO ]',
        'title': 'Cryptographic Hash & Wasm Module Digest Generator',
        'desc': 'Generate cryptographic SHA-256 digests for untrusted WebAssembly module verification before runtime compilation.',
        'url': '/tools/hash.html',
        'btn': 'Generate Wasm Digest ->'
    },
    'minimalist-server-architecture-pure-css-and-static-hosting': {
        'badge': '[ INTERACTIVE UTILITY // FRONTEND ]',
        'title': 'CSS Minifier & Bundle Optimizer',
        'desc': 'Minify CSS stylesheets, eliminate unused whitespace, and achieve sub-10ms render performance on static architectures.',
        'url': '/tools/css-minifier.html',
        'btn': 'Minify CSS Online ->'
    }
}

def inject_bridges():
    blog_dir = BASE_DIR / "blog"
    updated_count = 0

    for filepath in sorted(blog_dir.glob("*.html")):
        if filepath.name == "index.html":
            continue
        slug = filepath.stem
        if slug not in TOOL_MAPPINGS:
            continue

        m = TOOL_MAPPINGS[slug]
        html_content = filepath.read_text(encoding="utf-8")

        new_card_html = f'''    <!-- Contextual Interactive Tool Bridge -->
    <div class="article-cross-links tool-bridge-card">
      <div class="tool-bridge-info">
        <span class="tool-bridge-badge">{m['badge']}</span>
        <h4 class="tool-bridge-title">{m['title']}</h4>
        <p class="tool-bridge-desc">{m['desc']}</p>
      </div>
      <a class="tool-bridge-btn" href="{m['url']}">{m['btn']}</a>
    </div>'''

        # Match existing cross-links block cleanly
        pattern = r'(<!-- (?:Related Tools Recommendation|Contextual Interactive Tool Bridge) -->\s*)?<div class="article-cross-links[^"]*">.*?</div>'
        
        match = re.search(pattern, html_content, flags=re.DOTALL)
        if match:
            html_content = html_content[:match.start()] + new_card_html + html_content[match.end():]
            filepath.write_text(html_content, encoding="utf-8")
            updated_count += 1
        else:
            # Fallback: insert before </main>
            if "</main>" in html_content:
                html_content = html_content.replace("</main>", f"{new_card_html}\n  </main>")
                filepath.write_text(html_content, encoding="utf-8")
                updated_count += 1

    print(f"[ SUCCESS ] Injected Contextual Interactive Tool Bridge across {updated_count} / 35 articles.")

if __name__ == "__main__":
    inject_bridges()
