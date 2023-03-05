from discord.ext import commands
from database.database import createserver, deleteserver


class guildfunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await createserver(guild.id, self.bot.user.name, guild.name)  # Creates server row in database

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await deleteserver(guild.id, self.bot.user.name)  # Deletes server row in database.


async def setup(bot):
    await bot.add_cog(guildfunctions(bot))