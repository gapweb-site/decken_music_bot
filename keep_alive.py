# keep_alive.py
from aiohttp import web
import asyncio

async def handle(request):
    return web.Response(text="Bot is alive!")

app = web.Application()
app.router.add_get("/", handle)

async def start_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()

asyncio.get_event_loop().run_until_complete(start_server())
asyncio.get_event_loop().run_forever()
