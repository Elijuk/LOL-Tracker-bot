# fetch all images from ddragons
# ========== Imports ==========
import aiohttp
from PIL import Image, ImageDraw
from io import BytesIO
from typing import Optional
import os

VERSION = "16.3.1"

DRAGON_URL = "https://ddragon.leagueoflegends.com/cdn/"
RANK_ICON_URL = "https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-emblem/emblem-"

PERK_DATA_URL = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json"      # rune database. contains id, name, iconPath
SPELL_DATA_URL = f"https://ddragon.leagueoflegends.com/cdn/{VERSION}/data/en_US/summoner.json"

PERK_ICON_BASE = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default"
CACHE_DIR = "rendering/assets/cache/"


STYLE_ICON_MAP = {
    8000: "7201_precision.png",
    8100: "7200_domination.png",
    8200: "7202_sorcery.png",
    8300: "7203_whimsy.png",
    8400: "7204_resolve.png"
}


# global cache for perk data
perk_lookup: dict[int, str] = {}
spell_lookup: dict[int, str] = {}

"""
1. Fetch: raw bytes. discord nor pillow can read.
2. Wrap in BytesIO. discord and pillow can read
3. Open with pillow -> converts to PIL object
4. Save back to BytesIO. discord and pillow can read.
5. Discord has its own type. Use function."""

"""TODO: fix linux"""

async def _fetch_image(
        url_to_fetch: str,
        session: aiohttp.ClientSession
) -> Optional[BytesIO]:
    async with session.get(url_to_fetch) as response:
        if response.status == 200:
            data = await response.read()
            return BytesIO(data)
    return None
    

def _check_cache(identity: str | int, category: str) -> Optional[Image.Image]:
    if os.path.exists(CACHE_DIR + f"{category}_icons/{identity}.png"):
        return Image.open(CACHE_DIR + f"{category}_icons/{identity}.png").convert("RGBA")
    return None


async def get_spell_map(session: aiohttp.ClientSession) -> dict[int, str]:
    global spell_lookup
    if spell_lookup:
        return spell_lookup
    
    async with session.get(SPELL_DATA_URL) as response:
        if response.status != 200:
            return {}
        data = await response.json()

    for spell in data["data"].values():
        spell_key = int(spell["key"])
        spell_name = spell["id"]

        spell_lookup[spell_key] = spell_name
    
    return spell_lookup


async def get_rune_map(session: aiohttp.ClientSession) -> dict[int, str]:
    """Fetch and cache rune data once."""
    global perk_lookup
    if perk_lookup:
        return perk_lookup

    async with session.get(PERK_DATA_URL) as response:
        if response.status != 200:
            return {}
        data = await response.json()

    # build lookup dictionary (1. rune icons)
    for rune in data:
        rune_id = rune["id"]
        icon_path = rune["iconPath"].replace("/lol-game-data/assets", "").lower()   # remove  /lol-game-data/assets, C-Dragons doesn't need it
        perk_lookup[rune_id] = PERK_ICON_BASE + icon_path
    
    # build lookup dictionary (2. style icons (e.g. domination))
    for style_id_riot, filename_website in STYLE_ICON_MAP.items():
        perk_lookup[style_id_riot] = PERK_ICON_BASE + f"/v1/perk-images/styles/{filename_website}"

    return perk_lookup


async def get_image(identity: str | int,
                    category: str,
                    session: aiohttp.ClientSession
            ) -> Optional[Image.Image]:
    # identity = Ahri, DrMundo, 4132, Exhaust, ...
    # category = champion, item, rune, spell, rank (passed by user)

    cached = _check_cache(identity, category)
    if cached:
        return cached
    
    original_identity = identity

    print(f"not cached: {category}, {identity}")
    if category == "rank":
        url = RANK_ICON_URL + f"{identity}.png"

    elif category == "rune":
        lookup = await get_rune_map(session)     # we manually added correct links for styles
        if not lookup:
            return None
        
        url = lookup.get(int(identity))
        if not url:
            return None
            
    else:
        if category == "spell":
            identity = (await get_spell_map(session))[int(identity)]


        url = DRAGON_URL + f"{VERSION}/img/{category}/{identity}.png"
    
    img_bytes = await _fetch_image(url, session)
    if img_bytes is None:
        return None
    
    img = Image.open(img_bytes).convert("RGBA")
    img.save(CACHE_DIR + f"{category}_icons/{original_identity}.png")

    return img