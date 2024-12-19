import string

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

from setuptools.command.rotate import rotate


def code(width=140, height=40, char_length=4, font_size1=20, font_size2=40):
    code = []
    img = Image.new(mode="RGB", size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    for i in range(char_length):
        char = randomChar()
        code.append(char)
        x = i * width / char_length
        y = random.randint(1, 15)
        draw.text((x, y), char, fill=randomColor(), font_size=random.randint(font_size1, font_size2))

    for i in range(2):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=randomColor(), width=random.randint(1, 3))

    for i in range(3):
        x1 = random.randint(1, width - 1)
        y1 = random.randint(1, height - 1)
        x2 = random.randint(x1 + 1, width)
        y2 = random.randint(y1 + 1, height)
        draw.arc((x1, y1, x2, y2), start=1, end=random.randint(10, 300), fill=randomColor(), width=random.randint(1, 3))

    for i in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        color = randomColor()
        draw.point((x, y), fill=color)
        draw.point(((x + y) % width, (y * y) % height), fill=color)
        draw.point(((x + x) % width, (y + x) % height), fill=color)
        draw.point(((x * x) % width, (y * x) % height), fill=color)
        draw.point(((3 * x) % width, (5 * y) % height), fill=color)

        draw.point(((x + 8) % width, (y * 5) % height), fill=color)
        draw.point(((x + 55) % width, (y + 88) % height), fill=color)
        draw.point(((x * 3) % width, (y * 5) % height), fill=color)
        draw.point(((3 * 11) % width, (5 * 6) % height), fill=color)

    return img, ''.join(code)


def randomChar():
    char = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits))
    return char


def randomColor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
