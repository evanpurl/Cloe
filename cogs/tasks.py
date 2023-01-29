import discord
from discord.ext import tasks
from discord.ext import commands
from website.updatesite import update_wordpress_post
import time, datetime

starttime = 0.0

class runningtasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        global starttime
        starttime = time.time()  # Get time in seconds at start
        self.status_message.start()

    @tasks.loop(minutes=1)
    async def status_message(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                               name=f"Uptime: {datetime.timedelta(seconds=round(time.time() - starttime))}"))
        await update_wordpress_post()

    @status_message.before_loop
    async def status_beforeloop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(runningtasks(bot))