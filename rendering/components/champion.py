from typing import List, Tuple
import aiohttp
from PIL import Image

from rendering.core.cache_manager import AssetCache, get_image, get_multiple_images
from rendering.core.utils import crop_to_circle
from rendering.core.constants import ImageSizes

async def draw_champion(
        template: Image.Image,
        champion_name: str,
        x: int,
        y: int,
        session: aiohttp.ClientSession,
        cache: AssetCache,
        size: int = ImageSizes.CHAMPION_ICON

) -> bool:
    
    # fetch single champ image
    champ_img = await get_image(champion_name, "champion", session, cache)
    if not champ_img:
        return False
    
    champ_img_circle = crop_to_circle(champ_img, size)

    template.paste(champ_img_circle, (x, y), champ_img_circle)
    return True

async def draw_multiple_champions(
    template: Image.Image,
    champions_positions: List[Tuple[str, int, int]],
    session: aiohttp.ClientSession,
    cache: AssetCache,
    size: int = ImageSizes.CHAMPION_ICON,
) -> List[bool]:
    """
    Draw multiple champion icons in parallel.
    
    Args:
        template: Image to draw on
        champions_positions: List of (champion_name, x, y) tuples
        session: aiohttp session
        cache: Asset cache
        size: Icon size
    
    Returns:
        List of booleans indicating success/failure for each
    """
    # Fetch images
    champion_names = [champ for champ, _, _ in champions_positions]
    identity_category: List[Tuple] = [(name, "champion") for name in champion_names]
    champ_imgs = await get_multiple_images(identity_category, session, cache)
    
    # Draw each one at its position
    results = []
    for (champ_name, x, y), champ_img in zip(champions_positions, champ_imgs):
        if not champ_img:
            results.append(False)
            continue
        
        # Crop to circle
        champ_img = crop_to_circle(champ_img, size)

        # Paste
        template.paste(champ_img, (x, y), champ_img)
        results.append(True)
    
    return results


    