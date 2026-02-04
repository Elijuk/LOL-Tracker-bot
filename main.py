# ========== Imports ==========
import os
import dotenv
import discord

from discord import app_commands
from commands.commands import register_commands
from commands.errors import register_errors


# ========== Setup ==========
dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)
register_commands(tree)
register_errors(tree)


# ========== Startup ==========
token = os.getenv("DISCORD_TOKEN")
if token is None:
    raise RuntimeError("DISCORD_TOKEN environment variable not set")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    # sync with test server
    MY_GUILD = discord.Object(id=1461904966212911297)
    tree.copy_global_to(guild=MY_GUILD)
    await tree.sync(guild=MY_GUILD)

    # sync all joined guilds
    async for guild in client.fetch_guilds():
        """TODO: CHECK IF GUILD.ID AL ERIN ZIT """


@client.event
async def on_guild_join(guild: discord.Guild):
    """TODO: CALL FUNCTION TO ADD THIS GUILD ID"""
    # update_config(guild.id)

@client.event
async def on_guild_leave(guild: discord.Guild):
    """TODO: CALL FUNCTION TO REMOVE THIS GUILD"""
    # update_config(guild_id)

client.run(token)