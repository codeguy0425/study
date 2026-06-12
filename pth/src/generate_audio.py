import os
import sys
import subprocess

base_dir = r"C:\Users\andy\Documents\dev\ai\antigravity\chinese_study\pth"

def generate_audio(topic_num):
    draft_file = os.path.join(base_dir, "drafts", f"topic{topic_num}.txt")
    dest_wav = os.path.join(base_dir, "audio", "drafts", f"topic{topic_num}.wav")
    
    if not os.path.exists(draft_file):
        print(f"ERROR: Draft file for Topic {topic_num} does not exist at {draft_file}")
        return
        
    with open(draft_file, 'r', encoding='utf-8') as f:
        text_content = f.read().strip()
    
    # We clean up any newlines or weird formatting to make it a continuous speech string.
    speech_text = text_content.replace("\n", " ").replace('"', '\\"').replace("——", "，")
    
    # PowerShell commands to speak and output to wave file
    ps_script = f"""
    Add-Type -AssemblyName System.Speech;
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $synth.SelectVoice("Microsoft Hanhan Desktop");
    $synth.SetOutputToWaveFile("{dest_wav}");
    $synth.Speak("{speech_text}");
    $synth.Dispose();
    """
    
    try:
        # Run the powershell script
        result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True, encoding="utf-8")
        if result.returncode == 0:
            print(f"SUCCESS: Synthesized Topic {topic_num} ({len(text_content)} chars) -> pth/audio/drafts/topic{topic_num}.wav")
        else:
            print(f"ERROR: Topic {topic_num} synthesis failed: {result.stderr.strip()}")
    except Exception as e:
        print(f"ERROR: Topic {topic_num} synthesis failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            topic_id = int(sys.argv[1])
            generate_audio(topic_id)
        except ValueError:
            print("ERROR: Please provide a valid integer topic ID (1-6)")
    else:
        # Default to Topic 5
        generate_audio(5)
