"""Render the overview screen
    Open overview.png
    Draw champion name, KDA, win loss
    Save to overview_matchid.png"""

from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO

def generate_overview_image():
    current_folder = os.path.dirname(__file__)
    image_path = os.path.join(current_folder, "assets/templates/overview design.png")

    img = Image.open(image_path)
    buffer = BytesIO()
    img.save(buffer, format="png")
    buffer.seek(0)
    return buffer

generate_overview_image()