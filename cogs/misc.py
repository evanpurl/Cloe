import discord
from discord import app_commands
from discord.ext import commands


class misccommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="version", description="Slash command for Cloe's version.")
    async def version(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            content=f"""{interaction.user.mention}, this is the 2.0 version of Cloe. My features are as follows:
            **Saying hello.** 
            **Welcoming people to the server.**
            **Auto adding people to the 'Player' role.**
            **I'll add to this later.**""",
            ephemeral=True)

    @app_commands.command(name="site", description="Slash command for Cloe's website page.")
    async def site(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            content=f"https://www.nitelifesoftware.com/bots/cloe",
            ephemeral=True)


async def setup(bot):
    await bot.add_cog(misccommands(bot))