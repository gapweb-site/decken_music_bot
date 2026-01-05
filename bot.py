# bot.py
import discord
from discord.ext import commands
import os
from keep_alive import start_server
import asyncio

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Load cogs
bot.load_extension("cogs.music")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Start self-ping server
asyncio.create_task(start_server())

# Run bot
bot.run(os.environ['DISCORD_BOT_TOKEN'])
