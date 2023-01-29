import asyncio
import os
import time, datetime
import discord
from discord.ext import commands, tasks
from database.database import gettoken
from database.testdbconnection import connect


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

starttime = 0.0

client = commands.Bot(command_prefix="$", intents=intents)

@client.event
async def on_ready():
    await client.wait_until_ready()
    global starttime
    starttime = time.time()  # Get time in seconds at start
    if not status_message.is_running():
        status_message.start()
    print(f'We have logged in as {client.user}')



@tasks.loop(minutes=1)
async def status_message():
    try:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name=f"Uptime: {datetime.timedelta(seconds=round(time.time() - starttime))}"))
    except Exception as e:
        print(e)

@status_message.before_loop
async def status_beforeloop():
    await client.wait_until_ready()

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

asyncio.run(main())  # Runs main function above