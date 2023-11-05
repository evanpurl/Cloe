import asyncio
import os
import discord
from util.load_extensions import load_extensions  # Our code
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents)

load_dotenv()


# Main function to load extensions and then load bot.
async def main():
    async with client:
        try:
            await load_extensions(client)
            await client.start(os.getenv('token'))
        except KeyboardInterrupt:
            pass


asyncio.run(main())  # Runs main function above
