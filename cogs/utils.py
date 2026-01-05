# cogs/utils.py
import yt_dlp
import asyncio

# Search YouTube and return direct URL
async def search_youtube(query):
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        return {'url': info['url'], 'title': info['title']}
