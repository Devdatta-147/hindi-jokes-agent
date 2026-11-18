
import asyncio
import json
import os
import glob
import subprocess
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

    # Get available Hindi voices
    available = await edge_tts.list_voices()
    voice_names = {v["ShortName"] for v in available}

    # Bobby voice candidates
    bobby_candidates = [
        "hi-IN-AaravNeural",
        "hi-IN-ArjunNeural",
        "hi-IN-MadhurNeural"
    ]

    # Sunny voice candidates
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

    # Generate each dialogue line
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

    # Save subtitles
    with open("audio/subtitles.srt", "w", encoding="utf-8") as f:
        f.write("\n".join(subtitle_entries))

    # Save original line-level timings
    with open("audio/dialogue_timing.json", "w", encoding="utf-8") as f:
        json.dump(timings, f, ensure_ascii=False, indent=2)

    # ---------------------------------------------
    # WHISPERX WORD-LEVEL ALIGNMENT
    # ---------------------------------------------
    print("Starting WhisperX Hindi word alignment...")

    word_timings = []

    try:
        import whisperx

        device = "cpu"

        # Load Hindi alignment model
        align_model, metadata = whisperx.load_align_model(
            language_code="hi",
            device=device
        )

        # Load the combined audio
        audio = whisperx.load_audio("audio/joke.mp3")

        # Prepare dialogue segments for alignment
        alignment_segments = [
            {
                "start": item["start"],
                "end": item["end"],
                "text": item["text"]
            }
            for item in timings
        ]

        # Align spoken Hindi words
        aligned_result = whisperx.align(
            alignment_segments,
            align_model,
            metadata,
            audio,
            device,
            return_char_alignments=False
        )

        # Extract word timestamps
        for segment in aligned_result.get("segments", []):
            speaker = None

            # Identify the speaker using the original line timings
            midpoint = (
                segment.get("start", 0) +
                segment.get("end", 0)
            ) / 2

            for line in timings:
                if line["start"] <= midpoint <= line["end"]:
                    speaker = line["speaker"]
                    break

            for word in segment.get("words", []):
                if "start" not in word or "end" not in word:
                    continue

                word_timings.append({
                    "speaker": speaker,
                    "word": word.get("word", "").strip(),
                    "start": round(word["start"], 3),
                    "end": round(word["end"], 3)
                })

        # Save word-level timings
        with open("audio/word_timing.json", "w", encoding="utf-8") as f:
            json.dump(
                word_timings,
                f,
                ensure_ascii=False,
                indent=2
            )

        print(
            f"WhisperX alignment successful: "
            f"{len(word_timings)} words aligned."
        )

    except Exception as e:

        print("WARNING: WhisperX alignment failed.")
        print("Reason:", str(e))

        # Save an empty word timing file so the workflow can continue
        with open("audio/word_timing.json", "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

        print("Using existing line-level timings as fallback.")

    print("Neural Hindi voices generated successfully!")
    print("Subtitles and dialogue timings saved.")
    print("Word-level timing file: audio/word_timing.json")


asyncio.run(main())
