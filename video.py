
import os
import subprocess

os.makedirs("video", exist_ok=True)

images = [
    "scenes/scene1.png",
    "scenes/scene2.png",
    "scenes/scene3.png"
]

for image in images:
    if not os.path.exists(image):
        raise FileNotFoundError(f"Missing image: {image}")

# Create a vertical video from the three cartoon scenes
command = [
    "ffmpeg", "-y",
    "-loop", "1", "-t", "5", "-i", images[0],
    "-loop", "1", "-t", "5", "-i", images[1],
    "-loop", "1", "-t", "5", "-i", images[2],
    "-filter_complex",
    "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
    "pad=1080:1920:(ow-iw)/2:(oh-ih)/2[v0];"
    "[1:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
    "pad=1080:1920:(ow-iw)/2:(oh-ih)/2[v1];"
    "[2:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
    "pad=1080:1920:(ow-iw)/2:(oh-ih)/2[v2];"
    "[v0][v1][v2]concat=n=3:v=1:a=0[outv]",
    "-map", "[outv]",
    "-r", "30",
    "-pix_fmt", "yuv420p",
    "video/first_cartoon.mp4"
]

subprocess.run(command, check=True)
print("Video created successfully!")
