import os
import re
import shutil

base_dir = r"C:\Users\andy\Documents\dev\ai\antigravity\chinese_study"

# 1. Custom overrides for Topic 5 characters (including corrected '地' to 'dì')
TOPIC_5_OVERRIDES = {
    # Pronunciation corrections
    "地": "dì",
    "一": "yī",
    "了": "le",
    "得": "de",
    "處": "chǔ",
    "共": "gòng",
    "和": "hé",
    "與": "yǔ",
    "是": "shì",
    "個": "gè",
    "次": "cì",
    "大": "dà",
    "上": "shàng",
    "方": "fāng",
    "識": "shi",
    "把": "bǎ",
    
    # Missing 49 characters
    "享": "xiǎng",
    "今": "jīn",
    "介": "jiè",
    "但": "dàn",
    "充": "chōng",
    "匙": "shi",
    "又": "yòu",
    "向": "xiàng",
    "圖": "tú",
    "完": "wán",
    "形": "xíng",
    "影": "yǐng",
    "彷": "fǎng",
    "彿": "fú",
    "戶": "hù",
    "打": "dǎ",
    "找": "zhǎo",
    "束": "shù",
    "樂": "lè",
    "死": "sǐ",
    "洋": "yáng",
    "湃": "pài",
    "滿": "mǎn",
    "澎": "péng",
    "硬": "yìng",
    "紹": "shào",
    "結": "jié",
    "聳": "sǒng",
    "背": "bèi",
    "脈": "mài",
    "行": "xíng",
    "覺": "jué",
    "討": "tǎo",
    "記": "jì",
    "諧": "xié",
    "趣": "qù",
    "足": "zú",
    "遍": "biàn",
    "釋": "shì",
    "鑰": "yào",
    "需": "xū",
    "靈": "líng",
    "顆": "kē",
    "類": "lèi",
    "高": "gāo",
    "麗": "lì",
}

def extract_baseline_pinyin(scripts_html_path):
    """
    Parses scripts.html to build a baseline dictionary mapping characters to pinyin.
    """
    char_pinyin_map = {}
    if os.path.exists(scripts_html_path):
        with open(scripts_html_path, "r", encoding="utf-8") as f:
            content = f.read()
        matches = re.findall(r"<ruby>([^<]+)<rt>([^<]+)</rt></ruby>", content)
        for char, pinyin in matches:
            char_pinyin_map[char.strip()] = pinyin.strip()
    return char_pinyin_map

def compile_text_to_ruby(text, char_pinyin_map, overrides):
    """
    Converts plain text to a string containing HTML <ruby> tags for Chinese characters.
    Non-Chinese characters are preserved exactly.
    """
    compiled_parts = []
    for char in text:
        # Check if the character is in the Chinese Unicode range
        if "\u4e00" <= char <= "\u9fff":
            # 1. Check if we have an explicit override (priority)
            if char in overrides:
                pinyin = overrides[char]
            # 2. Check if we have a baseline mapping from other topics
            elif char in char_pinyin_map:
                pinyin = char_pinyin_map[char]
            else:
                raise ValueError(f"ERROR: No pinyin mapping found for character '{char}'! Please add it to TOPIC_5_OVERRIDES.")
            compiled_parts.append(f"<ruby>{char}<rt>{pinyin}</rt></ruby>")
        else:
            # Preserve spacing, newlines, and punctuation exactly
            compiled_parts.append(char)
            
    return "".join(compiled_parts)

def build_topic_5():
    print("=" * 60)
    print("BUILDING AND PUBLISHING TOPIC 5")
    print("=" * 60)
    
    # Paths
    scripts_html = os.path.join(base_dir, "pth", "scripts.html")
    scripts_template = os.path.join(base_dir, "pth", "templates", "scripts_template.html")
    print_html = os.path.join(base_dir, "pth", "print.html")
    print_template = os.path.join(base_dir, "pth", "templates", "print_template.html")
    topic5_draft = os.path.join(base_dir, "pth", "drafts", "topic5.txt")
    sw_file = os.path.join(base_dir, "sw.js")
    
    draft_wav = os.path.join(base_dir, "pth", "audio", "drafts", "topic5.wav")
    dest_wav = os.path.join(base_dir, "pth", "topic5.wav")
    
    # Verify sources
    if not os.path.exists(topic5_draft):
        print(f"ERROR: Topic 5 draft not found at {topic5_draft}")
        return
    if not os.path.exists(draft_wav):
        print(f"ERROR: Topic 5 draft audio not found at {draft_wav}")
        return
        
    # Read draft text
    with open(topic5_draft, "r", encoding="utf-8") as f:
        draft_text = f.read().strip()
        
    # 1. Promote WAV to production root
    print(f"Promoting WAV: {draft_wav} -> {dest_wav}")
    shutil.copy2(draft_wav, dest_wav)
    print("SUCCESS: Audio WAV file promoted.")
    
    # 2. Build Character Map from scripts.html (using it as our reference database)
    char_map = extract_baseline_pinyin(scripts_html)
    print(f"Loaded {len(char_map)} baseline character-to-pinyin mappings.")
    
    # 3. Compile Topic 5 text to Ruby HTML elements
    try:
        compiled_ruby_text = compile_text_to_ruby(draft_text, char_map, TOPIC_5_OVERRIDES)
        print("SUCCESS: Plain text draft compiled to <ruby> HTML successfully.")
    except Exception as e:
        print(f"Compilation Failed: {e}")
        return

    # 4. Inject into scripts.html
    if os.path.exists(scripts_template):
        with open(scripts_template, "r", encoding="utf-8") as f:
            template_content = f.read()
            
        # Specific regex pattern to target only the textWithRuby value inside Topic 5's block
        pattern = r'(id:\s*["\']5["\'],\s*title:\s*["\']介紹一個你最喜歡的科目["\'],\s*wav:\s*["\']topic5\.wav["\'],\s*textWithRuby:\s*`)([\s\S]*?)(`)'
        
        # We replace the matched content with the compiled ruby text
        modified_content, count = re.subn(pattern, rf"\g<1>\n          {compiled_ruby_text}\n        \g<3>", template_content)
        
        if count > 0:
            with open(scripts_html, "w", encoding="utf-8") as f:
                f.write(modified_content)
            print(f"SUCCESS: Injected ruby text into {scripts_html} ({count} replacement).")
        else:
            print(f"WARNING: Regex did not match Topic 5 block in {scripts_template}!")
    else:
        print(f"ERROR: scripts_template.html does not exist at {scripts_template}")

    # 5. Inject into print.html
    if os.path.exists(print_template):
        with open(print_template, "r", encoding="utf-8") as f:
            print_template_content = f.read()
            
        # Target the body container inside the <!-- Topic 5 --> section of print_template.html
        print_pattern = r'(<!-- Topic 5 -->[\s\S]*?<div class="topic-body[^"]*">)([\s\S]*?)(</div>\s*</section>)'
        
        modified_print_content, count = re.subn(print_pattern, rf"\g<1>\n        {compiled_ruby_text}\n      \g<3>", print_template_content)
        
        if count > 0:
            with open(print_html, "w", encoding="utf-8") as f:
                f.write(modified_print_content)
            print(f"SUCCESS: Injected ruby text into {print_html} ({count} replacement).")
        else:
            print(f"WARNING: Regex did not match Topic 5 section in {print_template}!")
    else:
        print(f"ERROR: print_template.html does not exist at {print_template}")
        
    # 6. Increment service worker cache version
    if os.path.exists(sw_file):
        with open(sw_file, "r", encoding="utf-8") as f:
            sw_content = f.read()
            
        # Find idioms-pwa-vX pattern and increment version
        sw_version_pattern = r"const CACHE_NAME = 'idioms-pwa-v(\d+)';"
        match = re.search(sw_version_pattern, sw_content)
        if match:
            current_ver = int(match.group(1))
            new_ver = current_ver + 1
            new_sw_content = re.sub(sw_version_pattern, f"const CACHE_NAME = 'idioms-pwa-v{new_ver}';", sw_content)
            
            with open(sw_file, "w", encoding="utf-8") as f:
                f.write(new_sw_content)
            print(f"SUCCESS: Sw.js cache version bumped from v{current_ver} to v{new_ver}.")
        else:
            print("WARNING: sw.js CACHE_NAME pattern not found. Manual update needed.")
            
    print("=" * 60)
    print("BUILD COMPLETED FOR TOPIC 5!")
    print("=" * 60)

if __name__ == "__main__":
    build_topic_5()
