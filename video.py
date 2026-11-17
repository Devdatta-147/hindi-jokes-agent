
import os
import subprocess

os.makedirs("video", exist_ok=True)

audio = "audio/joke.mp3"
subtitles = "audio/subtitles.srt"

images = [
    "scenes/scene1.png",
    "scenes/scene2.png",
    "scenes/scene3.png"
]

for path in images + [audio, subtitles]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")

duration = float(subprocess.check_output([
    "ffprobe", "-v", "error",
    "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1",
    audio
]).decode().strip())

segment = duration / 3

command = ["ffmpeg", "-y"]

for i, image in enumerate(images):
    length = segment if i < 2 else duration - 2 * segment
    command += ["-loop", "1", "-t", str(length), "-i", image]

command += ["-i", audio]

filter_complex = (
    "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
    "pad=1080:1920:(ow-iw)/2:(oh-ih)/2[v0];"
    "[1:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
    "pad=1080:1920:(ow-iw)/2:(oh-ih)/2[v1];"
    "[2:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
    "pad=1080:1920:(ow-iw)/2:(oh-ih)/2[v2];"
    "[v0][v1][v2]concat=n=3:v=1:a=0,"
    "subtitles=audio/subtitles.srt:"
    "force_style='FontName=Noto Sans Devanagari,FontSize=28,"
    "Alignment=2,MarginV=100'[outv]"
)

command += [
    "-filter_complex", filter_complex,
    "-map", "[outv]",
    "-map", "3:a",
    "-r", "30",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-shortest",
    "video/first_cartoon.mp4"
]

subprocess.run(command, check=True)
print("Hindi cartoon video with voice and subtitles created!")
