
import os
import json
import glob
import math
import subprocess
from PIL import Image, ImageDraw

WIDTH = 1080
HEIGHT = 1920
FPS = 24

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

    # Load additional poses when available
    optional_poses = [
        "arms_point.png",
        "arms_hips.png",
        "arms_laugh.png",
        "arms_folded.png",
        "arms_one_hand.png",
        "arms_facepalm.png"
    ]

    for filename in optional_poses:
        path = os.path.join(folder, filename)

        if os.path.exists(path):
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


# Load WhisperX word timings
word_timings = []

word_file = "audio/word_timing.json"

if os.path.exists(word_file):
    try:
        with open(word_file, "r", encoding="utf-8") as f:
            word_timings = json.load(f)

        if not isinstance(word_timings, list):
            word_timings = []

    except (json.JSONDecodeError, OSError) as e:
        print("Could not read word timings:", e)
        word_timings = []

if word_timings:
    print(f"Loaded {len(word_timings)} WhisperX word timings.")
else:
    print("No word timings found. Using line-level animation fallback.")


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


def active_word(time, character_name):
    for word in word_timings:
        if word.get("speaker") != character_name:
            continue

        start = word.get("start")
        end = word.get("end")

        if start is None or end is None:
            continue

        if start <= time < end:
            return word

    return None


def draw_character(scene, name, time, speaker):
    layers = scaled_characters[name]

    speaking = speaker == name

    # Dialogue timing drives the speaker's gestures and the listener's reactions.
    line = active_line(time)
    elapsed = 0.0
    progress = 0.0
    if line is not None:
        elapsed = max(0.0, time - line["start"])
        line_duration = max(0.1, line["end"] - line["start"])
        progress = min(1.0, elapsed / line_duration)

    # Different movement personalities, with a subtle breathing/sway motion.
    phase = 0.0 if name == "Bobby" else 1.5
    bob_amount = 7 if name == "Bobby" else 5
    idle_bob = bob_amount * math.sin(time * 3 + phase)
    body_sway = 2.0 * math.sin(time * 1.7 + phase)

    # The listener gives a small, timed nod; the speaker leans into the punchline.
    if line is not None and not speaking:
        reaction_nod = 5.0 * math.sin(elapsed * 8.0) * math.exp(-elapsed * 1.2)
    else:
        reaction_nod = 0.0

    punchline_lean = 0.0
    if speaking and progress > 0.72:
        punchline_lean = 3.0 * math.sin((progress - 0.72) * math.pi / 0.28)

    x, y = positions[name]
    y += int(idle_bob + reaction_nod - punchline_lean)
    x += int(body_sway)

    # Gentle idle head movement, plus a visible nod from the listening character.
    tilt_phase = (time + phase) % 7
    if tilt_phase < 2:
        head_angle = -3
    elif tilt_phase < 4:
        head_angle = 3
    else:
        head_angle = 0

    if line is not None and not speaking:
        head_angle += 4.0 * math.sin(elapsed * 7.0) * math.exp(-elapsed * 1.0)
    elif speaking and progress > 0.72:
        head_angle -= 3.0 * math.sin((progress - 0.72) * math.pi / 0.28)

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

    # Find this character's active word
    word = active_word(time, name) if word_timings else None

    if word_timings:
        word_speaking = word is not None
    else:
        word_speaking = speaking

    # Natural blinking
    blink = ((time + phase) % 3.8) < 0.13

    # Listener reaction
    reaction = (
        not speaking
        and line is not None
        and elapsed < 0.55
    )

    eyes = "eyes_normal"
    mouth = "mouth_closed"

    if reaction:
        if name == "Bobby":
            eyes = "eyes_surprised"
        else:
            eyes = "eyes_narrow"

        mouth = "mouth_closed"

    elif speaking and word_speaking:

        # Word-timed mouth movement
        if word_timings and word is not None:
            word_start = word["start"]
            word_end = word["end"]

            word_duration = max(
                0.05,
                word_end - word_start
            )

            word_phase = (
                time - word_start
            ) / word_duration

            if name == "Bobby":
                mouth_speed = 10
                open_ratio = 0.58
            else:
                mouth_speed = 7
                open_ratio = 0.48

            cycle = (word_phase * mouth_speed) % 1.0

            if cycle < open_ratio:
                mouth = "mouth_open"
            else:
                mouth = "mouth_closed"

        else:
            # Fallback if word timings are unavailable
            if name == "Bobby":
                mouth = (
                    "mouth_open"
                    if int(time * 8) % 2 == 0
                    else "mouth_closed"
                )
            else:
                mouth = (
                    "mouth_open"
                    if int(time * 6) % 2 == 0
                    else "mouth_closed"
                )

        # Character expressions
        if name == "Bobby":
            if 0.25 < progress < 0.42:
                eyes = "eyes_surprised"
            elif 0.55 < progress < 0.72:
                eyes = "eyes_narrow"
        else:
            if 0.20 < progress < 0.68:
                eyes = "eyes_narrow"
            elif 0.72 < progress < 0.88:
                eyes = "eyes_worried"

    else:
        # Listening expressions
        if name == "Sunny":
            eyes = "eyes_narrow"
        else:
            eyes = "eyes_normal"

        mouth = "mouth_smile"

    # Blinking overrides eye expression
    if blink:
        eyes = "eyes_closed"

    # --------------------------------
    # NEW: DYNAMIC ARM POSE SELECTION
    # --------------------------------

    arm_pose = "down"

    if speaking:

        if name == "Bobby":
            # Bobby points while explaining
            if 0.18 < progress < 0.50:
                arm_pose = "point"

            # Bobby raises both arms near the punchline
            elif progress > 0.78:
                arm_pose = "laugh"

            # Occasional energetic gesture
            elif (time + phase) % 3.5 < 1.0:
                arm_pose = "up"

        else:
            # Sunny uses one hand while explaining
            if 0.18 < progress < 0.72:
                arm_pose = "one_hand"

            # Occasional raised-arm gesture
            elif (time + phase) % 5.0 < 0.7:
                arm_pose = "up"

    else:

        if name == "Sunny" and speaker == "Bobby":
            # Sunny facepalms near Bobby's punchline
            if progress > 0.72:
                arm_pose = "facepalm"
            else:
                arm_pose = "folded"

        elif name == "Bobby" and speaker == "Sunny":
            # Bobby sometimes listens with hands on hips
            if progress > 0.55:
                arm_pose = "hips"

    # Use the requested pose if available
    requested_layer = f"arms_{arm_pose}"

    if requested_layer in layers:
        arms = layers[requested_layer]
    else:
        # Safe fallback
        fallback = "arms_up" if arm_pose != "down" else "arms_down"
        arms = layers[fallback]

    # Compose character
    layer_order = [
        layers["body"],
        arms,
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



def draw_animated_props(scene, time, speaker):
    """
    Draw simple animated props directly with Pillow.
    No external PNG assets are required.
    """
    # --- Bobby's tea cup: gently lifts while Bobby is speaking ---
    cup_layer = Image.new("RGBA", (180, 150), (0, 0, 0, 0))
    cup_draw = ImageDraw.Draw(cup_layer)

    cup_lift = 10 if speaker == "Bobby" and math.sin(time * 5) > 0 else 0
    cup_draw.ellipse((28, 112, 145, 137), fill=(80, 48, 31, 90))
    cup_draw.rounded_rectangle(
        (42, 55, 125, 120), radius=12,
        fill=(248, 244, 232, 255), outline=(75, 55, 43, 255), width=4
    )
    cup_draw.arc((108, 67, 158, 112), start=265, end=95,
                 fill=(75, 55, 43, 255), width=7)
    cup_draw.ellipse((49, 49, 119, 68),
                     fill=(111, 65, 39, 255), outline=(75, 55, 43, 255), width=3)
    cup_draw.arc((61, 12, 85, 48), start=210, end=330,
                 fill=(220, 220, 220, 220), width=3)
    cup_draw.arc((86, 4, 111, 43), start=210, end=330,
                 fill=(220, 220, 220, 220), width=3)

    cup_angle = -5 if speaker == "Bobby" else 0
    cup_layer = cup_layer.rotate(cup_angle, resample=Image.Resampling.BICUBIC,
                                 expand=False)
    scene.alpha_composite(cup_layer, (345, 1260 - cup_lift))

    # --- Sunny's newspaper: small rocking/page movement ---
    paper_layer = Image.new("RGBA", (260, 190), (0, 0, 0, 0))
    paper_draw = ImageDraw.Draw(paper_layer)
    paper_draw.rounded_rectangle(
        (10, 10, 250, 180), radius=5,
        fill=(247, 242, 222, 255), outline=(55, 55, 50, 255), width=4
    )
    paper_draw.line((130, 18, 130, 171), fill=(130, 120, 100, 255), width=3)
    paper_draw.rectangle((24, 23, 116, 48), fill=(55, 55, 50, 255))
    paper_draw.rectangle((145, 23, 235, 43), fill=(90, 85, 75, 255))
    for y_line in (62, 78, 94, 110, 126, 142, 158):
        paper_draw.line((25, y_line, 116, y_line),
                        fill=(125, 119, 105, 255), width=3)
        paper_draw.line((145, y_line, 235, y_line),
                        fill=(125, 119, 105, 255), width=3)

    page_shift = int(4 * math.sin(time * 2.2))
    paper_angle = 3 * math.sin(time * 1.8)
    paper_layer = paper_layer.rotate(paper_angle, resample=Image.Resampling.BICUBIC,
                                     expand=False)
    scene.alpha_composite(paper_layer, (625, 1230 + page_shift))

    # --- Mobile notification: slides in periodically and vibrates briefly ---
    cycle = time % 9.0
    if 1.0 <= cycle <= 4.0:
        # Smoothly slide the notification card into view, then hold it.
        slide = min(1.0, (cycle - 1.0) / 0.45)
        x = int(1080 + 20 - 360 * slide)
        vibration = int(3 * math.sin(time * 38)) if cycle < 1.8 else 0

        phone_layer = Image.new("RGBA", (350, 145), (0, 0, 0, 0))
        phone_draw = ImageDraw.Draw(phone_layer)
        phone_draw.rounded_rectangle(
            (4, 4, 344, 139), radius=22,
            fill=(30, 34, 43, 238), outline=(235, 235, 235, 220), width=3
        )
        phone_draw.ellipse((20, 23, 62, 65), fill=(80, 170, 125, 255))
        phone_draw.text((31, 31), "!", fill=(255, 255, 255, 255))
        phone_draw.text((77, 19), "NEW MESSAGE",
                        fill=(190, 220, 205, 255))
        phone_draw.text((77, 49), "Bobby: Ha ha!",
                        fill=(255, 255, 255, 255))
        phone_draw.text((77, 83), "Just now",
                        fill=(205, 205, 205, 255))
        scene.alpha_composite(phone_layer, (x + vibration, 300))



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

    # Briefly show listener reaction
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

    # Draw Bobby's tea cup, Sunny's newspaper, and the mobile notification.
    draw_animated_props(scene, current_time, speaker)

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
