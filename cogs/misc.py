import discord
from discord import app_commands
from discord.ext import commands


class misccommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="version", description="Slash command for Cloe's version.")
    async def version(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            content=f"""{interaction.user.mention}, this is the 2.1.5 version of Cloe. You can find my list of features here: https://bots.botsbypurls.com/C1o3.html
                    Discord: https://discord.gg/g8UbZ95QZh""",
            ephemeral=True)


async def setup(bot):
    await bot.add_cog(misccommands(bot))