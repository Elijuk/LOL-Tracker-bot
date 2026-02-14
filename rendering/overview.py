# ========== Imports ==========
import os
import asyncio

from PIL import ImageDraw
from io import BytesIO
from rendering.components import ranks, champion, runes, spells
from rendering.core.utils import draw_text_with_shadow
from rendering.core.cache_manager import AssetCache
from riot.extractors import get_participants
from riot.riot_types import MatchData
from riot.services import get_both_ranks_for_puuid
from tracking.models import User
import aiohttp
from rendering.core.constants import RANK_FONT, NAME_FONT, OVERVIEW_TEMPLATE


# ========== Functions ==========
async def generate_overview_image(tracked_user: User, match_data: MatchData, session: aiohttp.ClientSession):
    # Setup
    draw = ImageDraw.Draw(OVERVIEW_TEMPLATE)
    cache = AssetCache()
    
    participants = get_participants(match_data)
    
    # ===== SINGLE LOOP - Collect all data =====
    champions_positions = []
    rune_pairs = []
    spell_pairs = []
    
    for i, participant in enumerate(participants):
        # Calculate common values
        is_right = i >= 5
        row = i - 5 if is_right else i
        champ_x = 1730 if is_right else 109
        champ_y = 139 + row * 190
        name_x = 1730 if is_right else 190
        name_y = 142 + row * 190
        
        # Collect all champions + their positions in a tuple
        champions_positions.append((participant["championName"], champ_x, champ_y))
        
        # Draw names
        draw_text_with_shadow(
            draw,
            (name_x, name_y),
            participant["riotIdGameName"],
            NAME_FONT,
            anchor="ra" if is_right else "la"
        )
        
        #  Collect rune data
        perks = participant["perks"]["styles"]
        styles_map = {style["description"]: style for style in perks}

        primary_rune_id = styles_map["primaryStyle"]["selections"][0]["perk"]
        secondary_style_id = styles_map["subStyle"]["style"]

        center_x = champ_x + 40  # Center of champion icon
        rune_y = champ_y + 85
        rune_pairs.append((primary_rune_id, secondary_style_id, center_x, rune_y))
        
        # Collect spell data
        spell1_id = participant["summoner1Id"]
        spell2_id = participant["summoner2Id"]
        spell_y = 220 + row * 190
        spell_x = 190 if not is_right else (1730 - 30 - 4 - 30)
        spell_pairs.append((spell1_id, spell2_id, spell_x, spell_y))
    
    # DRAW EVERYTHING
    await asyncio.gather(
    champion.draw_multiple_champions(OVERVIEW_TEMPLATE, champions_positions, session, cache),
    runes.draw_multiple_rune_pairs(OVERVIEW_TEMPLATE, rune_pairs, session, cache),
    spells.draw_spell_pairs_batch(OVERVIEW_TEMPLATE, spell_pairs, session, cache)
    )

    # Parallel rank fetching
    rank_tasks = [
        get_both_ranks_for_puuid(p["puuid"], tracked_user.region, session)
        for p in participants
    ]
    all_ranks = await asyncio.gather(*rank_tasks)
    
    # Parallel rank drawing
    rank_badge_tasks = []
    
    for i, (participant, (solo_rank, flex_rank, status)) in enumerate(zip(participants, all_ranks)):
        is_right = i >= 5
        row = i - 5 if is_right else i
        
        # Handle error states
        if status in ["unfetchable", "error"]:
            error_text = "Not Fetchable" if status == "unfetchable" else "Error"
            text_x = 1728 if is_right else 192
            anchor = "ra" if is_right else "la"
            draw_text_with_shadow(draw, (text_x, 168 + row * 190), error_text, RANK_FONT, anchor=anchor)
            draw_text_with_shadow(draw, (text_x, 188 + row * 190), error_text, RANK_FONT, anchor=anchor)
        else:
            # Collect rank drawing tasks
            if is_right:
                rank_badge_tasks.append(ranks.draw_rank_badge_with_text(
                    OVERVIEW_TEMPLATE, draw, solo_rank,
                    1652, 140 + row * 190, 1698, 168 + row * 190,
                    session, cache, RANK_FONT, "ra"
                ))
                rank_badge_tasks.append(ranks.draw_rank_badge_with_text(
                    OVERVIEW_TEMPLATE, draw, flex_rank,
                    1652, 160 + row * 190, 1698, 188 + row * 190,
                    session, cache, RANK_FONT, "ra"
                ))
            else:
                rank_badge_tasks.append(ranks.draw_rank_badge_with_text(
                    OVERVIEW_TEMPLATE, draw, solo_rank,
                    140, 140 + row * 190, 220, 168 + row * 190,
                    session, cache, RANK_FONT
                ))
                rank_badge_tasks.append(ranks.draw_rank_badge_with_text(
                    OVERVIEW_TEMPLATE, draw, flex_rank,
                    140, 160 + row * 190, 220, 188 + row * 190,
                    session, cache, RANK_FONT
                ))
    
    # Draw all rank badges in parallel
    if rank_badge_tasks:
        await asyncio.gather(*rank_badge_tasks)
    
    # Save
    buffer = BytesIO()
    OVERVIEW_TEMPLATE.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer