"""Render the overview screen
    Open overview.png
    Draw champion name, KDA, win loss
    Save to overview_matchid.png"""

from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO

def generate_overview_image():
    current_folder = os.path.dirname(__file__)
    image_path = os.path.join(current_folder, "d1b11d5e4dbae547ac0d651476cec488.jpg")

    img = Image.open(image_path)
    buffer = BytesIO()
    img.save(buffer, format="jpeg")
    buffer.seek(0)
    return buffer

