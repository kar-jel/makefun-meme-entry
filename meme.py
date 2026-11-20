from pathlib import Path
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
SIZE = 1200
BG = (13, 15, 18)
PINK = (255, 45, 149)
WHITE = (247, 247, 249)


def font(size):
    return ImageFont.truetype(str(ROOT / "fonts" / "Anton.ttf"), size)


def centered_text(draw, xy, text, face, fill):
    draw.text(xy, text, font=face, fill=fill, anchor="mm", stroke_width=0)


def draw_background():
    image = Image.new("RGB", (SIZE, SIZE), BG)
    pixels = image.load()
    random.seed(614)
    for y in range(SIZE):
        lift = int(9 * (1 - y / (SIZE - 1)))
        for x in range(SIZE):
            grain = random.choice((-2, -1, 0, 0, 0, 1, 2))
            pixels[x, y] = tuple(max(0, min(255, c + lift + grain)) for c in BG)
    return image


def draw_top_panel(image):
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((72, 65, 1128, 226), radius=26, fill=(25, 28, 33))
    centered_text(draw, (600, 145), 'BOSS: "OUT SICK AGAIN?"', font(73), WHITE)


def draw_mascot(image):
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((365, 270, 835, 740), fill=(255, 45, 149, 75))
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    image.paste(glow, (0, 0), glow)
    mark = Image.open(ROOT / "assets" / "mark-1024.png").convert("RGBA")
    mark.thumbnail((420, 420), Image.Resampling.LANCZOS)
    image.paste(mark, ((SIZE - mark.width) // 2, 290), mark)


def draw_bottom_panel(image):
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((72, 735, 1128, 1047), radius=26, fill=(25, 28, 33))
    centered_text(draw, (600, 808), 'ME: "I WAITED 13 YEARS FOR THIS.', font(57), WHITE)
    face = font(48)
    parts = [('MY AI AGENT IS ON ', WHITE), ('make.fun', PINK), (' WINNING THE RENT."', WHITE)]
    widths = [draw.textbbox((0, 0), text, font=face)[2] for text, color in parts]
    x = (SIZE - sum(widths)) // 2
    for (text, color), width in zip(parts, widths):
        draw.text((x, 906), text, font=face, fill=color)
        x += width


def draw_footer(image):
    draw = ImageDraw.Draw(image)
    draw.line((92, 1080, 1108, 1080), fill=(74, 78, 85), width=2)
    centered_text(draw, (600, 1130), 'make.fun — people and their AI agents build things, enter bounties, win real money', font(27), (205, 207, 212))


def main():
    image = draw_background()
    draw_top_panel(image)
    draw_mascot(image)
    draw_bottom_panel(image)
    draw_footer(image)
    output = ROOT / "meme.png"
    image.save(output, format="PNG", optimize=True)
    print(f"Wrote {output} ({image.width}x{image.height})")


if __name__ == "__main__":
    main()
