import asyncio
import discord
import server
from aiohttp import web

from util.load_extensions import load_extensions  # Our code
from discord.ext import commands
from database.database import gettoken  # Our code
from database.testdbconnection import connect  # Our code

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents)


@client.event
async def on_ready():
    client.server = server.HTTPServer(
        bot=client,
        host="0.0.0.0",
        port="25565",
    )
    await client.server.start()


@server.add_route(path="/", method="GET")
async def home(request):
    return web.json_response(data={"foo": "bar"}, status=200)


# Main function to load extensions and then load bot.
async def main():
    async with client:
        try:
            token = await gettoken("c1o3")
            await connect()  # Tests database connection
            await load_extensions(client)
            await client.start(token[0])
        except KeyboardInterrupt:
            pass


asyncio.run(main())  # Runs main function above
