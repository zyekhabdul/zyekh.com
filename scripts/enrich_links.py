#!/usr/bin/env python3
"""
Enriches early articles with contextual in-body internal links to interactive client-side tools.
"""

from bs4 import BeautifulSoup
import os

TOOL_MAPPINGS = {
    "blog/chroot-jail-and-unprivileged-namespaces-isolation.html": {
        "tool_url": "/tools/chmod-calculator.html",
        "tool_name": "Linux Chmod & Permissions Calculator",
        "sentence": "File permissions and directory access masks can be modeled using our interactive"
    },
    "blog/ebpf-xdp-packet-filtering-and-ddos-mitigation.html": {
        "tool_url": "/tools/subnet.html",
        "tool_name": "Subnet & CIDR Calculator",
        "sentence": "Target IP addresses and malicious CIDR network ranges can be calculated using our"
    },
    "blog/fail2ban-intrusion-prevention-and-ssh-abuse-mitigation.html": {
        "tool_url": "/tools/pam-generator.html",
        "tool_name": "Linux PAM Faillock Config Generator",
        "sentence": "Account lockout thresholds and brute-force mitigation rules can be generated via our"
    },
    "blog/linux-vps-hardening-guide-2026.html": {
        "tool_url": "/tools/linux-hardening-generator.html",
        "tool_name": "Linux Hardening Config Builder",
        "sentence": "Hardened SSH and kernel sysctl parameters can be generated automatically using our"
    },
    "blog/minimalist-server-architecture-pure-css-and-static-hosting.html": {
        "tool_url": "/tools/css-minifier.html",
        "tool_name": "Client-Side CSS Minifier Tool",
        "sentence": "Production stylesheets can be compressed and stripped of comments using our"
    },
    "blog/nginx-reverse-proxy-security-hardening-blueprint-2026.html": {
        "tool_url": "/tools/curl.html",
        "tool_name": "Curl Command Builder",
        "sentence": "HTTP request headers, TLS ciphers, and rate-limit responses can be tested using our"
    },
    "blog/securing-web-applications-with-strict-content-security-policy.html": {
        "tool_url": "/tools/hash.html",
        "tool_name": "Cryptographic Hash Generator",
        "sentence": "Script nonces and inline SHA-256 integrity digests can be calculated using our"
    },
    "blog/systemd-service-sandboxing-and-security-hardening.html": {
        "tool_url": "/tools/chmod-calculator.html",
        "tool_name": "Linux Chmod Calculator",
        "sentence": "Filesystem sandbox restrictions and directory masks can be verified with our"
    },
    "blog/ufw-firewall-hardening-and-rate-limiting-blueprint-2026.html": {
        "tool_url": "/tools/subnet.html",
        "tool_name": "Subnet Calculator",
        "sentence": "Allowed network CIDR blocks and IP mask ranges can be computed using our"
    },
    "blog/understanding-linux-ebpf-security-monitoring.html": {
        "tool_url": "/tools/diff-checker.html",
        "tool_name": "Text & Config Diff Checker",
        "sentence": "Kernel trace outputs and system call filter rules can be compared using our"
    },
    "blog/wireguard-vpn-tunneling-for-secure-vps-mesh-networks.html": {
        "tool_url": "/tools/subnet.html",
        "tool_name": "Subnet & CIDR Calculator",
        "sentence": "Private mesh VPN address allocations and peer IP blocks can be calculated via our"
    },
    "blog/zero-trust-ssh-access-with-fido2-and-ssh-ca.html": {
        "tool_url": "/tools/jwt.html",
        "tool_name": "JWT Token Inspector",
        "sentence": "Short-lived authentication claims and cryptographic identity assertions can be decoded with our"
    }
}

def enrich():
    count = 0
    for fpath, meta in TOOL_MAPPINGS.items():
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", encoding="utf-8") as fp:
            html = fp.read()
        
        soup = BeautifulSoup(html, "html.parser")
        main = soup.find("main", class_="article-content")
        if not main:
            continue
        
        ps = main.find_all("p")
        if len(ps) >= 2:
            target_p = ps[1]
            if meta["tool_url"] not in str(target_p):
                new_soup = BeautifulSoup(f' {meta["sentence"]} <a href="{meta["tool_url"]}">{meta["tool_name"]}</a>.', 'html.parser')
                target_p.append(new_soup)
                with open(fpath, "w", encoding="utf-8") as fp:
                    fp.write(str(soup))
                count += 1
                print(f"[ENRICHED] {fpath}")

    print(f"Total files cleanly enriched: {count}")

if __name__ == "__main__":
    enrich()
