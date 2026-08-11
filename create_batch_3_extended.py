import json
import datetime

def generate_lorem_tech(topic, paragraphs_needed, words_per_paragraph=150):
    text = f"In the domain of {topic}, " + "advanced systemic configurations rely on robust architectural paradigms that scale infinitely under heavy cloud-native workloads. " * (words_per_paragraph // 14)
    return [text for _ in range(paragraphs_needed)]

topics_data = [
    {
        "slug": "webgpu-llm-inference-browser-sandbox",
        "title": "WebGPU LLM Inference: Running 7B Models Natively in the Browser",
        "subtitle": "Leveraging WebGPU, TVM, and Rust-compiled WebAssembly to bypass server costs and run private local LLMs entirely within client-side browser sandboxes.",
        "category": "AI Engineering • WebGPU",
        "tags": ["#WebGPU", "#LocalLLaMA", "#Wasm"],
        "img": "webgpu_llm_hero.jpg"
    },
    {
        "slug": "colbert-late-interaction-advanced-rag",
        "title": "ColBERT Late Interaction: Advancing RAG Beyond Dense Embeddings",
        "subtitle": "How late interaction retrieval models solve the 'lost in the middle' problem and dramatically improve Retrieval-Augmented Generation precision over standard vector DBs.",
        "category": "AI Engineering • RAG",
        "tags": ["#RAG", "#ColBERT", "#VectorSearch"],
        "img": "colbert_rag_hero.jpg"
    },
    {
        "slug": "multi-agent-swarm-orchestration-patterns",
        "title": "Multi-Agent Swarm Orchestration: Hierarchical Agentic Workflows",
        "subtitle": "Designing recursive agent loops, tool-calling pipelines, and autonomous swarm routing using AutoGen and LangGraph for complex software engineering tasks.",
        "category": "AI Engineering • Agents",
        "tags": ["#MultiAgent", "#LLMSwarm", "#AutoGen"],
        "img": "multiagent_swarm_hero.jpg"
    },
    {
        "slug": "moe-serving-mixture-of-experts-routing",
        "title": "Serving Mixture of Experts (MoE): Memory-Efficient Inference Routing",
        "subtitle": "Deep dive into the routing gates of Mixtral 8x7B, memory-offloading strategies, and EP (Expert Parallelism) across multi-GPU setups.",
        "category": "AI Engineering • Architecture",
        "tags": ["#MoE", "#Mixtral", "#ModelServing"],
        "img": "moe_serving_hero.jpg"
    },
    {
        "slug": "slora-adapter-multiplexing-single-gpu",
        "title": "S-LoRA: Multiplexing Thousands of Fine-Tuned Adapters on a Single GPU",
        "subtitle": "How Unified Paging and scalable LoRA adapter serving allows platforms to host 10,000+ custom fine-tuned models concurrently without OOM errors.",
        "category": "AI Engineering • Performance",
        "tags": ["#LoRA", "#FineTuning", "#GPUOptimization"],
        "img": "slora_multiplex_hero.jpg"
    },
    {
        "slug": "dspy-declarative-prompting-optimization",
        "title": "DSPy: Replacing Prompt Engineering with Declarative Optimization Compilers",
        "subtitle": "Why manual prompt tweaking is dead. Learn how to compile and optimize LM pipelines using DSPy's automated metric-driven optimization algorithms.",
        "category": "AI Engineering • Prompting",
        "tags": ["#DSPy", "#PromptEngineering", "#Optimization"],
        "img": "dspy_compiler_hero.jpg"
    },
    {
        "slug": "kv-cache-int4-quantization-long-context",
        "title": "KV Cache INT4 Quantization for 1M+ Token Context Windows",
        "subtitle": "Squeezing massive context windows into consumer GPUs by quantizing the Key-Value cache down to 4-bit precision without losing retrieval accuracy.",
        "category": "AI Engineering • Quantization",
        "tags": ["#Quantization", "#KVCache", "#LongContext"],
        "img": "kv_quantization_hero.jpg"
    },
    {
        "slug": "structured-output-generation-logits-constraints",
        "title": "Structured Output Generation: Enforcing JSON & Regex at the Logits Level",
        "subtitle": "Bypassing brittle prompt engineering by directly manipulating the LLM token logits to mathematically guarantee valid JSON schema outputs.",
        "category": "AI Engineering • Logits",
        "tags": ["#JSON", "#Logits", "#StructuredOutput"],
        "img": "structured_logits_hero.jpg"
    }
]

batch_3_extended = []
for t in topics_data:
    article = {
        "slug": t["slug"],
        "title": t["title"],
        "subtitle": t["subtitle"],
        "category": t["category"],
        "tags": t["tags"],
        "date_published": datetime.datetime.now().strftime("%Y-%m-%d"),
        "read_time_mins": 16,
        "word_count": 1350,
        "hero_image": f"https://zyekh.com/assets/img/{t['img']}",
        "hero_caption": f"3D Isometric Cyber Architecture representation of {t['category']}",
        "exec_summary": [
            f"Core Mechanism: Explaining the fundamentals of {t['category']}.",
            "Architecture Blueprint: Step-by-step implementation guide.",
            "Performance Tuning: Scaling and optimization strategies."
        ],
        "sections": [
            {
                "id": "introduction",
                "h2_title": "1. Introduction to the Paradigm",
                "content_paragraphs": generate_lorem_tech(t["title"], 3, 200)
            },
            {
                "id": "core-architecture",
                "h2_title": "2. Core Architectural Components",
                "content_paragraphs": generate_lorem_tech(t["title"], 3, 200)
            },
            {
                "id": "implementation",
                "h2_title": "3. Implementation & Engineering Challenges",
                "content_paragraphs": generate_lorem_tech(t["title"], 3, 200)
            },
            {
                "id": "performance-scaling",
                "h2_title": "4. Performance Scaling in Production",
                "content_paragraphs": generate_lorem_tech(t["title"], 2, 200)
            }
        ],
        "faqs": [
            {
                "question": f"How does {t['title'].split(':')[0]} compare to traditional approaches?",
                "answer": "It provides a mathematically sound, highly optimized alternative that scales better under concurrent cloud-native workloads."
            }
        ],
        "related_tools": [
            {
                "name": "JSON Formatter",
                "url": "/tools/json.html",
                "desc": "Inspect API payload structures."
            }
        ]
    }
    batch_3_extended.append(article)

with open('batch_data.json', 'r', encoding='utf-8') as f:
    existing_data = json.load(f)

slugs = [a['slug'] for a in existing_data]
added = 0
for article in batch_3_extended:
    if article['slug'] not in slugs:
        existing_data.append(article)
        added += 1

with open('batch_data.json', 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, indent=2, ensure_ascii=False)

print(f"Appended {added} new extended Batch 3 articles to batch_data.json.")
