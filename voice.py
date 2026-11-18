
import json
import os
import glob
import subprocess
from datetime import datetime
from gtts import gTTS

os.makedirs("audio/temp", exist_ok=True)
os.makedirs("audio", exist_ok=True)

# Find the latest generated joke
files = glob.glob("generated/joke_*.json")

if not files:
    raise FileNotFoundError("No generated joke JSON found.")

latest_file = max(files, key=os.path.getmtime)

with open(latest_file, "r", encoding="utf-8") as f:
    joke = json.load(f)

dialogue = joke.get("dialogue", [])

if not dialogue:
    raise ValueError("No dialogue lines found in joke JSON.")

# Add the ending as Sunny's final dialogue
ending = joke.get("ending", "")
if ending:
    dialogue.append({
        "speaker": "Sunny",
        "text": ending
    })


def get_duration(filename):
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            filename
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return float(result.stdout.strip())


def format_srt_time(seconds):
    milliseconds = int(round(seconds * 1000))
    hours = milliseconds // 3600000
    milliseconds %= 3600000
    minutes = milliseconds // 60000
    milliseconds %= 60000
    secs = milliseconds // 1000
    milliseconds %= 1000

    return (
        f"{hours:02}:{minutes:02}:{secs:02},"
        f"{milliseconds:03}"
    )


timings = []
subtitle_entries = []
current_time = 0.0
audio_files = []

for index, line in enumerate(dialogue):
    speaker = line.get("speaker", "Bobby")
    text = line.get("text", "").strip()

    if not text:
        continue

    print(f"Generating voice: {speaker}")

    raw_file = f"audio/temp/raw_{index}.mp3"
    processed_file = f"audio/temp/processed_{index}.mp3"

    # Generate Hindi speech
    tts = gTTS(text=text, lang="hi")
    tts.save(raw_file)

    # Slightly different pitch for each character
    pitch = 0.94 if speaker.lower() == "bobby" else 1.07

    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", raw_file,
            "-af",
            f"asetrate=44100*{pitch},aresample=44100,"
            f"atempo={1/pitch}",
            "-codec:a", "libmp3lame",
            "-q:a", "4",
            processed_file
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    duration = get_duration(processed_file)

    start_time = current_time
    end_time = current_time + duration

    timings.append({
        "speaker": speaker,
        "text": text,
        "start": round(start_time, 3),
        "end": round(end_time, 3)
    })

    subtitle_entries.append(
        f"{len(subtitle_entries) + 1}\n"
        f"{format_srt_time(start_time)} --> "
        f"{format_srt_time(end_time)}\n"
        f"{speaker}: {text}\n"
    )

    audio_files.append(processed_file)
    current_time = end_time

# Combine all dialogue audio files
concat_file = "audio/temp/concat.txt"

with open(concat_file, "w", encoding="utf-8") as f:
    for filename in audio_files:
        absolute_path = os.path.abspath(filename)
        f.write(f"file '{absolute_path}'\n")

subprocess.run(
    [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c:a", "libmp3lame",
        "-q:a", "4",
        "audio/joke.mp3"
    ],
    check=True
)

# Save subtitles
with open("audio/subtitles.srt", "w", encoding="utf-8") as f:
    f.write("\n".join(subtitle_entries))

# Save dialogue timing for character animation
with open("audio/dialogue_timing.json", "w", encoding="utf-8") as f:
    json.dump(timings, f, ensure_ascii=False, indent=2)

print("Hindi voice generated successfully!")
print("Subtitles saved.")
print("Dialogue animation timings saved.")
