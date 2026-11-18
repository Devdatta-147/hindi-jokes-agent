
import os
import json
import subprocess
import math
from PIL import Image, ImageDraw

WIDTH, HEIGHT = 1080, 1920
FPS = 15
FRAMES_DIR = "frames"
SCENES_DIR = "scenes"
AUDIO_FILE = "audio/joke.mp3"
SUBTITLE_FILE = "audio/subtitles.srt"
OUTPUT_FILE = "video/first_cartoon.mp4"


def run(command):
    subprocess.run(command, check=True)


def get_audio_duration():
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            AUDIO_FILE
        ],
        capture_output=True, text=True, check=True
    )
    return float(result.stdout.strip())


def create_moving_frame(scene, frame_number, total_frames):
    image = scene.copy().convert("RGB")
    draw = ImageDraw.Draw(image)

    progress = frame_number / max(total_frames, 1)

    # Gentle camera movement
    bob = int(5 * math.sin(progress * math.pi * 8))

    # Add a small moving highlight to make the scene feel lively
    sun_x = int(900 + 12 * math.sin(progress * math.pi * 6))
    draw.ellipse(
        (sun_x - 8, 175 - 8, sun_x + 8, 175 + 8),
        fill=(255, 235, 120)
    )

    # Subtle vertical movement
    shifted = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
    shifted.paste(image, (0, bob))
    return shifted


def main():
    for folder in ["video", FRAMES_DIR]:
        os.makedirs(folder, exist_ok=True)

    if not os.path.exists(AUDIO_FILE):
        raise FileNotFoundError("Hindi audio not found: " + AUDIO_FILE)

    if not os.path.exists(SUBTITLE_FILE):
        raise FileNotFoundError("Subtitles not found: " + SUBTITLE_FILE)

    scene_paths = [
        os.path.join(SCENES_DIR, "scene1.png"),
        os.path.join(SCENES_DIR, "scene2.png"),
        os.path.join(SCENES_DIR, "scene3.png")
    ]

    for path in scene_paths:
        if not os.path.exists(path):
            raise FileNotFoundError("Cartoon scene not found: " + path)

    duration = get_audio_duration()
    total_frames = max(1, int(duration * FPS))
    frames_per_scene = max(1, total_frames // len(scene_paths))

    frame_number = 0

    for scene_index, path in enumerate(scene_paths):
        scene = Image.open(path).convert("RGB").resize((WIDTH, HEIGHT))

        if scene_index == len(scene_paths) - 1:
            scene_frames = total_frames - frame_number
        else:
            scene_frames = frames_per_scene

        for local_frame in range(scene_frames):
            frame = create_moving_frame(
                scene, local_frame, scene_frames
            )
            frame.save(
                os.path.join(FRAMES_DIR, f"frame_{frame_number:06d}.jpg"),
                quality=90
            )
            frame_number += 1

    run([
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(FRAMES_DIR, "frame_%06d.jpg"),
        "-i", AUDIO_FILE,
        "-vf",
        "subtitles=" + SUBTITLE_FILE +
        ":force_style='FontName=DejaVu Sans,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=100'",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        "-movflags", "+faststart",
        OUTPUT_FILE
    ])

    print("Cartoon video created:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
