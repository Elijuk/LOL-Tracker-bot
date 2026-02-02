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
    MY_GUILD = discord.Object(id=1461904966212911297)
    tree.copy_global_to(guild=MY_GUILD)
    await tree.sync(guild=MY_GUILD)

client.run(token)