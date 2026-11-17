
from PIL import Image, ImageDraw
import os
import math

os.makedirs("scenes", exist_ok=True)

W, H = 1080, 1920

def draw_character(draw, x, y, name, shirt, hair, expression="smile", hand="down"):
    # Body
    draw.rounded_rectangle(
        (x-105, y+210, x+105, y+520),
        radius=55, fill=shirt
    )

    # Neck
    draw.rectangle((x-35, y+145, x+35, y+250), fill="#D99A70")

    # Head
    draw.ellipse((x-120, y-90, x+120, y+190), fill="#E8B18A")

    # Hair
    draw.pieslice((x-125, y-115, x+125, y+115),
                  180, 360, fill=hair)
    draw.ellipse((x-120, y-80, x-35, y+5), fill=hair)
    draw.ellipse((x+35, y-80, x+120, y+5), fill=hair)

    # Eyes
    draw.ellipse((x-65, y+20, x-30, y+58), fill="white")
    draw.ellipse((x+30, y+20, x+65, y+58), fill="white")
    draw.ellipse((x-53, y+30, x-35, y+50), fill="black")
    draw.ellipse((x+42, y+30, x+60, y+50), fill="black")

    # Eyebrows
    draw.line((x-72, y+5, x-28, y-2), fill=hair, width=9)
    draw.line((x+28, y-2, x+72, y+5), fill=hair, width=9)

    # Nose
    draw.ellipse((x-10, y+65, x+10, y+85), fill="#C98262")

    # Mouth
    if expression == "laugh":
        draw.arc((x-48, y+75, x+48, y+150),
                 0, 180, fill="#7B2525", width=12)
    elif expression == "surprise":
        draw.ellipse((x-20, y+100, x+20, y+145),
                     fill="#7B2525")
    else:
        draw.arc((x-45, y+75, x+45, y+140),
                 0, 180, fill="#7B2525", width=10)

    # Arms
    if hand == "up":
        draw.line((x-95, y+260, x-210, y+120),
                  fill="#E8B18A", width=45)
        draw.ellipse((x-235, y+90, x-185, y+145),
                     fill="#E8B18A")
        draw.line((x+95, y+260, x+210, y+390),
                  fill="#E8B18A", width=45)
    else:
        draw.line((x-95, y+260, x-165, y+430),
                  fill="#E8B18A", width=45)
        draw.line((x+95, y+260, x+165, y+430),
                  fill="#E8B18A", width=45)

    # Character name
    draw.text((x-85, y+545), name, fill="#222222")

def make_scene(number, title, bobby_expression, sunny_expression,
               bobby_hand="down", sunny_hand="down"):

    img = Image.new("RGB", (W, H), "#FFF2D9")
    d = ImageDraw.Draw(img)

    # Background
    d.rectangle((0, 1450, W, H), fill="#D9EAD3")
    d.ellipse((80, 120, 300, 340), fill="#FFD966")
    d.rounded_rectangle((60, 420, 1020, 650),
                        radius=45, fill="white")

    d.text((100, 490), title, fill="#222222")

    # Bobby and Sunny
    draw_character(d, 330, 850, "BOBBY",
                   "#2471A3", "#202020",
                   bobby_expression, bobby_hand)

    draw_character(d, 750, 850, "SUNNY",
                   "#E67E22", "#302018",
                   sunny_expression, sunny_hand)

    d.text((80, 1650), "BOBBY & SUNNY COMEDY",
           fill="#333333")

    img.save(f"scenes/scene{number}.png")
    print(f"Scene {number} created")

make_scene(1, "A funny conversation begins!",
           "smile", "smile")

make_scene(2, "Wait... what happened?",
           "surprise", "laugh", "up")

make_scene(3, "That's the real punchline!",
           "laugh", "laugh", "up", "up")

print("Bobby and Sunny cartoon scenes created!")
