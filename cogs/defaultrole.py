import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
from database.database import setplayerrole




class defaultrole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="setdefaultrole", description="Slash command for setting your server's Default role.")
    async def setdefaultrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            await setplayerrole(role.id, interaction.guild.id)
            await interaction.response.send_message(content=f"""You server's default role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @setdefaultrole.error
    async def setdefaultroleerror(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(content=str(error), ephemeral=True)
        else:
            await interaction.response.send_message(content=str(error),
                                                    ephemeral=True)

async def setup(bot):
    await bot.add_cog(defaultrole(bot))