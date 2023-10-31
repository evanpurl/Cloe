import discord
from discord.ext import commands


class bcommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="sync", description="Command to sync slash commands")
    async def reload(self, ctx) -> None:
        tagged = ctx.message.mentions
        if tagged[0].id == self.bot.user.id:
            print(f"Syncing commands")
            await self.bot.tree.sync()
            await self.bot.tree.sync(guild=discord.Object(id=1081357638954123276))
            await ctx.send(f"Commands synced")
            print(f"Commands synced")

    @reload.error
    async def onerror(self, interaction: discord.Interaction, error: commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(bcommands(bot))
