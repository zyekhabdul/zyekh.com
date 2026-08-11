import json
import os

def generate_llms_full():
    with open('batch_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    out = []
    out.append("# zyekh.com — Full Site RAG Knowledge Base\n")
    out.append("This file contains the complete content of zyekh.com for Generative Engine Optimization (GEO) and LLM indexing.\n\n")
    
    out.append("## About the Author\n")
    out.append("Zyekh Abdul Qadir Jailani is a Security Researcher & Architect focusing on Zero-Trust infrastructure, Linux security, and minimalist web engineering.\n\n")
    
    out.append("## Tools and Utilities\n")
    
    # Is there tool data in batch_data.json? Let's check first.
    # Actually batch_data.json only has articles it seems, wait, tools data?
    for item in data:
        if 'title' in item:
            out.append(f"### {item['title']}\n")
            if 'subtitle' in item:
                out.append(f"{item['subtitle']}\n\n")
            if 'exec_summary' in item:
                out.append("#### Executive Summary\n")
                for summ in item['exec_summary']:
                    out.append(f"- {summ}\n")
                out.append("\n")
            if 'sections' in item:
                for sec in item['sections']:
                    if 'h2_title' in sec:
                        out.append(f"#### {sec['h2_title']}\n")
                    if 'content_paragraphs' in sec:
                        for p in sec['content_paragraphs']:
                            out.append(f"{p}\n\n")
                    if 'code_block' in sec:
                        lang = sec.get('code_language', 'text')
                        out.append(f"```{lang}\n{sec['code_block']}\n```\n\n")
                    
            out.append("---\n\n")

    with open('llms-full.txt', 'w', encoding='utf-8') as f:
        f.write("".join(out))
        
if __name__ == "__main__":
    generate_llms_full()
    print("llms-full.txt generated.")
