
from PIL import Image, ImageDraw
import os

WIDTH, HEIGHT = 1080, 1920

os.makedirs("scenes", exist_ok=True)

def draw_character(draw, x, y, name, shirt, mood):
    # Body
    draw.rounded_rectangle(
        (x-115, y+190, x+115, y+550),
        radius=65, fill=shirt
    )

    # Head
    draw.ellipse(
        (x-130, y-130, x+130, y+180),
        fill="#F2C49B", outline="#333333", width=8
    )

    # Hair
    draw.arc(
        (x-130, y-160, x+130, y+70),
        180, 360, fill="#222222", width=30
    )

    # Eyes
    draw.ellipse((x-70, y-35, x-35, y+5), fill="black")
    draw.ellipse((x+35, y-35, x+70, y+5), fill="black")

    # Mouth
    if mood == "surprised":
        draw.ellipse((x-25, y+65, x+25, y+125), fill="#7A2222")
    elif mood == "happy":
        draw.arc((x-55, y+35, x+55, y+125),
                 0, 180, fill="#7A2222", width=9)
    else:
        draw.line((x-40, y+90, x+40, y+90),
                  fill="#7A2222", width=8)

    # Character name
    draw.text((x-100, y+580), name, fill="black")

def make_scene(number, title, mood1, mood2):
    img = Image.new("RGB", (WIDTH, HEIGHT), "#B9E8FF")
    draw = ImageDraw.Draw(img)

    # Background
    draw.rectangle((0, 1300, WIDTH, HEIGHT), fill="#8ED58A")
    draw.ellipse((780, 100, 1000, 320), fill="#FFD95C")

    # Scene title
    draw.text((70, 100), title, fill="#222222")

    # Characters
    draw_character(draw, 330, 650, "RAJU", "#F4B942", mood1)
    draw_character(draw, 760, 650, "PAPPU", "#4D91D9", mood2)

    img.save(f"scenes/scene{number}.png")

make_scene(1, "THE FUNNY FRIENDS", "happy", "surprised")
make_scene(2, "THE BIG QUESTION", "surprised", "happy")
make_scene(3, "THE FUNNY ENDING", "happy", "happy")

print("3 CARTOON SCENES CREATED!")
