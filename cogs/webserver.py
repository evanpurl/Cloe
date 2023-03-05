import server
from aiohttp import web
from discord.ext import commands


def html_response(document):
    s = open(document, "r")
    return web.Response(text=s.read(), content_type='text/html')


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

    routes = web.RouteTableDef()

    @server.add_route(path="/", method="GET", cog="ServerCog")
    async def home(self, request):
        return html_response('web/index.html')


async def setup(bot):
    await bot.add_cog(ServerCog(bot))
