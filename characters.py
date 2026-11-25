
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

    # Legs with subtle depth
    d.rounded_rectangle(
        (215, 610, 280, 850),
        radius=28, fill="#252F46"
    )
    d.rounded_rectangle(
        (320, 610, 385, 850),
        radius=28, fill=PANTS
    )

    # Trouser highlights
    d.line((235, 650, 235, 810), fill="#46516A", width=5)
    d.line((340, 650, 340, 810), fill="#46516A", width=5)

    # Shoes
    d.rounded_rectangle(
        (185, 825, 295, 885),
        radius=25, fill=SHOE,
        outline="#171B25", width=5
    )
    d.rounded_rectangle(
        (305, 825, 415, 885),
        radius=25, fill=SHOE,
        outline="#171B25", width=5
    )
    d.line((205, 850, 275, 850), fill="#596071", width=5)
    d.line((325, 850, 395, 850), fill="#596071", width=5)

    # Shirt body
    d.rounded_rectangle(
        (145, 320, 455, 650),
        radius=65,
        fill=shirt,
        outline=DARK,
        width=9
    )

    # Side shadows for a rounded 3D appearance
    d.rounded_rectangle(
        (145, 355, 180, 615),
        radius=18, fill="#173E50"
    )
    d.rounded_rectangle(
        (420, 355, 455, 615),
        radius=18, fill="#173E50"
    )

    # Shirt highlight
    d.rounded_rectangle(
        (195, 345, 225, 590),
        radius=14, fill="#FFFFFF"
    )
    d.rounded_rectangle(
        (195, 345, 225, 590),
        radius=14, fill=shirt
    )

    # Collar
    d.polygon(
        [(235, 325), (300, 390), (365, 325)],
        fill="#F7F3E9",
        outline=DARK
    )
    d.line((300, 390, 300, 620), fill=DARK, width=5)

    # Buttons
    for y in (425, 480, 535):
        d.ellipse(
            (292, y-7, 308, y+7),
            fill="#F5E6C8",
            outline=DARK,
            width=2
        )

    # Chest pocket
    d.rounded_rectangle(
        (365, 420, 420, 490),
        radius=9,
        fill=shirt,
        outline="#D9E5E8",
        width=4
    )
    d.line((375, 430, 410, 430), fill="#D9E5E8", width=3)

    # Sleeve seams
    d.arc((135, 320, 250, 435), 0, 180, fill="#D9E5E8", width=4)
    d.arc((350, 320, 465, 435), 0, 180, fill="#D9E5E8", width=4)

    save_layer(img, folder, "body.png")


def draw_arms(folder, direction="down"):
    img = new_layer()
    d = ImageDraw.Draw(img)

    if direction == "down":
        d.line(
            (165, 375, 105, 590),
            fill=SKIN, width=48
        )
        d.line(
            (435, 375, 495, 590),
            fill=SKIN, width=48
        )
        d.ellipse((80, 565, 130, 620), fill=SKIN)
        d.ellipse((470, 565, 520, 620), fill=SKIN)

    elif direction == "up":
        d.line(
            (165, 375, 70, 210),
            fill=SKIN, width=48
        )
        d.line(
            (435, 375, 530, 210),
            fill=SKIN, width=48
        )
        d.ellipse((45, 175, 95, 230), fill=SKIN)
        d.ellipse((505, 175, 555, 230), fill=SKIN)

    elif direction == "point":
        # One arm pointing outward
        d.line(
            (165, 375, 90, 485),
            fill=SKIN, width=48
        )
        d.ellipse((65, 460, 115, 510), fill=SKIN)

        d.line(
            (435, 375, 495, 590),
            fill=SKIN, width=48
        )
        d.ellipse((470, 565, 520, 620), fill=SKIN)

        # Pointing finger
        d.line(
            (90, 480, 35, 445),
            fill=SKIN, width=22
        )

    elif direction == "hips":
        # Hands resting on hips
        d.line(
            (165, 375, 115, 500, 175, 535),
            fill=SKIN, width=45,
            joint="curve"
        )
        d.line(
            (435, 375, 485, 500, 425, 535),
            fill=SKIN, width=45,
            joint="curve"
        )
        d.ellipse((150, 510, 205, 555), fill=SKIN)
        d.ellipse((395, 510, 450, 555), fill=SKIN)

    elif direction == "folded":
        # Folded arms
        d.line(
            (165, 375, 235, 470, 390, 455),
            fill=SKIN, width=45,
            joint="curve"
        )
        d.line(
            (435, 375, 365, 515, 210, 495),
            fill=SKIN, width=45,
            joint="curve"
        )
        d.ellipse((365, 430, 415, 480), fill=SKIN)
        d.ellipse((190, 470, 240, 520), fill=SKIN)

    elif direction == "one_hand":
        # One hand raised for explaining
        d.line(
            (165, 375, 100, 260),
            fill=SKIN, width=48
        )
        d.ellipse((75, 225, 125, 280), fill=SKIN)

        d.line(
            (435, 375, 495, 590),
            fill=SKIN, width=48
        )
        d.ellipse((470, 565, 520, 620), fill=SKIN)

    elif direction == "facepalm":
        # One arm raised towards forehead
        d.line(
            (435, 375, 490, 250, 405, 165),
            fill=SKIN, width=48,
            joint="curve"
        )
        d.ellipse((380, 130, 430, 185), fill=SKIN)

        d.line(
            (165, 375, 105, 590),
            fill=SKIN, width=48
        )
        d.ellipse((80, 565, 130, 620), fill=SKIN)

    elif direction == "laugh":
        # Both arms lifted in a cheerful pose
        d.line(
            (165, 375, 90, 260),
            fill=SKIN, width=48
        )
        d.line(
            (435, 375, 510, 260),
            fill=SKIN, width=48
        )
        d.ellipse((65, 225, 115, 280), fill=SKIN)
        d.ellipse((485, 225, 535, 280), fill=SKIN)

    save_layer(img, folder, f"arms_{direction}.png")


def draw_head(folder, older=False, tilt="normal"):
    img = new_layer()
    d = ImageDraw.Draw(img)

    shift = {
        "normal": 0,
        "left": -15,
        "right": 15
    }[tilt]

    # Ears
    d.ellipse(
        (135+shift, 115, 205+shift, 235),
        fill=SKIN,
        outline=DARK,
        width=6
    )
    d.ellipse(
        (395+shift, 115, 465+shift, 235),
        fill=SKIN,
        outline=DARK,
        width=6
    )

    # Head shape
    if older:
        d.ellipse(
            (170+shift, 55, 430+shift, 385),
            fill=SKIN,
            outline=DARK,
            width=8
        )
    else:
        d.ellipse(
            (145+shift, 55, 455+shift, 365),
            fill=SKIN,
            outline=DARK,
            width=8
        )

    # Cheeks
    d.ellipse(
        (170+shift, 245, 225+shift, 280),
        fill="#EF9B91"
    )
    d.ellipse(
        (375+shift, 245, 430+shift, 280),
        fill="#EF9B91"
    )

    # Nose
    d.ellipse(
        (286+shift, 225, 314+shift, 255),
        fill=SKIN_SHADOW
    )

    save_layer(img, folder, f"head_{tilt}.png")


def draw_hair(folder, older=False):
    img = new_layer()
    d = ImageDraw.Draw(img)

    if not older:
        # Bobby's messy hairstyle
        d.pieslice(
            (135, 15, 465, 245),
            180, 360,
            fill=DARK
        )

        for x, y, r in [
            (180, 90, 55),
            (240, 35, 48),
            (300, 55, 48),
            (365, 35, 50),
            (420, 90, 45)
        ]:
            d.ellipse(
                (x-r, y-r, x+r, y+r),
                fill=DARK
            )

    else:
        # Sunny's neatly combed hair
        d.pieslice(
            (155, 10, 445, 230),
            180, 360,
            fill=DARK
        )

        d.polygon(
            [
                (185, 125),
                (205, 45),
                (300, 30),
                (410, 65),
                (430, 125),
                (355, 85),
                (270, 90)
            ],
            fill=DARK
        )

        # Slight grey hair at temples
        d.line(
            (165, 125, 185, 175),
            fill="#B9B9B9",
            width=10
        )
        d.line(
            (415, 125, 395, 175),
            fill="#B9B9B9",
            width=10
        )

    save_layer(img, folder, "hair.png")


def draw_eyes(folder, expression="normal", older=False):
    img = new_layer()
    d = ImageDraw.Draw(img)

    if expression == "closed":
        d.arc(
            (195, 175, 270, 225),
            190, 350,
            fill=DARK,
            width=9
        )
        d.arc(
            (330, 175, 405, 225),
            190, 350,
            fill=DARK,
            width=9
        )

    else:
        if expression == "surprised":
            height = 75
        elif expression == "narrow":
            height = 35
        else:
            height = 58 if not older else 52

        d.ellipse(
            (195, 160, 270, 160+height),
            fill=WHITE,
            outline=DARK,
            width=5
        )
        d.ellipse(
            (330, 160, 405, 160+height),
            fill=WHITE,
            outline=DARK,
            width=5
        )

        pupil_y = (
            185 if expression == "surprised"
            else 178
        )

        d.ellipse(
            (225, pupil_y, 255, pupil_y+37),
            fill=DARK
        )
        d.ellipse(
            (360, pupil_y, 390, pupil_y+37),
            fill=DARK
        )

        d.ellipse(
            (230, pupil_y+2, 242, pupil_y+14),
            fill=WHITE
        )
        d.ellipse(
            (365, pupil_y+2, 377, pupil_y+14),
            fill=WHITE
        )

    # Eyebrow styles
    if expression == "surprised":
        d.line(
            (190, 115, 270, 115),
            fill=DARK, width=13
        )
        d.line(
            (330, 115, 410, 115),
            fill=DARK, width=13
        )

    elif expression == "angry":
        d.line(
            (190, 125, 270, 155),
            fill=DARK, width=14
        )
        d.line(
            (330, 155, 410, 125),
            fill=DARK, width=14
        )

    elif expression == "worried":
        d.line(
            (190, 130, 270, 155),
            fill=DARK, width=12
        )
        d.line(
            (330, 155, 410, 130),
            fill=DARK, width=12
        )

    elif older:
        d.line(
            (190, 145, 270, 135),
            fill=DARK, width=12
        )
        d.line(
            (330, 135, 410, 145),
            fill=DARK, width=12
        )

    else:
        d.line(
            (190, 135, 270, 145),
            fill=DARK, width=12
        )
        d.line(
            (330, 145, 410, 135),
            fill=DARK, width=12
        )

    save_layer(
        img,
        folder,
        f"eyes_{expression}.png"
    )


def draw_mouth(folder, expression):
    img = new_layer()
    d = ImageDraw.Draw(img)

    if expression == "closed":
        d.arc(
            (245, 265, 355, 320),
            0, 180,
            fill="#7B2525",
            width=9
        )

    elif expression == "open":
        d.ellipse(
            (260, 265, 340, 345),
            fill="#7B2525"
        )
        d.arc(
            (270, 270, 330, 305),
            0, 180,
            fill=WHITE,
            width=6
        )

    elif expression == "smile":
        d.arc(
            (240, 255, 360, 335),
            0, 180,
            fill="#7B2525",
            width=10
        )

    elif expression == "surprise":
        d.ellipse(
            (275, 265, 325, 340),
            fill="#7B2525"
        )

    elif expression == "laugh":
        d.ellipse(
            (245, 260, 355, 350),
            fill="#7B2525"
        )
        d.rectangle(
            (260, 260, 340, 285),
            fill=WHITE
        )
        d.arc(
            (245, 260, 355, 350),
            0, 180,
            fill=DARK,
            width=5
        )

    save_layer(
        img,
        folder,
        f"mouth_{expression}.png"
    )


def create_character(name, shirt, older=False):
    folder = os.path.join(
        "characters",
        name.lower()
    )
    os.makedirs(folder, exist_ok=True)

    draw_body(folder, shirt)

    # Original poses: preserve compatibility
    for pose in [
        "down",
        "up"
    ]:
        draw_arms(folder, pose)

    # Additional poses
    if name == "Bobby":
        poses = [
            "point",
            "hips",
            "laugh"
        ]
    else:
        poses = [
            "folded",
            "one_hand",
            "facepalm"
        ]

    for pose in poses:
        draw_arms(folder, pose)

    # Head poses
    for tilt in [
        "normal",
        "left",
        "right"
    ]:
        draw_head(folder, older, tilt)

    draw_hair(folder, older)

    # Eye expressions
    for expression in [
        "normal",
        "closed",
        "surprised",
        "narrow",
        "angry",
        "worried"
    ]:
        draw_eyes(folder, expression, older)

    # Mouth expressions
    for expression in [
        "closed",
        "open",
        "smile",
        "surprise",
        "laugh"
    ]:
        draw_mouth(folder, expression)

    print(name, "character assets created!")


create_character("Bobby", BLUE, older=False)
create_character("Sunny", GREEN, older=True)

print("All character animation assets created successfully!")
