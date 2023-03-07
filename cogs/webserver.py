from aiohttp import web
import asyncio
from discord.ext import commands

host = '0.0.0.0'
port = 25565


class ServerCog(commands.Cog):
    def __init__(self, bot):
        self.site = None
        self.bot = bot

    async def webserver(self):
        async def handler(request):
            if not self.bot.user.avatar:
                pfp = 'nothing.png'
            else:
                pfp = self.bot.user.avatar.url
            return web.json_response(data={self.bot.user.name: pfp}, status=200)

        app = web.Application()
        app.router.add_get('/', handler)
        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, host, port)
        await self.bot.wait_until_ready()
        await self.site.start()
        print(f"Web server has been started at port {port}")

    def __unload(self):
        asyncio.ensure_future(self.site.stop())


async def setup(bot):
    server = ServerCog(bot)
    await bot.add_cog(server)
    bot.loop.create_task(server.webserver())
