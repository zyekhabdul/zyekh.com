import os

def check_emojis(directory):
    for root, _, files in os.walk(directory):
        if '.git' in root or '__pycache__' in root or '.gemini' in root:
            continue
        for file in files:
            if file.endswith(('.html', '.css', '.js', '.json', '.md')):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # simple heuristic for emojis block
                        emojis = [c for c in content if '\U00010000' <= c <= '\U0010ffff']
                        if emojis:
                            print(f"{path}: Found potential emojis: {set(emojis)}")
                except Exception as e:
                    pass

check_emojis('.')
