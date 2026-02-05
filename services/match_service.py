"""Connects all 5 layers (see image)"""

# ========== Imports ==========
import discord
from typing import Optional

from riot.api import get_match_data, get_match_id
from riot.extractors import *
from rendering.overview import generate_overview_image
from track_manager.track_data import TrackManager


# ========== Function ==========
async def generate_image(
        discord_id: int,
        guild_id: int,
        tracker: TrackManager,
        image_type: str
) -> Optional[discord.File]:
    
    # 1. TRIGGER LAYER
    # Trigger layer is the command that called this function.

    # 2. IDENTITY LAYER
    guild = tracker.get_guild(guild_id)
    if not guild:
        return None
    
    user = guild.get_member(discord_id)
    if not user:
        return None
    

    # 3. DATA LAYER
    if user.recent_match is None:
        return
    
    match_data = await get_match_data(user.recent_match, user.region)
    if not match_data:
        return None
    
    # 4. INTERPRETATION LAYER
    # We always need to generate an overview
    if image_type == "overview":
        image_buffer = generate_overview_image()
        discord_file = discord.File(fp=image_buffer, filename=f"overview_{user.recent_match}.png")
        return discord_file

