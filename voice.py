
import os
import json
import glob
import subprocess
from gtts import gTTS

os.makedirs("audio", exist_ok=True)
os.makedirs("audio/temp", exist_ok=True)

files = glob.glob("generated/*.json")
if not files:
    raise FileNotFoundError("No joke JSON file found")

latest = max(files, key=os.path.getmtime)

with open(latest, "r", encoding="utf-8") as f:
    joke = json.load(f)

dialogue = joke["dialogue"]
dialogue.append({
    "speaker": "Sunny",
    "text": joke.get("ending", "")
})

def get_duration(path):
    result = subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path
    ])
    return float(result.decode().strip())

def timestamp(seconds):
    ms = int(seconds * 1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

segments = []

for i, line in enumerate(dialogue):
    text = line["text"].strip()
    if not text:
        continue

    speaker = line["speaker"].lower()

    # Bobby: slightly lower pitch
    # Sunny: slightly higher pitch
    pitch = 0.94 if speaker == "bobby" else 1.07

    raw_file = f"audio/temp/raw_{i}.mp3"
    final_file = f"audio/temp/voice_{i}.mp3"

    tts = gTTS(text=text, lang="hi", slow=False)
    tts.save(raw_file)

    subprocess.run([
        "ffmpeg", "-y", "-i", raw_file,
        "-af",
        f"asetrate=44100*{pitch},aresample=44100,"
        f"atempo={1/pitch}",
        "-ar", "44100",
        "-ac", "2",
        final_file
    ], check=True)

    segments.append({
        "file": final_file,
        "text": text,
        "duration": get_duration(final_file)
    })

if not segments:
    raise RuntimeError("No dialogue was generated")

# Combine all dialogue audio
command = ["ffmpeg", "-y"]

for segment in segments:
    command += ["-i", segment["file"]]

filters = "".join(
    f"[{i}:a]"
    for i in range(len(segments))
)

filters += (
    f"concat=n={len(segments)}:v=0:a=1[outa]"
)

command += [
    "-filter_complex", filters,
    "-map", "[outa]",
    "-c:a", "libmp3lame",
    "-q:a", "3",
    "audio/joke.mp3"
]

subprocess.run(command, check=True)

# Create synchronized subtitles
current = 0.0

with open("audio/subtitles.srt", "w", encoding="utf-8") as f:
    for i, segment in enumerate(segments, 1):
        start = current
        end = current + segment["duration"]

        f.write(f"{i}\n")
        f.write(
            f"{timestamp(start)} --> {timestamp(end)}\n"
        )
        f.write(segment["text"] + "\n\n")

        current = end

print("Bobby and Sunny voices generated!")
print("Hindi audio and subtitles created!")
