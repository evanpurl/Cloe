import os

from discord.ext import commands
from util.accessutils import whohasaccess


class cloecommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cloereload", description="command to reload cogs")
    async def reload(self, ctx) -> None:
        if str(ctx.message.author.id) in await whohasaccess():
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    await ctx.send(f"reloading cog: {filename[:-3]}")
                    print(f"reloading cog: {filename[:-3]}")
                    await self.bot.reload_extension(f"cogs.{filename[:-3]}")
            await ctx.send(f"Syncing commands")
            print(f"Syncing commands")
            await self.bot.tree.sync()
            await ctx.send(f"Commands synced")
            print(f"Commands synced")
        else:
            await ctx.send(f"You can't run this command.")

async def setup(bot):
    await bot.add_cog(cloecommands(bot))