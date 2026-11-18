
from PIL import Image, ImageDraw
import os

WIDTH = 1080
HEIGHT = 1920

os.makedirs("scenes", exist_ok=True)


def create_scene(scene_number):
    image = Image.new("RGB", (WIDTH, HEIGHT), "#FFF3D6")
    draw = ImageDraw.Draw(image)

    # Background wall
    draw.rectangle(
        (0, 0, WIDTH, 1250),
        fill="#FFF0D2"
    )

    # Floor
    draw.rectangle(
        (0, 1250, WIDTH, HEIGHT),
        fill="#D9B58B"
    )

    # Window
    draw.rounded_rectangle(
        (80, 180, 420, 620),
        radius=25,
        fill="#B9E3F5",
        outline="#FFFFFF",
        width=18
    )

    draw.line(
        (250, 190, 250, 610),
        fill="#FFFFFF",
        width=12
    )
    draw.line(
        (90, 400, 410, 400),
        fill="#FFFFFF",
        width=12
    )

    # Wall decoration changes by scene
    if scene_number == 1:
        draw.rounded_rectangle(
            (650, 220, 980, 430),
            radius=30,
            fill="#F5C76E"
        )
        draw.text(
            (715, 290),
            "WELCOME!",
            fill="#543A27",
            stroke_width=1
        )

    elif scene_number == 2:
        draw.ellipse(
            (720, 220, 930, 430),
            fill="#F6D477"
        )
        draw.ellipse(
            (775, 275, 825, 325),
            fill="#FFFFFF"
        )
        draw.ellipse(
            (850, 275, 900, 325),
            fill="#FFFFFF"
        )

    else:
        draw.rounded_rectangle(
            (650, 220, 980, 430),
            radius=30,
            fill="#B8DDBB"
        )
        draw.ellipse(
            (760, 270, 870, 380),
            fill="#F4A261"
        )

    # Rug
    draw.ellipse(
        (130, 1450, 950, 1790),
        fill="#B85C50"
    )

    # Bottom caption area
    draw.rectangle(
        (0, 1810, WIDTH, HEIGHT),
        fill="#293746"
    )

    return image


for number in range(1, 4):
    scene = create_scene(number)
    scene.save(f"scenes/scene{number}.png")

print("Three clean cartoon backgrounds created successfully!")
