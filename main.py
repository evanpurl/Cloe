import os
import discord
from discord.ext import commands
from database.database import gettoken
from database.testdbconnection import connect


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


client = commands.Bot(command_prefix="$", intents=intents)

@client.event
async def on_ready():
    await client.wait_until_ready()
    print(f'We have logged in as {client.user}')

# Function used to load extensions into the bot
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            print(f"Loading cog: {filename[:-3]}")
            await client.load_extension(f"cogs.{filename[:-3]}")


# Main function to load extensions and then load bot.
async def main():
    async with client:
        try:
            token = await gettoken("Cloe")
            await connect()
            await load_extensions()
            await client.start(token[0])
        except KeyboardInterrupt:
            pass
