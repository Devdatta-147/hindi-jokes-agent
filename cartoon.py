
from PIL import Image, ImageDraw
import os

WIDTH = 1080
HEIGHT = 1920

os.makedirs("scenes", exist_ok=True)


def draw_sofa(draw):
    # Sofa
    draw.rounded_rectangle(
        (650, 950, 1030, 1240),
        radius=45,
        fill="#547C91",
        outline="#36576A",
        width=12
    )
    draw.rounded_rectangle(
        (680, 890, 1000, 1100),
        radius=35,
        fill="#7299AA"
    )
    draw.line((840, 970, 840, 1200), fill="#36576A", width=8)

    # Cushions
    draw.rounded_rectangle(
        (700, 1000, 820, 1130),
        radius=25,
        fill="#F4C76B"
    )
    draw.rounded_rectangle(
        (860, 1000, 980, 1130),
        radius=25,
        fill="#D98B70"
    )

    # Small tea table
    draw.rounded_rectangle(
        (35, 1110, 260, 1160),
        radius=12,
        fill="#8B573A"
    )
    draw.rectangle((55, 1150, 75, 1280), fill="#68412E")
    draw.rectangle((220, 1150, 240, 1280), fill="#68412E")

    # Tea cup
    draw.rounded_rectangle(
        (105, 1040, 175, 1110),
        radius=12,
        fill="#FFFFFF",
        outline="#68412E",
        width=6
    )
    draw.arc((160, 1050, 205, 1100), 270, 90, fill="#68412E", width=7)
    draw.line((115, 1035, 115, 1010), fill="#FFFFFF", width=5)
    draw.line((140, 1035, 140, 1005), fill="#FFFFFF", width=5)


def draw_bookshelf(draw):
    # Shelf frame
    draw.rounded_rectangle(
        (690, 480, 1020, 1050),
        radius=18,
        fill="#9A623D",
        outline="#68412E",
        width=12
    )

    for y in (660, 850):
        draw.rectangle((700, y, 1010, y + 18), fill="#68412E")

    # Books on shelves
    book_colors = [
        "#D96C59", "#F2C14E", "#6B9E78",
        "#6A8CAF", "#B77B9E", "#E7A45B"
    ]

    for shelf_y in (520, 690, 880):
        x = 720
        for index, color in enumerate(book_colors):
            book_width = 35 if index % 2 == 0 else 42
            draw.rounded_rectangle(
                (x, shelf_y, x + book_width, shelf_y + 125),
                radius=5,
                fill=color
            )
            draw.line(
                (x + 7, shelf_y + 20, x + book_width - 7, shelf_y + 20),
                fill="#FFFFFF",
                width=4
            )
            x += 48

    # Mobile phone on small table
    draw.rounded_rectangle(
        (55, 1050, 145, 1200),
        radius=15,
        fill="#293746",
        outline="#FFFFFF",
        width=5
    )
    draw.rounded_rectangle(
        (65, 1065, 135, 1175),
        radius=8,
        fill="#8ED5E8"
    )
    draw.ellipse((95, 1180, 110, 1195), fill="#FFFFFF")


def draw_office(draw):
    # Office desk
    draw.rounded_rectangle(
        (620, 1080, 1050, 1160),
        radius=15,
        fill="#8B573A"
    )
    draw.rectangle((660, 1150, 690, 1320), fill="#68412E")
    draw.rectangle((980, 1150, 1010, 1320), fill="#68412E")

    # Computer monitor
    draw.rounded_rectangle(
        (750, 850, 980, 1050),
        radius=18,
        fill="#293746",
        outline="#526A7A",
        width=12
    )
    draw.rounded_rectangle(
        (770, 870, 960, 1025),
        radius=8,
        fill="#91D5E8"
    )
    draw.rectangle((850, 1050, 880, 1080), fill="#526A7A")
    draw.rounded_rectangle(
        (810, 1070, 920, 1090),
        radius=8,
        fill="#526A7A"
    )

    # Keyboard
    draw.rounded_rectangle(
        (720, 1110, 920, 1140),
        radius=8,
        fill="#D7DEE4"
    )

    # Newspaper
    draw.rectangle(
        (60, 1050, 300, 1170),
        fill="#FFFDF5",
        outline="#777777",
        width=5
    )
    draw.text((80, 1060), "NEWS", fill="#293746")
    draw.line((80, 1095, 275, 1095), fill="#777777", width=4)
    draw.line((80, 1115, 270, 1115), fill="#777777", width=3)
    draw.line((80, 1135, 250, 1135), fill="#777777", width=3)


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

    # Scene-specific wall decoration and comedy props
    if scene_number == 1:
        draw.rounded_rectangle(
            (650, 220, 980, 430),
            radius=30,
            fill="#F5C76E"
        )
        draw.text(
            (715, 290),
            "WELCOME!",
            fill="#543A27"
        )
        draw_sofa(draw)

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
        draw_bookshelf(draw)

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
        draw_office(draw)

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

print("Three cartoon backgrounds with comedy props created successfully!")
