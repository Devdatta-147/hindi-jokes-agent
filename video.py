
import os
import json
import glob
import math
import subprocess
from PIL import Image

WIDTH = 1080
HEIGHT = 1920
FPS = 15

os.makedirs("video/frames", exist_ok=True)
os.makedirs("video", exist_ok=True)


def run_command(command):
    subprocess.run(command, check=True)


def get_audio_duration():
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            "audio/joke.mp3"
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return float(result.stdout.strip())


def load_character(name):
    folder = f"characters/{name}"

    required = [
        "body.png",
        "head.png",
        "hair.png",
        "eyes_open.png",
        "eyes_closed.png",
        "mouth_closed.png",
        "mouth_open.png",
        "mouth_smile.png",
        "mouth_surprise.png",
        "arms_down.png",
        "arms_up.png"
    ]

    layers = {}

    for filename in required:
        path = os.path.join(folder, filename)

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Missing character layer: {path}"
            )

        layers[filename.replace(".png", "")] = (
            Image.open(path).convert("RGBA")
        )

    return layers


characters = {
    "Bobby": load_character("bobby"),
    "Sunny": load_character("sunny")
}

backgrounds = []

for number in range(1, 4):
    path = f"scenes/scene{number}.png"

    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing background: {path}")

    backgrounds.append(
        Image.open(path).convert("RGBA").resize((WIDTH, HEIGHT))
    )

with open("audio/dialogue_timing.json", "r", encoding="utf-8") as f:
    dialogue = json.load(f)

if not dialogue:
    raise ValueError("Dialogue timing file is empty.")

duration = get_audio_duration()
total_frames = math.ceil(duration * FPS)

# Resize character layers while keeping them transparent
CHARACTER_WIDTH = 430
CHARACTER_HEIGHT = 680

scaled_characters = {}

for name, layers in characters.items():
    scaled_characters[name] = {}

    for layer_name, layer in layers.items():
        scaled_characters[name][layer_name] = layer.resize(
            (CHARACTER_WIDTH, CHARACTER_HEIGHT),
            Image.Resampling.LANCZOS
        )

# Character positions on the screen
positions = {
    "Bobby": (85, 850),
    "Sunny": (565, 850)
}


def active_speaker(time):
    for line in dialogue:
        if line["start"] <= time <= line["end"]:
            return line["speaker"]

    return None


def draw_character(scene, name, time, speaking):
    layers = scaled_characters[name]

    # Gentle body movement
    bob = int(5 * math.sin(time * 3 + (0 if name == "Bobby" else 1)))

    x, y = positions[name]
    y += bob

    # Blink briefly at regular intervals
    blink = (time % 3.7) < 0.14

    if speaking:
        # Mouth opens and closes while this character speaks
        mouth_is_open = (int(time * 7) % 2 == 0)
        mouth = "mouth_open" if mouth_is_open else "mouth_closed"
    else:
        mouth = "mouth_smile"

    # Occasional hand gesture while speaking
    gesture = speaking and (int(time * 1.5) % 3 == 0)
    arms = "arms_up" if gesture else "arms_down"

    # Compose transparent layers in order
    layer_order = [
        "body",
        arms,
        "head",
        "hair",
        "eyes_closed" if blink else "eyes_open",
        mouth
    ]

    character_image = Image.new(
        "RGBA",
        (CHARACTER_WIDTH, CHARACTER_HEIGHT),
        (0, 0, 0, 0)
    )

    for layer_name in layer_order:
        character_image = Image.alpha_composite(
            character_image,
            layers[layer_name]
        )

    scene.alpha_composite(character_image, (x, y))


print("Creating animated cartoon frames...")

for frame_number in range(total_frames):
    current_time = frame_number / FPS

    # Change background across the video
    scene_index = min(
        int((current_time / duration) * 3),
        2
    )

    scene = backgrounds[scene_index].copy()

    speaker = active_speaker(current_time)

    draw_character(
        scene,
        "Bobby",
        current_time,
        speaker == "Bobby"
    )

    draw_character(
        scene,
        "Sunny",
        current_time,
        speaker == "Sunny"
    )

    frame_path = f"video/frames/frame_{frame_number:05d}.jpg"

    scene.convert("RGB").save(
        frame_path,
        quality=90
    )

print("Frames created. Building final video...")

# Create silent video from frames
run_command([
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", "video/frames/frame_%05d.jpg",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "ultrafast",
    "video/silent.mp4"
])

# Add Hindi audio and subtitles
run_command([
    "ffmpeg", "-y",
    "-i", "video/silent.mp4",
    "-i", "audio/joke.mp3",
    "-vf",
    "subtitles=audio/subtitles.srt:"
    "force_style='FontSize=18,Outline=2,Shadow=1,"
    "Alignment=2,MarginV=100'",
    "-map", "0:v:0",
    "-map", "1:a:0",
    "-c:v", "libx264",
    "-preset", "ultrafast",
    "-c:a", "aac",
    "-b:a", "128k",
    "-shortest",
    "-pix_fmt", "yuv420p",
    "video/first_cartoon.mp4"
])

print("SUCCESS! Animated Hindi cartoon video created.")
