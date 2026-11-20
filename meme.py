from pathlib import Path
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
SIZE = 1200
PINK = (255, 45, 149)
WHITE = (255, 248, 250)
BLACK = (7, 5, 13)


def font(size):
    return ImageFont.truetype(str(ROOT / "fonts" / "Anton.ttf"), size)


def centered_text(draw, xy, text, face, fill):
    draw.text(xy, text, font=face, fill=fill, anchor="mm", stroke_width=0)


def draw_background():
    image = Image.new("RGB", (SIZE, SIZE), BLACK)
    pixels = image.load()
    random.seed(614)
    stops = [(0, (31, 10, 70)), (0.43, (142, 17, 128)), (0.77, (255, 45, 149)), (1, (255, 116, 35))]
    for y in range(SIZE):
        t = y / (SIZE - 1)
        for index in range(len(stops) - 1):
            if stops[index][0] <= t <= stops[index + 1][0]:
                lo, a = stops[index]
                hi, b = stops[index + 1]
                f = (t - lo) / (hi - lo)
                color = tuple(round(a[c] * (1 - f) + b[c] * f) for c in range(3))
                break
        for x in range(SIZE):
            grain = random.choice((-2, -1, 0, 0, 0, 1, 2))
            pixels[x, y] = tuple(max(0, min(255, c + grain)) for c in color)
    return image


def draw_sunset(image):
    draw = ImageDraw.Draw(image)
    draw.ellipse((380, 220, 820, 660), fill=(255, 177, 91))
    draw.ellipse((410, 250, 790, 630), fill=(255, 194, 104))
    draw.rectangle((0, 850, SIZE, SIZE), fill=BLACK)
    draw.polygon([(0, 850), (95, 850), (95, 770), (175, 770), (175, 820), (245, 820), (245, 740), (310, 740), (310, 850), (405, 850), (405, 790), (500, 790), (500, 850), (600, 850), (600, 755), (685, 755), (685, 850), (790, 850), (790, 790), (875, 790), (875, 850), (965, 850), (965, 730), (1045, 730), (1045, 850), (1200, 850), (1200, 1200), (0, 1200)], fill=BLACK)
    draw.polygon([(170, 850), (180, 620), (190, 850)], fill=BLACK)
    draw.polygon([(180, 635), (95, 595), (34, 612), (110, 616), (45, 650), (130, 631), (165, 670)], fill=BLACK)
    draw.polygon([(182, 635), (240, 565), (305, 555), (250, 591), (316, 608), (230, 610), (198, 670)], fill=BLACK)
    draw.polygon([(1030, 850), (1044, 600), (1058, 850)], fill=BLACK)
    draw.polygon([(1044, 620), (968, 570), (905, 580), (978, 596), (920, 630), (1000, 610), (1032, 665)], fill=BLACK)
    draw.polygon([(1047, 620), (1110, 550), (1175, 548), (1120, 580), (1184, 605), (1100, 598), (1060, 665)], fill=BLACK)


def draw_top_panel(image):
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((64, 50, 1136, 174), radius=24, fill=(22, 13, 35))
    centered_text(draw, (600, 112), 'BOSS: "OUT SICK AGAIN?"', font(76), WHITE)
    centered_text(draw, (600, 204), 'GTA 6 LAUNCH WEEK', font(36), PINK)


def draw_mascot(image):
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((390, 260, 810, 680), fill=(255, 45, 149, 75))
    glow = glow.filter(ImageFilter.GaussianBlur(55))
    image.paste(glow, (0, 0), glow)
    mark = Image.open(ROOT / "assets" / "mark-1024.png").convert("RGBA")
    mark.thumbnail((400, 400), Image.Resampling.LANCZOS)
    image.paste(mark, ((SIZE - mark.width) // 2, 280), mark)
    draw = ImageDraw.Draw(image)
    centered_text(draw, (600, 705), "make.fun", font(78), PINK)


def draw_bottom_panel(image):
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((64, 748, 1136, 922), radius=22, fill=(22, 13, 35))
    centered_text(draw, (600, 788), 'ME: "GTA 6 IS OUT.', font(63), WHITE)
    centered_text(draw, (600, 860), 'I WAITED 13 YEARS - I EARNED THIS SICK DAY."', font(47), WHITE)


def draw_pitch(image):
    draw = ImageDraw.Draw(image)
    centered_text(draw, (600, 975), "my AI agent earns on make.fun while I play", font(46), WHITE)
    centered_text(draw, (600, 1035), "people + their agents build things, win bounties, get paid", font(31), WHITE)


def main():
    image = draw_background()
    draw_sunset(image)
    draw_top_panel(image)
    draw_mascot(image)
    draw_bottom_panel(image)
    draw_pitch(image)
    output = ROOT / "meme.png"
    image.save(output, format="PNG", optimize=True)
    print(f"Wrote {output} ({image.width}x{image.height})")


if __name__ == "__main__":
    main()
