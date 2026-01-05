# cogs/music.py
import discord
from discord.ext import commands
import asyncio
from cogs.utils import search_youtube
import json

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.loop = {}

    async def ensure_guild_queue(self, guild_id):
        if guild_id not in self.queue:
            self.queue[guild_id] = []
            self.loop[guild_id] = {'song': False, 'queue': False}

    @commands.command()
    async def play(self, ctx, *, query):
        await self.ensure_guild_queue(ctx.guild.id)
        song = await search_youtube(query)
        self.queue[ctx.guild.id].append(song)
        await ctx.send(f"Added **{song['title']}** to the queue!")

        # Auto-play if not already playing
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await self.start_playback(ctx)

    async def start_playback(self, ctx):
        guild_id = ctx.guild.id
        while self.queue[guild_id]:
            song = self.queue[guild_id][0]
            if not ctx.voice_client:
                await ctx.author.voice.channel.connect()
            ctx.voice_client.stop()
            ctx.voice_client.play(discord.FFmpegPCMAudio(song['url']),
                                  after=lambda e: self.bot.loop.create_task(self.after_song(ctx)))
            await ctx.send(f"🎵 Now playing: **{song['title']}**")
            break

    async def after_song(self, ctx):
        guild_id = ctx.guild.id
        if self.loop[guild_id]['song']:
            # Repeat same song
            await self.start_playback(ctx)
        else:
            if not self.loop[guild_id]['queue']:
                self.queue[guild_id].pop(0)
            if self.queue[guild_id]:
                await self.start_playback(ctx)

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸ Paused the song!")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶ Resumed the song!")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭ Skipped the song!")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            self.queue[ctx.guild.id] = []
            ctx.voice_client.stop()
            await ctx.send("⏹ Stopped playback and cleared the queue!")

    @commands.command()
    async def queue_list(self, ctx):
        await self.ensure_guild_queue(ctx.guild.id)
        if not self.queue[ctx.guild.id]:
            await ctx.send("Queue is empty!")
        else:
            msg = "🎶 **Queue:**\n"
            for i, song in enumerate(self.queue[ctx.guild.id]):
                msg += f"{i+1}. {song['title']}\n"
            await ctx.send(msg)

    @commands.command()
    async def loop_song(self, ctx):
        self.loop[ctx.guild.id]['song'] = not self.loop[ctx.guild.id]['song']
        await ctx.send(f"🔁 Loop song: {self.loop[ctx.guild.id]['song']}")

    @commands.command()
    async def loop_queue(self, ctx):
        self.loop[ctx.guild.id]['queue'] = not self.loop[ctx.guild.id]['queue']
        await ctx.send(f"🔂 Loop queue: {self.loop[ctx.guild.id]['queue']}")
