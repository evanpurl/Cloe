import server
from aiohttp import web
from discord.ext import commands


class ServerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server = server.HTTPServer(
            bot=self.bot,
            host="0.0.0.0",
            port=25565,
        )
        self.bot.loop.create_task(self._start_server())

    async def _start_server(self):
        await self.bot.wait_until_ready()
        await self.server.start()

    @server.add_route(path="/", method="GET", cog="ServerCog")
    async def home(self, request):
        return web.json_response(data={self.bot.user.name: self.bot.user.avatar.url}, status=200)


async def setup(bot):
    await bot.add_cog(ServerCog(bot))
