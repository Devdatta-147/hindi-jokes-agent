
import os
import json
import glob
import math
import subprocess
from PIL import Image

WIDTH = 1080
HEIGHT = 1920
FPS = 15

CHARACTER_WIDTH = 430
CHARACTER_HEIGHT = 680

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
        "head_normal.png",
        "hair.png",
        "eyes_normal.png",
        "eyes_closed.png",
        "eyes_surprised.png",
        "eyes_narrow.png",
        "eyes_angry.png",
        "eyes_worried.png",
        "mouth_closed.png",
        "mouth_open.png",
        "mouth_smile.png",
        "mouth_surprise.png",
        "mouth_laugh.png",
        "arms_down.png",
        "arms_up.png"
    ]

    layers = {}

    for filename in required:
        path = os.path.join(folder, filename)

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Missing character layer: {path}. "
                "Please run characters.py first."
            )

        layers[filename.replace(".png", "")] = (
            Image.open(path).convert("RGBA")
        )

    return layers


characters = {
    "Bobby": load_character("bobby"),
    "Sunny": load_character("sunny")
}


# Load backgrounds
backgrounds = []

for number in range(1, 4):
    path = f"scenes/scene{number}.png"

    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing background: {path}")

    backgrounds.append(
        Image.open(path).convert("RGBA").resize(
            (WIDTH, HEIGHT)
        )
    )


# Load dialogue timing
with open(
    "audio/dialogue_timing.json",
    "r",
    encoding="utf-8"
) as f:
    dialogue = json.load(f)

if not dialogue:
    raise ValueError("Dialogue timing file is empty.")


duration = get_audio_duration()

if duration <= 0:
    raise ValueError("Audio duration is invalid.")

total_frames = math.ceil(duration * FPS)


# Resize character layers
scaled_characters = {}

for name, layers in characters.items():
    scaled_characters[name] = {}

    for layer_name, layer in layers.items():
        scaled_characters[name][layer_name] = layer.resize(
            (CHARACTER_WIDTH, CHARACTER_HEIGHT),
            Image.Resampling.LANCZOS
        )


# Character positions
positions = {
    "Bobby": (85, 850),
    "Sunny": (565, 850)
}


def active_line(time):
    for line in dialogue:
        if line["start"] <= time < line["end"]:
            return line

    return None


def draw_character(scene, name, time, speaker):
    layers = scaled_characters[name]

    speaking = speaker == name

    # Gentle body movement
    phase = 0 if name == "Bobby" else 1.5
    bob = int(6 * math.sin(time * 3 + phase))

    x, y = positions[name]
    y += bob

    # Gentle head tilt
    tilt_phase = (time + phase) % 7

    if tilt_phase < 2:
        head_angle = -3
    elif tilt_phase < 4:
        head_angle = 3
    else:
        head_angle = 0

    head = layers["head_normal"].rotate(
        head_angle,
        resample=Image.Resampling.BICUBIC,
        center=(215, 170)
    )

    hair = layers["hair"].rotate(
        head_angle,
        resample=Image.Resampling.BICUBIC,
        center=(215, 170)
    )

    # Eye blinking
    blink = (time % 3.7) < 0.14

    # Short surprised reaction when the other character starts speaking
    reaction = False

    if speaker is not None and speaker != name:
        for line in dialogue:
            if line["speaker"] == speaker:
                if (
                    line["start"] <= time
                    and time - line["start"] < 0.45
                ):
                    reaction = True
                    break

    if blink:
        eyes = "eyes_closed"
    elif reaction:
        eyes = "eyes_surprised"
    elif speaking and (time % 8) > 6.5:
        eyes = "eyes_surprised"
    elif speaking and (time % 11) > 8.5:
        eyes = "eyes_narrow"
    else:
        eyes = "eyes_normal"

    # Mouth movement
    if reaction:
        mouth = "mouth_surprise"

    elif speaking:
        mouth_phase = int(time * 7) % 2 == 0

        if (time % 9) > 7.5:
            mouth = "mouth_laugh"
        else:
            mouth = (
                "mouth_open"
                if mouth_phase
                else "mouth_closed"
            )
    else:
        mouth = "mouth_smile"

    # Hand gestures
    gesture = (
        speaking
        and ((time + phase) % 4.5 < 1.0)
    )

    arms = "arms_up" if gesture else "arms_down"

    # Compose character layers
    layer_order = [
        layers["body"],
        layers[arms],
        head,
        hair,
        layers[eyes],
        layers[mouth]
    ]

    character_image = Image.new(
        "RGBA",
        (CHARACTER_WIDTH, CHARACTER_HEIGHT),
        (0, 0, 0, 0)
    )

    for layer in layer_order:
        character_image = Image.alpha_composite(
            character_image,
            layer
        )

    scene.alpha_composite(character_image, (x, y))


def apply_camera(scene, time, line):
    if line is None:
        return scene

    speaker = line.get("speaker")

    if speaker not in positions:
        return scene

    elapsed = max(0, time - line["start"])
    line_duration = max(
        0.1,
        line["end"] - line["start"]
    )

    progress = min(1.0, elapsed / line_duration)

    # Briefly show the listener's reaction
    if elapsed < 0.35:
        focus = "Sunny" if speaker == "Bobby" else "Bobby"
        zoom = 1.10

    else:
        focus = speaker

        # Gradual zoom towards the punchline
        zoom = 1.0 + 0.10 * math.sin(
            math.pi * progress
        )

    center_x = (
        positions[focus][0] + CHARACTER_WIDTH // 2
    )

    center_y = (
        positions[focus][1] + CHARACTER_HEIGHT // 2
    )

    crop_width = int(WIDTH / zoom)
    crop_height = int(HEIGHT / zoom)

    left = max(
        0,
        min(
            WIDTH - crop_width,
            center_x - crop_width // 2
        )
    )

    top = max(
        0,
        min(
            HEIGHT - crop_height,
            center_y - crop_height // 2
        )
    )

    cropped = scene.crop((
        left,
        top,
        left + crop_width,
        top + crop_height
    ))

    return cropped.resize(
        (WIDTH, HEIGHT),
        Image.Resampling.LANCZOS
    )


print("Preparing cartoon video...")

# Remove old frames
for old_frame in glob.glob("video/frames/frame_*.jpg"):
    os.remove(old_frame)


print("Creating animated cartoon frames...")

for frame_number in range(total_frames):

    current_time = frame_number / FPS

    # Three background scenes
    scene_index = min(
        int((current_time / duration) * 3),
        2
    )

    scene = backgrounds[scene_index].copy()

    line = active_line(current_time)

    speaker = (
        line.get("speaker")
        if line is not None
        else None
    )

    # Draw Bobby and Sunny
    draw_character(
        scene,
        "Bobby",
        current_time,
        speaker
    )

    draw_character(
        scene,
        "Sunny",
        current_time,
        speaker
    )

    # Apply camera movement
    scene = apply_camera(
        scene,
        current_time,
        line
    )

    frame_path = (
        f"video/frames/frame_{frame_number:05d}.jpg"
    )

    scene.convert("RGB").save(
        frame_path,
        quality=90
    )

print("Frames created. Building final video...")


# Create silent video
run_command([
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", "video/frames/frame_%05d.jpg",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "ultrafast",
    "video/silent.mp4"
])


# Add Hindi voice and subtitles
run_command([
    "ffmpeg", "-y",
    "-i", "video/silent.mp4",
    "-i", "audio/joke.mp3",
    "-vf",
    "subtitles=audio/subtitles.srt:"
    "force_style='FontSize=12,Outline=2,Shadow=1,"
    "Alignment=2,MarginV=35'",
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
