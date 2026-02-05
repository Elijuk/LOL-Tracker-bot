# ========== Imports ==========
import os
import dotenv
import discord
from track_manager.track_data import *

DEV_TOKEN = os.getenv("DEV_TOKEN")

# ========== Global ==========
track = TrackManager()


# ========== Functions ==========
def get_guild_from_interaction(interaction: discord.Interaction) -> Optional[Guild]:
    """If the guild_id - where the interaction is being sent from - exists in the database, return its info. Else None.
    """
    if interaction.guild_id is None:
        return None
    return track.get_guild(interaction.guild_id)

def validate_user(interaction: discord.Interaction):
    if DEV_TOKEN:
        return str(interaction.user.id) in DEV_TOKEN
    return False