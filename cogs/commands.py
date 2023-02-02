import os

from discord.ext import commands
from util.accessutils import whohasaccess
class cloecommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cloereload", description="Command to reload cogs")
    async def reload(self, ctx) -> None:
        if await whohasaccess(ctx.message.author.id):
            await ctx.send(f"Reloading Cogs,  Please Wait")
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    print(f"reloading cog: {filename[:-3]}")
                    await self.bot.reload_extension(f"cogs.{filename[:-3]}")
            await ctx.send(f"Cogs Reloaded, Syncing commands")
            print(f"Syncing commands")
            await self.bot.tree.sync()
            await ctx.send(f"Commands synced")
            print(f"Commands synced")
        else:
            await ctx.send(f"You can't run this command.")

    @commands.command(name="cloeload", description="Command to load cogs")
    async def load(self, ctx, extension) -> None:
        if await whohasaccess(ctx.message.author.id):
            await ctx.send(f"Processing Please Wait")
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    if extension == filename[:-3]:
                        await self.bot.load_extension(f"cogs.{filename[:-3]}")
                        await ctx.send(f"Loading {filename[:-3]}")
            await ctx.send(f"Syncing commands")
            print(f"Syncing commands")
            await self.bot.tree.sync()
            await ctx.send(f"Commands synced")
            print(f"Commands synced")
        else:
            await ctx.send(f"You can't run this command.")

async def setup(bot):
    await bot.add_cog(cloecommands(bot))