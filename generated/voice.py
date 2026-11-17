
import os
import json
import glob
import re
import subprocess
from gtts import gTTS

os.makedirs("audio", exist_ok=True)

files = glob.glob("generated/*.json")
if not files:
    raise FileNotFoundError("No joke JSON file found")

latest = max(files, key=os.path.getmtime)

with open(latest, "r", encoding="utf-8") as f:
    joke = json.load(f)

script = joke["script"].strip()
ending = joke.get("ending", "").strip()
full_text = script + " " + ending

# Generate Hindi voice
tts = gTTS(text=full_text, lang="hi", slow=False)
tts.save("audio/joke.mp3")

# Find actual audio duration
duration = float(subprocess.check_output([
    "ffprobe", "-v", "error",
    "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1",
    "audio/joke.mp3"
]).decode().strip())

# Split text into subtitle lines
parts = [
    p.strip() for p in re.split(r"(?<=[।!?])\s*|\n+", full_text)
    if p.strip()
]

total_chars = sum(len(p) for p in parts)
current = 0.0

def timestamp(seconds):
    ms = int(seconds * 1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

with open("audio/subtitles.srt", "w", encoding="utf-8") as f:
    for i, part in enumerate(parts, 1):
        segment = duration * len(part) / total_chars
        start = current
        end = current + segment
        f.write(f"{i}\n")
        f.write(f"{timestamp(start)} --> {timestamp(end)}\n")
        f.write(part + "\n\n")
        current = end

print("Hindi voiceover and subtitles created!")
