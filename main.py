import asyncio
import os
import subprocess
import sys


def install_requirements():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    if os.path.exists('requirements.txt'):
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])


install_requirements()

import discord
from util.load_extensions import load_extensions  # Our code
from discord.ext import commands
from database.database import gettoken  # Our code
from database.testdbconnection import connect  # Our code

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents)


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
