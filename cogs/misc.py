import discord
from discord import app_commands
from discord.ext import commands


class misccommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="version", description="Slash command for Cloe's version.")
    async def version(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            content=f"""{interaction.user.mention}, this is the 2.4.6 version of Cloe. You can find my list of features here: https://bots.botsbypurls.com/cloe.html
Discord: https://discord.gg/g8UbZ95QZh""",
            ephemeral=True)

    @app_commands.command(name="member_count", description="Gets member count on the current server.")
    async def mcount(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"Current member count in {interaction.guild.name}: {len([m for m in interaction.guild.members if not m.bot])}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(misccommands(bot))