# ========== Imports ==========
import discord
from discord import app_commands


# ========== Commands registry ==========
def register_commands(tree):
    @tree.command(name="recent_matches", description="show recent league of legends matches for a gamer")
    async def recent_matches(interaction: discord.Interaction, summoner_name: str, summoner_id: str, region: str):
        await interaction.response.send_message("Sigma boy")
        return
