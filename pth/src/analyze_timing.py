import os
import sys
import wave
import re

base_dir = r"C:\Users\andy\Documents\dev\ai\antigravity\chinese_study\pth"

def count_chinese_chars(text):
    # Regex to match Chinese characters (Unicode range for CJK Unified Ideographs)
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)

def analyze_topic(topic_num):
    draft_file = os.path.join(base_dir, "drafts", f"topic{topic_num}.txt")
    
    if not os.path.exists(draft_file):
        print(f"ERROR: Draft file for Topic {topic_num} does not exist at {draft_file}")
        return
        
    with open(draft_file, 'r', encoding='utf-8') as f:
        text_content = f.read().strip()
        
    total_chars = len(text_content.replace("\n", "").replace(" ", ""))
    chinese_chars_count = count_chinese_chars(text_content)
    
    # Comfortable oral speaking pace: roughly 135 Chinese characters per minute (2.25 chars per second)
    # Standard exam reading: ~120 to 140 characters for 60 seconds.
    est_duration_comfort = chinese_chars_count / 2.25  # 135 cpm
    
    print("=" * 60)
    print(f"TIMING ANALYSIS FOR TOPIC {topic_num}")
    print("=" * 60)
    print(f"Draft File:      pth/drafts/topic{topic_num}.txt")
    print(f"Chinese Chars:   {chinese_chars_count} characters")
    print(f"Total Length:    {total_chars} symbols (including punctuation)")
    print(f"Est. speaking:   ~{est_duration_comfort:.1f} seconds (at standard pace ~135 cpm)")
    print("-" * 60)
    
    # Check for WAV files (prioritize drafts, then published)
    draft_wav = os.path.join(base_dir, "audio", "drafts", f"topic{topic_num}.wav")
    published_wav = os.path.join(base_dir, "audio", "published", f"topic{topic_num}.wav")
    legacy_wav = os.path.join(base_dir, f"topic{topic_num}.wav")
    
    wav_path = None
    source_label = ""
    
    if os.path.exists(draft_wav):
        wav_path = draft_wav
        source_label = "Draft Folder (audio/drafts/)"
    elif os.path.exists(published_wav):
        wav_path = published_wav
        source_label = "Published Folder (audio/published/)"
    elif os.path.exists(legacy_wav):
        wav_path = legacy_wav
        source_label = "Legacy Root Folder (pth/)"
        
    if wav_path:
        try:
            with wave.open(wav_path, 'rb') as w:
                frames = w.getnframes()
                rate = w.getframerate()
                actual_duration = frames / float(rate)
                
            print(f"Audio Source:    {source_label}")
            print(f"Actual Duration: {actual_duration:.2f} seconds")
            
            # Check if duration is close to 60s sweet spot (55s - 65s)
            if 55.0 <= actual_duration <= 65.0:
                print(f"STATUS:          Perfect timing! ({actual_duration:.1f}s is inside 55s-65s sweet spot)")
            elif actual_duration < 55.0:
                shortfall = 60.0 - actual_duration
                print(f"STATUS:          A bit too short! ({actual_duration:.1f}s). Need ~{shortfall:.1f}s more text.")
            else:
                excess = actual_duration - 60.0
                print(f"STATUS:          A bit too long! ({actual_duration:.1f}s). Need to trim ~{excess:.1f}s of text.")
                
            actual_speed = chinese_chars_count / (actual_duration / 60.0)
            print(f"Actual Pace:     {actual_speed:.1f} characters per minute")
            
        except Exception as e:
            print(f"Error reading WAV file: {e}")
    else:
        print("STATUS:          No audio WAV file found. Run or record audio first.")
        
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            topic_id = int(sys.argv[1])
            analyze_topic(topic_id)
        except ValueError:
            print("ERROR: Please provide a valid integer topic ID (1-6)")
    else:
        # Default to analyzing topic 5 if no argument given
        analyze_topic(5)
