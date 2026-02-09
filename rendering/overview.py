# ========== Imports ==========
import os

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from rendering.assets import get_image
import riot.extractors
from riot.riot_types import *


# ========== Functions ==========
def _crop_to_circle(img: Image.Image) -> Image.Image:
    # Create a circular mask that matches the resized image dimensions
    mask = Image.new("L", (128, 128), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((17, 17, 111, 111), fill=255)

    # Apply the mask
    img.putalpha(mask)
    return img


async def generate_overview_image(match_data: MatchData):
    current_folder = os.path.dirname(__file__)
    template_path = os.path.join(current_folder, "assets/templates/overview design.png")

    # 1. Open template as FIL object (RGBA for transparency)
    template = Image.open(template_path).convert("RGBA")

    # 2. Extract match info and participants
    participants = riot.extractors.get_participants(match_data)
    
    # 3. Fetch all champion names asynchronously
    y = 110

    for i, participant in enumerate(participants):
        champ_img = await get_image(participant["championName"], "champion")
        if not champ_img:
            return

        champ_img_circle = _crop_to_circle(champ_img)
        template.paste(champ_img_circle, ((166 if i < 5 else 1626), y + ((i if i < 5 else i - 5) * 200)), champ_img_circle)
        
    buffer = BytesIO()
    template.save(buffer, format="png")
    buffer.seek(0)

    return buffer
