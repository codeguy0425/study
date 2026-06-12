import os
import sys
import re
import shutil
import json

base_dir = r"C:\Users\andy\Documents\dev\ai\antigravity\chinese_study"

# 1. Global character-level overrides (corrections and mappings)
GLOBAL_OVERRIDES = {
    # Pronunciation corrections
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
    "著": "zhe",
    "還": "hái",
    "好": "hǎo",
    
    # Missing characters from previous mappings
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
    "見": "jiàn",
    "交": "jiāo",
    "代": "dài",
    "獨": "dú",
    "野": "yě",
    
    # Topic 1 missing mappings
    "兩": "liǎng",
    "具": "jù",
    "初": "chū",
    "千": "qiān",
    "午": "wǔ",
    "原": "yuán",
    "口": "kǒu",
    "守": "shǒu",
    "屈": "qū",
    "巷": "xiàng",
    "念": "niàn",
    "承": "chéng",
    "揮": "huī",
    "於": "yú",
    "昂": "áng",
    "槳": "jiǎng",
    "沸": "fèi",
    "清": "qīng",
    "爭": "zhēng",
    "百": "bǎi",
    "着": "zhe",
    "種": "zhǒng",
    "立": "lì",
    "端": "duān",
    "粽": "zòng",
    "紀": "jì",
    "肉": "ròu",
    "興": "xīng",
    "舟": "zhōu",
    "舸": "gě",
    "英": "yīng",
    "莫": "mò",
    "葉": "yè",
    "血": "xuè",
    "街": "jiē",
    "設": "shè",
    "詩": "shī",
    "護": "hù",
    "載": "zài",
    "飄": "piāo",
    "騰": "téng",
    "鹹": "xián",
    "鹼": "jiǎn",
    "點": "diǎn",
    "龍": "lóng",
    
    # Topic 4 missing mappings
    "令": "lìng",
    "勝": "shèng",
    "協": "xié",
    "員": "yuán",
    "堂": "táng",
    "契": "qì",
    "強": "qiáng",
    "待": "dài",
    "戰": "zhàn",
    "挑": "tiǎo",
    "掣": "chè",
    "接": "jiē",
    "擬": "nǐ",
    "期": "qī",
    "榮": "róng",
    "汗": "hàn",
    "法": "fǎ",
    "短": "duǎn",
    "舞": "wǔ",
    "譽": "yù",
    "身": "shēn",
    "配": "pèi",
    "陸": "lù",
    "集": "jí",
    "電": "diàn",
    "靜": "jìng",
    "項": "xiàng",
    "風": "fēng",
    "馳": "chí",
    "驕": "jiāo",
    "齊": "qí",
    
    # Topic 6 missing mappings
    "之": "zhī",
    "事": "shì",
    "些": "xiē",
    "亮": "liàng",
    "份": "fèn",
    "位": "wèi",
    "你": "nǐ",
    "依": "yī",
    "單": "dān",
    "回": "huí",
    "太": "tài",
    "已": "yǐ",
    "幸": "xìng",
    "微": "wēi",
    "忘": "wàng",
    "您": "nín",
    "懂": "dǒng",
    "或": "huò",
    "戲": "xì",
    "敢": "gǎn",
    "易": "yì",
    "枯": "kū",
    "業": "yè",
    "正": "zhèng",
    "準": "zhǔn",
    "燥": "zào",
    "甚": "shèn",
    "畏": "wèi",
    "畢": "bì",
    "發": "fā",
    "簡": "jiǎn",
    "糾": "jiū",
    "經": "jīng",
    "至": "zhì",
    "許": "xǔ",
    "語": "yǔ",
    "誨": "huì",
    "雖": "suī",
    "音": "yīn",
    
    # Topic 2 missing mappings
    "伴": "bàn",
    "備": "bèi",
    "優": "yōu",
    "功": "gōng",
    "唱": "chàng",
    "愉": "yú",
    "折": "zhé",
    "挫": "cuò",
    "書": "shū",
    "滴": "dī",
    "病": "bìng",
    "聯": "lián",
    "菜": "cài",
    "融": "róng",
    "讀": "dú",
    "陪": "péi",
    "飯": "fàn",
    
    # Topic 1 rewritten missing mappings
    "他": "tā",
    "便": "biàn",
    "俗": "sú",
    "傷": "shāng",
    "入": "rù",
    "其": "qí",
    "划": "huá",
    "另": "lìng",
    "吃": "chī",
    "姓": "xìng",
    "害": "hài",
    "將": "jiāng",
    "徵": "zhēng",
    "憂": "yōu",
    "投": "tóu",
    "救": "jiù",
    "止": "zhǐ",
    "民": "mín",
    "江": "jiāng",
    "源": "yuán",
    "營": "yíng",
    "盡": "jìn",
    "米": "mǐ",
    "糯": "nuò",
    "船": "chuán",
    "華": "huá",
    "蝦": "xiā",
    "軟": "ruǎn",
    "防": "fáng",
    "震": "zhèn",
    "食": "shí",
    "鮮": "xiān",
    
    # Topic 4 rewritten missing mappings
    "下": "xià",
    "互": "hù",
    "利": "lì",
    "努": "nǔ",
    "友": "yǒu",
    "因": "yīn",
    "展": "zhǎn",
    "己": "jǐ",
    "很": "hěn",
    "所": "suǒ",
    "才": "cái",
    "擅": "shàn",
    "擲": "zhì",
    "棒": "bàng",
    "氛": "fēn",
    "油": "yóu",
    "給": "gěi",
    "舉": "jǔ",
    "誼": "yì",
    "起": "qǐ",
    "跳": "tiào",
    "遠": "yuǎn",
    "邊": "biān",
    "隊": "duì",
    
    # Topic 2 rewritten missing mappings
    "則": "zé",
    "半": "bàn",
    "卻": "què",
    "句": "jù",
    "奏": "zòu",
    "後": "hòu",
    "放": "fàng",
    "未": "wèi",
    "段": "duàn",
    "達": "dá",
    
    # Topic 6 rewritten missing mappings
    "困": "kùn",
    "基": "jī",
    "字": "zì",
    "容": "róng",
    "導": "dǎo",
    "建": "jiàn",
    "怕": "pà",
    "慢": "màn",
    "犯": "fàn",
    "產": "chǎn",
    "礎": "chǔ",
    "者": "zhě",
    "良": "liáng",
    "進": "jìn",
    "錯": "cuò",
    "關": "guān",
    "除": "chú",
    "階": "jiē",
    "幫": "bāng",
    "暖": "nuǎn",
    
    # Topic 3 rewritten missing mappings
    "久": "jiǔ",
    "住": "zhù",
    "夜": "yè",
    "居": "jū",
    "帝": "dì",
    "悠": "yōu",
    "慧": "huì",
    "景": "jǐng",
    "智": "zhì",
    "毅": "yì",
    "濃": "nóng",
    "物": "wù",
    "珍": "zhēn",
    "皇": "huáng",
    "知": "zhī",
    "站": "zhàn",
    "築": "zhú",
    "繁": "fán",
    "蜿": "wān",
    "蜒": "yán",
    "貴": "guì",
    "走": "zǒu",
    "蹟": "jì",
    "道": "dào",
    "間": "jiān",
    "面": "miàn",
    "欣": "xīn",
    "賞": "shǎng",
    "那": "nà",
    
    # Topic 5 missing mappings
    "助": "zhù",
    "各": "gè",
    "問": "wèn",
    "境": "jìng",
    "川": "chuān",
    "布": "bù",
    "式": "shì",
    "晰": "xī",
    "環": "huán",
    "眼": "yǎn",
    "置": "zhì",
    "變": "biàn",
    "資": "zī",
    "透": "tòu",
    "通": "tōng",
    "連": "lián",
    "過": "guò",
    "闊": "kuò",
    "題": "tí",
    "保": "bǎo",
}

# 2. Topic-specific overrides for polyphonic characters
TOPIC_SPECIFIC_OVERRIDES = {
    "1": {
        "地": "dì",     # 地方 (dì fāng)
    },
    "2": {
        "重": "chóng",   # 重新 (chóng xīn)
    },
    "3": {
        "地": "dì",     # 地方, 實地, 當地 (dì)
        "都": "dū",     # 首都 (shǒu dū)
        "長": "cháng",   # 萬里長城, 長城 (cháng)
        "城": "chéng",   # 長城 (chéng)
        "廈": "shà",     # 高樓大廈 (shà)
        "輝": "huī",     # 輝映 (huī)
        "映": "yìng",    # 輝映 (yìng)
        "魅": "mèi",     # 魅力 (mèi)
        "力": "lì",      # 魅力 (lì)
        "四": "sì",      # 四合院 (sì)
        "合": "hé",      # 四合院 (hé)
        "院": "yuàn",    # 四合院 (yuàn)
        "樓": "lóu",     # 高樓 (lóu)
    },
    "4": {
        "地": "dì",     # 目的地 (mù dì dì)
    },
    "5": {
        "地": "dì",     # 地理 (dì lǐ)
    },
    "6": {
        "地": "de",     # 溫柔地, 耐心地 (de)
    }
}

# 3. Multi-character word overrides to cleanly handle polyphonic words in context
WORD_OVERRIDES = {
    "著名": ["zhù", "míng"],
    "好奇": ["hào", "qí"],
    "好漢": ["hǎo", "hàn"],
    "首都": ["shǒu", "dū"],
    "重新": ["chóng", "xīn"],
    "認為": ["rèn", "wéi"],
    "身為": ["shēn", "wéi"],
    "為了": ["wèi", "le"],
}

def load_baseline_pinyin():
    """
    Loads baseline character-to-pinyin mappings from char_map.json.
    """
    json_path = os.path.join(base_dir, "pth", "src", "char_map.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    print(f"WARNING: char_map.json not found at {json_path}. Returning empty map.")
    return {}

def compile_text_to_ruby(text, char_pinyin_map, overrides, topic_num):
    """
    Converts plain text to a string containing HTML <ruby> tags for Chinese characters.
    Non-Chinese characters are preserved exactly.
    Handles multi-character word overrides first to resolve polyphonic context.
    """
    compiled_parts = []
    i = 0
    n = len(text)
    
    while i < n:
        # 1. Try word-level overrides first (longest match)
        matched_word = None
        for word, pinyins in sorted(WORD_OVERRIDES.items(), key=lambda x: len(x[0]), reverse=True):
            if text.startswith(word, i):
                matched_word = (word, pinyins)
                break
                
        if matched_word:
            word, pinyins = matched_word
            for char, pinyin in zip(word, pinyins):
                compiled_parts.append(f"<ruby>{char}<rt>{pinyin}</rt></ruby>")
            i += len(word)
            continue
            
        char = text[i]
        # 2. Character-level fallback
        if "\u4e00" <= char <= "\u9fff":
            # Check if we have an explicit override (priority)
            if char in overrides:
                pinyin = overrides[char]
            # Check if we have a baseline mapping from other topics
            elif char in char_pinyin_map:
                pinyin = char_pinyin_map[char]
            else:
                raise ValueError(
                    f"ERROR: No pinyin mapping found for character '{char}' (Unicode: \\u{ord(char):04x}) in Topic {topic_num}!\n"
                    f"Please add it to GLOBAL_OVERRIDES or TOPIC_SPECIFIC_OVERRIDES inside pth/src/build.py."
                )
            compiled_parts.append(f"<ruby>{char}<rt>{pinyin}</rt></ruby>")
        else:
            # Preserve spacing, newlines, and punctuation exactly
            compiled_parts.append(char)
        i += 1
            
    return "".join(compiled_parts)


def build_topic(topic_num, scripts_html, scripts_template, print_html, print_template, char_map):
    print("-" * 60)
    print(f"COMPILING TOPIC {topic_num}")
    print("-" * 60)
    
    topic_draft = os.path.join(base_dir, "pth", "drafts", f"topic{topic_num}.txt")
    draft_wav = os.path.join(base_dir, "pth", "audio", "drafts", f"topic{topic_num}.wav")
    dest_wav = os.path.join(base_dir, "pth", f"topic{topic_num}.wav")
    
    if not os.path.exists(topic_draft):
        print(f"Skipping Topic {topic_num}: Draft text not found at {topic_draft}")
        return None, None
        
    if not os.path.exists(draft_wav):
        print(f"Skipping Topic {topic_num}: Draft audio not found at {draft_wav}")
        return None, None
        
    # Read draft text
    with open(topic_draft, "r", encoding="utf-8") as f:
        draft_text = f.read().strip()
        
    # 1. Promote WAV to production root
    print(f"Promoting WAV: {draft_wav} -> {dest_wav}")
    shutil.copy2(draft_wav, dest_wav)
    print(f"SUCCESS: Audio promoted.")
    
    # 2. Compile Topic text to Ruby HTML elements
    overrides = dict(GLOBAL_OVERRIDES)
    topic_overrides = TOPIC_SPECIFIC_OVERRIDES.get(str(topic_num), {})
    overrides.update(topic_overrides)
    
    try:
        compiled_ruby_text = compile_text_to_ruby(draft_text, char_map, overrides, topic_num)
        print(f"SUCCESS: Plain text draft compiled to <ruby> HTML.")
        return compiled_ruby_text, draft_text
    except Exception as e:
        print(f"Compilation Failed for Topic {topic_num}: {e}")
        raise e

def main():
    # Paths
    scripts_html = os.path.join(base_dir, "pth", "scripts.html")
    scripts_template = os.path.join(base_dir, "pth", "templates", "scripts_template.html")
    print_html = os.path.join(base_dir, "pth", "print.html")
    print_template = os.path.join(base_dir, "pth", "templates", "print_template.html")
    sw_file = os.path.join(base_dir, "sw.js")
    
    # Load Character Map from char_map.json
    char_map = load_baseline_pinyin()
    print(f"Loaded {len(char_map)} baseline character-to-pinyin mappings.")
    
    # Determine which topics to build
    topics_to_build = []
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "all":
            topics_to_build = ["1", "2", "3", "4", "5", "6"]
        else:
            topics_to_build = [arg for arg in sys.argv[1:] if arg in ["1", "2", "3", "4", "5", "6"]]
    else:
        # Default: auto-detect topics that have both txt draft and drafts wav
        for i in range(1, 7):
            t_num = str(i)
            topic_draft = os.path.join(base_dir, "pth", "drafts", f"topic{t_num}.txt")
            draft_wav = os.path.join(base_dir, "pth", "audio", "drafts", f"topic{t_num}.wav")
            if os.path.exists(topic_draft) and os.path.exists(draft_wav):
                topics_to_build.append(t_num)
                
    if not topics_to_build:
        print("No topics specified or auto-detected for compilation.")
        return
        
    print("=" * 60)
    print(f"STARTING COMPILATION FOR TOPICS: {', '.join(topics_to_build)}")
    print("=" * 60)
    
    # Read templates
    if not os.path.exists(scripts_template):
        print(f"ERROR: scripts_template.html not found at {scripts_template}")
        return
    if not os.path.exists(print_template):
        print(f"ERROR: print_template.html not found at {print_template}")
        return
        
    with open(scripts_template, "r", encoding="utf-8") as f:
        scripts_content = f.read()
        
    with open(print_template, "r", encoding="utf-8") as f:
        print_content = f.read()
        
    built_count = 0
    
    for t_num in topics_to_build:
        try:
            compiled_ruby, draft_text = build_topic(t_num, scripts_html, scripts_template, print_html, print_template, char_map)
            if compiled_ruby:
                # 4. Inject into scripts.html content (using template as master)
                pattern = rf'(id:\s*["\']{t_num}["\'],\s*title:\s*["\'][^"\']+["\'],\s*wav:\s*["\']topic{t_num}\.wav["\'],\s*textWithRuby:\s*`)([\s\S]*?)(`)'
                scripts_content, count = re.subn(pattern, rf"\g<1>\n          {compiled_ruby}\n        \g<3>", scripts_content)
                if count > 0:
                    print(f"SUCCESS: Injected ruby text into scripts content ({count} replacement).")
                else:
                    print(f"WARNING: Regex did not match Topic {t_num} block in scripts_template!")
                    
                # 5. Inject into print.html content
                print_pattern = rf'(<!-- Topic {t_num} -->[\s\S]*?<div class="topic-body[^"]*">)([\s\S]*?)(</div>\s*</section>)'
                print_content, count = re.subn(print_pattern, rf"\g<1>\n        {compiled_ruby}\n      \g<3>", print_content)
                if count > 0:
                    print(f"SUCCESS: Injected ruby text into print content ({count} replacement).")
                else:
                    print(f"WARNING: Regex did not match Topic {t_num} section in print_template!")
                
                built_count += 1
        except Exception as e:
            print(f"Skipping topic {t_num} compilation due to error.")
            return
            
    if built_count > 0:
        # Write modified files to production targets
        with open(scripts_html, "w", encoding="utf-8") as f:
            f.write(scripts_content)
        print(f"SUCCESS: Wrote compiled HTML to {scripts_html}")
        
        with open(print_html, "w", encoding="utf-8") as f:
            f.write(print_content)
        print(f"SUCCESS: Wrote compiled HTML to {print_html}")
        
        # Write back to master templates to permanently prevent template drift
        with open(scripts_template, "w", encoding="utf-8") as f:
            f.write(scripts_content)
        print(f"SUCCESS: Updated master template {scripts_template}")
        
        with open(print_template, "w", encoding="utf-8") as f:
            f.write(print_content)
        print(f"SUCCESS: Updated master template {print_template}")
        
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
                print(f"SUCCESS: sw.js cache version bumped from v{current_ver} to v{new_ver}.")
            else:
                print("WARNING: sw.js CACHE_NAME pattern not found. Manual update needed.")
                
        print("=" * 60)
        print(f"BUILD COMPLETED SUCCESSFULLY FOR {built_count} TOPICS!")
        print("=" * 60)
    else:
        print("No topics built.")

if __name__ == "__main__":
    main()
