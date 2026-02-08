# ========== Imports ==========
import discord
from typing import Optional

from riot.riot_types import MatchData
from rendering.overview import generate_overview_image
from tracking.models import User


# ========== Function ==========
async def generate_image(
        image_type: str,
        tracked_user: User,
        match_data: MatchData
) -> Optional[discord.File]:

    if image_type == "overview":
        image_buffer = generate_overview_image()
        discord_file = discord.File(fp=image_buffer, filename=f"overview_{tracked_user.recent_match}.png")
        return discord_file
    
    return None

