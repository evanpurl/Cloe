from discord.ext import commands

from util.load_data import loadallservers


class onready(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        print(f"Confirming server data.")
        await loadallservers(self.bot.guilds)
        print(f'We have logged in as {self.bot.user}')


async def setup(bot):
    await bot.add_cog(onready(bot))
