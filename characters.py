
from PIL import Image, ImageDraw
import os

W, H = 600, 950

# Character colours
SKIN = "#E8AD82"
SKIN_SHADOW = "#C98560"
DARK = "#29202A"
WHITE = "#FFFFFF"
BLUE = "#2471A3"
GREEN = "#279B62"
PANTS = "#303B55"
SHOE = "#292D38"


def new_layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def save_layer(image, folder, filename):
    image.save(os.path.join(folder, filename))


def draw_body(folder, shirt):
    img = new_layer()
    d = ImageDraw.Draw(img)

    # Legs
    d.rounded_rectangle(
        (215, 610, 280, 850), radius=25, fill=PANTS
    )
    d.rounded_rectangle(
        (320, 610, 385, 850), radius=25, fill=PANTS
    )

    # Shoes
    d.rounded_rectangle(
        (185, 825, 295, 885), radius=25, fill=SHOE
    )
    d.rounded_rectangle(
        (305, 825, 415, 885), radius=25, fill=SHOE
    )

    # Shirt
    d.rounded_rectangle(
        (145, 320, 455, 650),
        radius=65, fill=shirt,
        outline=DARK, width=8
    )

    # Collar
    d.polygon(
        [(245, 325), (300, 380), (355, 325)],
        fill=WHITE, outline=DARK
    )

    # Buttons
    for y in (420, 475, 530):
        d.ellipse((294, y-7, 306, y+7), fill=WHITE)

    # Pocket
    d.rounded_rectangle(
        (365, 420, 420, 485),
        radius=8, outline=WHITE, width=4
    )

    save_layer(img, folder, "body.png")


def draw_arms(folder, direction="down"):
    img = new_layer()
    d = ImageDraw.Draw(img)

    if direction == "down":
        d.line((165, 375, 105, 590), fill=SKIN, width=48)
        d.line((435, 375, 495, 590), fill=SKIN, width=48)

        d.ellipse((80, 565, 130, 620), fill=SKIN)
        d.ellipse((470, 565, 520, 620), fill=SKIN)

    elif direction == "up":
        d.line((165, 375, 70, 210), fill=SKIN, width=48)
        d.line((435, 375, 530, 210), fill=SKIN, width=48)

        d.ellipse((45, 175, 95, 230), fill=SKIN)
        d.ellipse((505, 175, 555, 230), fill=SKIN)

    save_layer(img, folder, f"arms_{direction}.png")


def draw_head(folder, older=False):
    img = new_layer()
    d = ImageDraw.Draw(img)

    # Ears
    d.ellipse((135, 115, 205, 235), fill=SKIN, outline=DARK, width=6)
    d.ellipse((395, 115, 465, 235), fill=SKIN, outline=DARK, width=6)

    # Face
    if older:
        # Slightly longer and slimmer face
        d.ellipse(
            (170, 55, 430, 385),
            fill=SKIN, outline=DARK, width=8
        )
    else:
        # Rounder, younger face
        d.ellipse(
            (145, 55, 455, 365),
            fill=SKIN, outline=DARK, width=8
        )

    # Cheeks
    d.ellipse((170, 245, 225, 280), fill="#EF9B91")
    d.ellipse((375, 245, 430, 280), fill="#EF9B91")

    # Nose
    d.ellipse((286, 225, 314, 255), fill=SKIN_SHADOW)

    save_layer(img, folder, "head.png")


def draw_hair(folder, older=False):
    img = new_layer()
    d = ImageDraw.Draw(img)

    if not older:
        # Bobby: playful messy hair
        d.pieslice(
            (135, 15, 465, 245),
            180, 360, fill=DARK
        )

        for x, y, r in [
            (180, 90, 55),
            (240, 35, 48),
            (300, 55, 48),
            (365, 35, 50),
            (420, 90, 45)
        ]:
            d.ellipse((x-r, y-r, x+r, y+r), fill=DARK)

    else:
        # Sunny: mature, neatly combed hairstyle
        d.pieslice(
            (155, 10, 445, 230),
            180, 360, fill=DARK
        )

        d.polygon(
            [(185, 125), (205, 45), (300, 30),
             (410, 65), (430, 125), (355, 85),
             (270, 90)],
            fill=DARK
        )

        # Slight grey at both temples
        d.line(
            (165, 125, 185, 175),
            fill="#B9B9B9", width=10
        )
        d.line(
            (415, 125, 395, 175),
            fill="#B9B9B9", width=10
        )

    save_layer(img, folder, "hair.png")


def draw_eyes(folder, closed=False, older=False):
    img = new_layer()
    d = ImageDraw.Draw(img)

    if closed:
        d.arc((195, 175, 270, 225), 190, 350, fill=DARK, width=9)
        d.arc((330, 175, 405, 225), 190, 350, fill=DARK, width=9)

    else:
        eye_height = 58 if not older else 52

        d.ellipse(
            (195, 160, 270, 160 + eye_height),
            fill=WHITE, outline=DARK, width=5
        )
        d.ellipse(
            (330, 160, 405, 160 + eye_height),
            fill=WHITE, outline=DARK, width=5
        )

        d.ellipse((225, 178, 255, 215), fill=DARK)
        d.ellipse((360, 178, 390, 215), fill=DARK)

        d.ellipse((230, 180, 242, 192), fill=WHITE)
        d.ellipse((365, 180, 377, 192), fill=WHITE)

    # Eyebrows
    if older:
        d.line((190, 145, 270, 135), fill=DARK, width=12)
        d.line((330, 135, 410, 145), fill=DARK, width=12)
    else:
        d.line((190, 135, 270, 145), fill=DARK, width=12)
        d.line((330, 145, 410, 135), fill=DARK, width=12)

    filename = "eyes_closed.png" if closed else "eyes_open.png"
    save_layer(img, folder, filename)


def draw_mouth(folder, expression):
    img = new_layer()
    d = ImageDraw.Draw(img)

    if expression == "closed":
        d.arc(
            (245, 265, 355, 320),
            0, 180, fill="#7B2525", width=9
        )

    elif expression == "open":
        d.ellipse(
            (260, 265, 340, 345),
            fill="#7B2525"
        )
        d.arc(
            (270, 270, 330, 305),
            0, 180, fill=WHITE, width=6
        )

    elif expression == "smile":
        d.arc(
            (240, 255, 360, 335),
            0, 180, fill="#7B2525", width=10
        )

    elif expression == "surprise":
        d.ellipse(
            (275, 265, 325, 340),
            fill="#7B2525"
        )

    save_layer(img, folder, f"mouth_{expression}.png")


def create_character(name, shirt, older=False):
    folder = os.path.join("characters", name.lower())
    os.makedirs(folder, exist_ok=True)

    draw_body(folder, shirt)

    draw_arms(folder, "down")
    draw_arms(folder, "up")

    draw_head(folder, older)
    draw_hair(folder, older)

    draw_eyes(folder, closed=False, older=older)
    draw_eyes(folder, closed=True, older=older)

    for expression in ["closed", "open", "smile", "surprise"]:
        draw_mouth(folder, expression)

    print(name, "character assets created!")


# Bobby: younger, round face, blue shirt
create_character("Bobby", BLUE, older=False)

# Sunny: older, slim face, green shirt, slight grey hair
create_character("Sunny", GREEN, older=True)

print("All character animation assets created successfully!")
