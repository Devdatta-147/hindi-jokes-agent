
import asyncio
import json
import os
import glob
import subprocess
from datetime import datetime
import edge_tts

os.makedirs("audio/temp", exist_ok=True)
os.makedirs("audio", exist_ok=True)

# Find latest joke
files = glob.glob("generated/joke_*.json")

if not files:
    raise FileNotFoundError("No generated joke JSON found.")

latest_file = max(files, key=os.path.getmtime)

with open(latest_file, "r", encoding="utf-8") as f:
    joke = json.load(f)

dialogue = list(joke.get("dialogue", []))

if not dialogue:
    raise ValueError("No dialogue found.")

ending = joke.get("ending", "")
if ending:
    dialogue.append({
        "speaker": "Sunny",
        "text": ending
    })


async def generate_audio(text, voice, rate, pitch, filename):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch
    )
    await communicate.save(filename)


def get_duration(filename):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
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
    ms = int(round(seconds * 1000))
    hours = ms // 3600000
    ms %= 3600000
    minutes = ms // 60000
    ms %= 60000
    secs = ms // 1000
    ms %= 1000

    return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"


async def main():

    # Check available Hindi voices
    available = await edge_tts.list_voices()
    voice_names = {v["ShortName"] for v in available}

    # Prefer different male voices if available
    bobby_candidates = [
        "hi-IN-AaravNeural",
        "hi-IN-ArjunNeural",
        "hi-IN-MadhurNeural"
    ]

    sunny_candidates = [
        "hi-IN-KunalNeural",
        "hi-IN-RehaanNeural",
        "hi-IN-ArjunNeural",
        "hi-IN-MadhurNeural"
    ]

    bobby_voice = next(
        (v for v in bobby_candidates if v in voice_names),
        "hi-IN-MadhurNeural"
    )

    sunny_voice = next(
        (v for v in sunny_candidates
         if v in voice_names and v != bobby_voice),
        bobby_voice
    )

    print("Bobby voice:", bobby_voice)
    print("Sunny voice:", sunny_voice)

    timings = []
    subtitle_entries = []
    audio_files = []
    current_time = 0.0

    for index, line in enumerate(dialogue):

        speaker = line.get("speaker", "Bobby")
        text = line.get("text", "").strip()

        if not text:
            continue

        if speaker.lower() == "bobby":
            voice = bobby_voice
            rate = "+8%"
            pitch = "+8Hz"
        else:
            voice = sunny_voice
            rate = "-5%"
            pitch = "-8Hz"

        filename = f"audio/temp/line_{index}.mp3"

        print(f"Generating {speaker}: {text}")

        await generate_audio(
            text,
            voice,
            rate,
            pitch,
            filename
        )

        duration = get_duration(filename)

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

        audio_files.append(filename)
        current_time = end_time

    # Combine dialogue audio
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

    with open("audio/subtitles.srt", "w", encoding="utf-8") as f:
        f.write("\n".join(subtitle_entries))

    with open("audio/dialogue_timing.json", "w", encoding="utf-8") as f:
        json.dump(timings, f, ensure_ascii=False, indent=2)

    print("Neural Hindi voices generated successfully!")
    print("Subtitles and dialogue timings saved.")


asyncio.run(main())
