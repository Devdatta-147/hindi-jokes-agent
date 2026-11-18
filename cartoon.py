
from PIL import Image, ImageDraw, ImageFont
import os
import math

os.makedirs("scenes", exist_ok=True)

W, H = 1080, 1920

SKIN = "#E8AD82"
SKIN_SHADOW = "#C98560"
DARK = "#29202A"
WHITE = "#FFFFFF"
BLUE = "#2471A3"
GREEN = "#279B62"
PANTS = "#303B55"

def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def draw_character(draw, x, y, name, shirt, expression="smile",
                   hand="down", hairstyle="bobby"):

    # Ground shadow
    draw.ellipse((x-145, y+700, x+145, y+745),
                 fill="#B7C8B2")

    # Legs
    draw.rounded_rectangle(
        (x-85, y+475, x-12, y+690),
        radius=25, fill=PANTS
    )
    draw.rounded_rectangle(
        (x+12, y+475, x+85, y+690),
        radius=25, fill=PANTS
    )

    # Shoes
    draw.rounded_rectangle(
        (x-110, y+665, x-5, y+725),
        radius=25, fill="#292D38"
    )
    draw.rounded_rectangle(
        (x+5, y+665, x+110, y+725),
        radius=25, fill="#292D38"
    )

    # Arms
    if hand == "up":
        draw.line(
            (x-90, y+300, x-185, y+155),
            fill=SKIN, width=55
        )
        draw.ellipse(
            (x-215, y+125, x-155, y+185),
            fill=SKIN
        )
        draw.line(
            (x+90, y+300, x+180, y+420),
            fill=SKIN, width=55
        )
    else:
        draw.line(
            (x-90, y+300, x-145, y+475),
            fill=SKIN, width=55
        )
        draw.line(
            (x+90, y+300, x+145, y+475),
            fill=SKIN, width=55
        )

    # Body
    draw.rounded_rectangle(
        (x-115, y+220, x+115, y+535),
        radius=65, fill=shirt,
        outline=DARK, width=8
    )

    # Shirt collar
    draw.polygon(
        [(x-42, y+225), (x, y+275), (x+42, y+225)],
        fill="#FFFFFF", outline=DARK
    )

    # Shirt buttons
    for by in (315, 365, 415):
        draw.ellipse(
            (x-6, y+by-6, x+6, y+by+6),
            fill="#FFFFFF"
        )

    # Shirt pocket
    draw.rounded_rectangle(
        (x+35, y+330, x+85, y+390),
        radius=8, outline="#FFFFFF", width=4
    )

    # Neck
    draw.rectangle(
        (x-38, y+145, x+38, y+270),
        fill=SKIN
    )

    # Ears
    draw.ellipse(
        (x-135, y-5, x-85, y+85),
        fill=SKIN, outline=DARK, width=6
    )
    draw.ellipse(
        (x+85, y-5, x+135, y+85),
        fill=SKIN, outline=DARK, width=6
    )

    # Head
    draw.ellipse(
        (x-125, y-100, x+125, y+205),
        fill=SKIN, outline=DARK, width=8
    )

    # Cheeks
    draw.ellipse(
        (x-105, y+95, x-55, y+130),
        fill="#EF9B91"
    )
    draw.ellipse(
        (x+55, y+95, x+105, y+130),
        fill="#EF9B91"
    )

    # Hairstyles
    if hairstyle == "bobby":
        draw.pieslice(
            (x-130, y-135, x+130, y+100),
            180, 360, fill=DARK
        )
        for hx, hy, r in [
            (x-90, y-105, 45),
            (x-35, y-140, 45),
            (x+25, y-135, 45),
            (x+85, y-100, 40)
        ]:
            draw.ellipse(
                (hx-r, hy-r, hx+r, hy+r),
                fill=DARK
            )
    else:
        draw.pieslice(
            (x-130, y-135, x+130, y+95),
            180, 360, fill=DARK
        )
        draw.ellipse(
            (x-115, y-125, x+65, y-35),
            fill=DARK
        )
        draw.polygon(
            [(x+5, y-95), (x+120, y-115),
             (x+95, y-45), (x+20, y-25)],
            fill=DARK
        )

    # Eyes
    draw.ellipse(
        (x-75, y+5, x-25, y+70),
        fill=WHITE, outline=DARK, width=4
    )
    draw.ellipse(
        (x+25, y+5, x+75, y+70),
        fill=WHITE, outline=DARK, width=4
    )

    draw.ellipse(
        (x-58, y+25, x-35, y+62),
        fill=DARK
    )
    draw.ellipse(
        (x+42, y+25, x+65, y+62),
        fill=DARK
    )

    # Eye highlights
    draw.ellipse(
        (x-53, y+27, x-43, y+38),
        fill=WHITE
    )
    draw.ellipse(
        (x+47, y+27, x+57, y+38),
        fill=WHITE
    )

    # Eyebrows
    if expression == "surprise":
        draw.line(
            (x-78, y-12, x-25, y-25),
            fill=DARK, width=10
        )
        draw.line(
            (x+25, y-25, x+78, y-12),
            fill=DARK, width=10
        )
    else:
        draw.line(
            (x-78, y-12, x-25, y-3),
            fill=DARK, width=10
        )
        draw.line(
            (x+25, y-3, x+78, y-12),
            fill=DARK, width=10
        )

    # Nose
    draw.ellipse(
        (x-13, y+75, x+13, y+100),
        fill=SKIN_SHADOW
    )

    # Mouth
    if expression == "laugh":
        draw.ellipse(
            (x-48, y+115, x+48, y+175),
            fill="#7B2525"
        )
        draw.arc(
            (x-38, y+118, x+38, y+155),
            0, 180, fill=WHITE, width=7
        )
    elif expression == "surprise":
        draw.ellipse(
            (x-22, y+120, x+22, y+170),
            fill="#7B2525"
        )
    else:
        draw.arc(
            (x-48, y+110, x+48, y+170),
            0, 180, fill="#7B2525", width=9
        )

    # Character name
    font = get_font(34, True)
    box = draw.textbbox((0, 0), name, font=font)
    text_width = box[2] - box[0]
    draw.text(
        (x-text_width//2, y+755),
        name, fill=DARK, font=font
    )

def make_scene(number, title, bobby_expression,
               sunny_expression, bobby_hand="down",
               sunny_hand="down"):

    img = Image.new("RGB", (W, H), "#FFF1D6")
    d = ImageDraw.Draw(img)

    # Cartoon park background
    d.rectangle((0, 1400, W, H), fill="#B8DFA5")
    d.rectangle((0, 0, W, 1400), fill="#BCE5F5")

    # Sun
    d.ellipse((820, 100, 1000, 280), fill="#FFD34E")

    # Clouds
    for cx, cy in [(160, 230), (520, 150), (760, 390)]:
        d.ellipse((cx-80, cy, cx+30, cy+75), fill=WHITE)
        d.ellipse((cx-20, cy-35, cx+90, cy+75), fill=WHITE)
        d.ellipse((cx+35, cy, cx+135, cy+75), fill=WHITE)

    # Title panel
    d.rounded_rectangle(
        (55, 400, 1025, 590),
        radius=45, fill=WHITE,
        outline="#E6A23C", width=7
    )

    font = get_font(38, True)
    d.text((95, 465), title, fill="#303044", font=font)

    # Characters
    draw_character(
        d, 330, 850, "BOBBY", BLUE,
        bobby_expression, bobby_hand, "bobby"
    )

    draw_character(
        d, 750, 850, "SUNNY", GREEN,
        sunny_expression, sunny_hand, "sunny"
    )

    # Bottom banner
    d.rounded_rectangle(
        (90, 1710, 990, 1830),
        radius=40, fill="#FFFFFF",
        outline="#E6A23C", width=5
    )

    d.text(
        (155, 1745),
        "BOBBY & SUNNY COMEDY",
        fill="#303044",
        font=get_font(34, True)
    )

    img.save(f"scenes/scene{number}.png")
    print(f"Scene {number} created")

make_scene(
    1, "A funny conversation begins!",
    "smile", "smile"
)

make_scene(
    2, "Wait... what happened?",
    "surprise", "laugh", "up"
)

make_scene(
    3, "That's the real punchline!",
    "laugh", "laugh", "up", "up"
)

print("2D cartoon scenes created!")
