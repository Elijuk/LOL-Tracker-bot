from typing import List, Tuple
import aiohttp
from PIL import Image

from rendering.core.cache_manager import AssetCache, get_image, get_multiple_images
from rendering.core.utils import crop_to_circle
from rendering.core.constants import ImageSizes


async def draw_spell_icon(
        template: Image.Image,
        spell_id: int,
        x: int,
        y: int,
        session: aiohttp.ClientSession,
        cache: AssetCache,
        size: int = ImageSizes.SPELL_ICON
) -> bool:
    
    # fetch single spell image
    spell_img = await get_image(spell_id, "spell", session, cache)
    if not spell_img:
        return False
    
    spell_img = spell_img.resize(size, size)
    template.paste(spell_img, (x, y), spell_img)
    return True


async def draw_spell_icon_pair(
        template: Image.Image,
        spell_ids: Tuple[int, int],
        x: int,
        y: int,
        session: aiohttp.ClientSession,
        cache: AssetCache,
        size: int = ImageSizes.SPELL_ICON,
        gap: int = 4
) -> Tuple[bool, bool]:
    
    
    spell_images = await get_multiple_images(
        [(spell_ids[0], "spell"), (spell_ids[1], "spell")],
        session,
        cache
    )

    success = []
    # draw first spell
    if spell_images[0]:
        spell_1_resized = spell_images[0].resize((size, size))
        template.paste(spell_1_resized, (x, y), spell_1_resized)
        success.append(True)
    
    if spell_images[1]:
        spell_2_resized = spell_images[1].resize((size, size))
        template.paste(spell_2_resized, (x + gap, y), spell_2_resized)
        success.append(True)
    
    return tuple(success)
