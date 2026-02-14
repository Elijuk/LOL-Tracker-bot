from typing import Optional, Tuple
import aiohttp
from PIL import Image, ImageDraw, ImageFont

from rendering.core.cache_manager import AssetCache, get_image
from rendering.core.constants import RANK_LABELS, ImageSizes, COLORS
from rendering.core.utils import draw_text_with_shadow
from riot.riot_types import RankData

def format_rank_text(rank_data: RankData) -> str:
    """
    Format rank data into display text.
    
    Args:
        rank_data: Rank dictionary with 'tier', 'rank', 'leaguePoints'
    
    Returns:
        Formatted string ("G2 · 45LP")
    """
    tier = rank_data.get("tier", "")
    rank_label = rank_data.get("rank", "")
    lp = rank_data.get("leaguePoints", "")
    
    tier_abbrev = tier[0] if tier else ""
    rank_num = RANK_LABELS.get(rank_label, "")
    
    return f"{tier_abbrev}{rank_num} · {lp}LP"


async def draw_rank_badge(
    template: Image.Image,
    rank_data: RankData,
    x: int,
    y: int,
    session: aiohttp.ClientSession,
    cache: AssetCache,
    size: Optional[Tuple[int, int]] = None
) -> bool:
    """
    Draw a rank badge icon.
    
    Args:
        template: Image to draw on
        rank_data: Rank dictionary
        x: X position (top-left corner)
        y: Y position (top-left corner)
        session: aiohttp session
        cache: Asset cache instance
        size: Optional (width, height) tuple, defaults to ImageSizes.RANK_ICON
    
    Returns:
        True if badge was drawn, False if unranked or error
    """
    tier = rank_data.get("tier", "").lower()
    if not tier:
        return False
    
    rank_img = await get_image(tier, "rank", session, cache)
    if not rank_img:
        return False
    
    if size is None:
        size = ImageSizes.RANK_ICON
    
    rank_img = rank_img.resize(size)
    template.paste(rank_img, (x, y), rank_img)
    return True

def draw_rank_text(
    draw: ImageDraw.ImageDraw,
    rank_data: RankData,
    x: int,
    y: int,
    font: ImageFont.FreeTypeFont,
    anchor: str = "la",
    unranked_text: str = "Unranked"
) -> None:
    """
    Draw rank text (e.g., "G2 · 45LP" or "Unranked").
    
    Args:
        draw: ImageDraw object
        rank_data: Rank dictionary
        x: X position
        y: Y position
        font: Font to use
        anchor: Text anchor (e.g., "la", "ra")
        unranked_text: Text to show when unranked
    """
    if rank_data:
        text = format_rank_text(rank_data)
        color = COLORS[rank_data["tier"]]
    else:
        text = unranked_text
        color = (255, 255, 255, 255)
    
    draw_text_with_shadow(draw, (x, y), text, font, fill=color, anchor=anchor)


async def draw_rank_badge_with_text(
    template: Image.Image,
    draw: ImageDraw.ImageDraw,
    rank_data: RankData,
    badge_x: int,
    badge_y: int,
    text_x: int,
    text_y: int,
    session: aiohttp.ClientSession,
    cache: AssetCache,
    font: ImageFont.FreeTypeFont,
    text_anchor: str = "la",
    badge_size: Optional[Tuple[int, int]] = None
) -> bool:
    """
    Draw rank badge and text together.
    
    Args:
        template: Image to draw on
        draw: ImageDraw object
        rank_data: Rank dictionary
        badge_x: Badge X position
        badge_y: Badge Y position
        text_x: Text X position
        text_y: Text Y position
        session: aiohttp session
        cache: Asset cache instance
        font: Font for text
        text_anchor: Text anchor
        badge_size: Optional badge size
    
    Returns:
        True if badge was drawn, False if only text
    """
    badge_drawn = await draw_rank_badge(
        template, rank_data, badge_x, badge_y, session, cache, badge_size
    )
    draw_rank_text(draw, rank_data, text_x, text_y, font, text_anchor)
    return badge_drawn