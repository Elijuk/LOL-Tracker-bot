"""utils.py

Contains shared helper function across multiple rendering components"""

# ========== Imports ==========
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple

from .constants import ImageSizes, Colors


# ========== Imports ==========
def crop_to_circle(
        img: Image.Image,
        size: int = ImageSizes.CHAMPION_ICON,
        inwards: int = ImageSizes.CHAMPION_CIRCLE_INSET
) -> Image.Image:
    """
    Crop an image to a circle with transparency.
    
    Args:
        img: Input image
        size: Diameter of the circle (default = CHANPION_ICON (80))
        inwards: Pixels to inset from edges (default = CHAMPION_CIRCLE_INSET)
    
    Returns:
        Circular image
    """
    img = img.resize((size, size))
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((inwards, inwards, size - inwards, size - inwards), fill=255)
    img.putalpha(mask)
    return img


def draw_text_with_shadow(
    draw: ImageDraw.ImageDraw,
    position: Tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: Tuple[int, int, int, int] = Colors.WHITE,
    shadow_color: Tuple[int, int, int, int] = Colors.SHADOW,
    offset: int = 2,
    anchor: str = "la"
) -> None:
    """
    Draw text with a shadow which looks less plain.
    
    Args:
        draw: ImageDraw object
        position: (x, y) coordinates
        text: Text to draw
        font: Font to use
        fill: Main text color (RGBA)
        shadow_color: Shadow color (RGBA)
        offset: Pixel offset for shadow
        anchor: Text anchor point ("la" or "ra", default "la")
    """
    x, y = position
    draw.text((x + offset, y + offset), text, font=font, fill=shadow_color, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)