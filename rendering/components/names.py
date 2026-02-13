from rendering.core.utils import draw_text_with_shadow
from PIL import ImageDraw, ImageFont

def draw_name(
        template: ImageDraw.ImageDraw,
        name: str,
        x: int,
        y: int,
        font: ImageFont.FreeTypeFont,
        anchor: str = "la"
) -> bool:
    
    draw_text_with_shadow(template, (x, y), name, font, anchor=anchor)
    return True