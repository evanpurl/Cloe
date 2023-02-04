import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import MissingPermissions

from util.dbsetget import dbset


class welcomechannel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setwelcomechannel", description="Admin command to set the welcome channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def setwelcomechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "welcomechannelid", channel.id)
            await interaction.response.send_message(f"Your welcome channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @setwelcomechannel.error
    async def setwelcomechannelerror(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(content="You don't have permission to use this command.",
                                                    ephemeral=True)


async def setup(bot):
    await bot.add_cog(welcomechannel(bot))