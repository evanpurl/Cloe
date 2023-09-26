import os

from discord.ext import commands
from util.load_data import loadserverdata


class guildfunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await loadserverdata(guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        if os.path.exists(f"storage/{guild.id}"):
            os.remove(f"storage/{guild.id}")


async def setup(bot):
    await bot.add_cog(guildfunctions(bot))
