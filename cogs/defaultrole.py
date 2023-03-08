import datetime

import discord
from discord import app_commands
from discord.ext import commands

from util.dbsetget import dbset

"requires defaultroleid in db"

class defrole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="setdefaultrole", description="Slash command for setting your server's Default role.")
    async def defaultrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "defaultroleid", role.id)
            await interaction.response.send_message(
                content=f"""You server's default role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @defaultrole.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(defrole(bot))
