"""
This file contains functions and constants required to generate images suitable for a mock NFT project.

@author: Zack West <alphazwest@gmail.com>
@version: 1.0.0
@date: 5/27/2022
"""

from PIL import Image, ImageDraw, ImageColor, ImageFont
import os
import shutil
import json
import random
import time

HERE = os.path.abspath(os.path.dirname(__file__))

# Hard statics
TOTAL_IMAGES = 1000
COUNT = 256
SIZE = (1024, 1024)
EXT = '.jpg'
FONT_SIZE = 512
OUTPUT_DIR = os.path.abspath(os.path.join(HERE, 'output'))
FONT = os.path.abspath(os.path.join(HERE, 'fonts', 'Volkhov-Bold.ttf'))

# Creates output directory if not existing
if not(os.path.exists(OUTPUT_DIR)):
    os.mkdir(os.path.abspath(OUTPUT_DIR))

# Color pallets w/weighted distributions (for rarity simulation)
_DARKS = {"171212": 5, "002500": 4, "083b49": 3, "3d2b00": 2, "3c011d": 1}
DARKS = [x for k, v in _DARKS.items() for x in [k] * v]
_LIGHTS = {"f58eb9": 5, "e19451": 4, "f8f4a6": 3, "bdf7b7": 2, "b1b5e7": 1}
LIGHTS = [x for k, v in _LIGHTS.items() for x in [k] * v]

# Source letters and weighted distributions. Note: the weights are the frequency distribution
# of English alphabet letters in the dictionary where x is the least frequency, e is the most
# such that the "rarity" scoring my e.g. OpenSea will reflect, roughly, these values for the letters.
LETTERS = {
    'a': 0.0846402860096712, 'h': 0.026430828106619526, 'e': 0.10772176322650225, 'd': 0.03238955368790574,
    'i': 0.08956630698939853, 'n': 0.0719479487121524, 'g': 0.023643469967582403, 's': 0.0716180211960545,
    'l': 0.05577434674781033, 'm': 0.030104955866114096, 'r': 0.07043308637891531, 'v': 0.009464312744959735,
    'k': 0.007672746241673479, 'w': 0.006411696316744151, 'o': 0.07199344608861344, 'f': 0.011227836840112776,
    'c': 0.0437750575370124, 't': 0.06606991659100463, 'u': 0.03762718877433788, 'b': 0.018296526718835086,
    'y': 0.02019654294337122, 'x': 0.0030025406994062735, 'j': 0.001561218150763426, 'p': 0.03252432893515823,
    'z': 0.004222671600222851, 'q': 0.0016834029290581443
}


class MetaData:
    """
    Wrapper for image metadata
    """
    def __init__(self, bg_color: str, letter: str, letter_color: str):
        self.bg_color = bg_color
        self.letter = letter
        self.letter_color = letter_color

    def to_dict(self):
        return {
            "bg_color": self.bg_color,
            "letter": self.letter,
            "letter_color": self.letter_color,
        }

    def as_os_metadata(self):
        """Returns as OpenSea features"""
        return [{"trait_type": k, "value": v} for k, v in self.__dict__.items() if k[0] != "_"]


def clear_output_dir():
    """Clears all images"""
    for file in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, file)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)


def create_bg(color: ImageColor):
    """Creates an image with a background color"""
    return Image.new("RGB", size=SIZE, color=color)


def get_random_letter():
    """Get a random letter from [a-zA-Z]"""
    # return random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    rand = random.random() * sum(LETTERS.values())
    for k, v in LETTERS.items():
        rand -= v
        if rand < 0:
            return k


def get_random_hex_color(pallete: None or list = None):
    """
    Get a random hex color
    Note: Pillow needs the "#" prefix to work.
    """
    if not pallete:
        return "#" + "".join(random.choice("abcdef01234567") for _ in range(6))
    return "#" + random.choice(pallete)


def get_font():
    """returns a font object sized to spec"""
    return ImageFont.truetype(FONT, FONT_SIZE)


def gen_image() -> tuple:
    """
    Creates an images of SIZE with random bg color
    and randomly-colored letter in center.
    """
    # Get the attrs
    bg_color = get_random_hex_color(pallete=DARKS)
    letter_color = get_random_hex_color(pallete=LIGHTS)
    letter = get_random_letter()

    # create the image
    bg = create_bg(color=bg_color)
    draw = ImageDraw.Draw(bg)
    font = get_font()

    draw.text(
        xy=(SIZE[0] / 2, SIZE[1] / 2),
        text=letter,
        fill=letter_color,
        font=font,
        anchor="mm",
        align="center"
    )

    # return the image + metadata
    return bg, MetaData(bg_color, letter, letter_color)


def save_output(image_name: str, image: Image, meta: MetaData):
    """Save the image and data"""
    image.save(os.path.abspath(os.path.join(HERE, OUTPUT_DIR, f"{image_name}{EXT}")))
    with open(os.path.abspath(os.path.join(HERE, OUTPUT_DIR, f"{image_name}-meta.json")), 'w')as file:
        file.write(json.dumps(meta.as_os_metadata()))


def check_letter_distribution():
    """
    Un unused utility function that creates a million-character
    distribution of letters based on their weighted values.
    todo why don't the weights need to be sorted?
    """
    total = 1000000
    counts = {}
    for i in range(total):
        letter = get_random_letter()
        if letter in counts:
            counts[letter] += 1
        else:
            counts[letter] = 1

    return {k: v / total for k, v in counts.items()}


def generate_images():
    """
    Generates the images using the parameters defined
    at the top of this file
    """
    # Generate Images
    for i in range(TOTAL_IMAGES):
        img, meta = gen_image()
        save_output(str(i), img, meta)


if __name__ == '__main__':
    print(f"Generating {TOTAL_IMAGES} images")
    st = time.time()
    generate_images()
    print(f"{TOTAL_IMAGES} images generated in {time.time() - st} seconds.")