import os

from discord.ext import commands
from util.accessutils import whohasaccess
class cloecommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cloereload", description="Command to reload cogs")
    async def reload(self, ctx) -> None:
        if await whohasaccess(ctx.message.author.id):
            print(f"Syncing commands")
            await self.bot.tree.sync()
            await ctx.send(f"Commands synced")
            print(f"Commands synced")
        else:
            await ctx.send(f"You can't run this command.")

async def setup(bot):
    await bot.add_cog(cloecommands(bot))