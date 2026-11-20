
import os
import json
import glob
import math
import subprocess
from PIL import Image, ImageDraw

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

