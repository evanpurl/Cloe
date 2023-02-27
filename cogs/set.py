import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import MissingPermissions

from util.dbsetget import dbset


class setcmd(commands.GroupCog, name="set"):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="welcomechannel", description="Admin command to set configuration options.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def welcomechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "welcomechannelid", channel.id)
            await interaction.response.send_message(f"Your welcome channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="defaultrole", description="Slash command for setting your server's Default role.")
    async def defaultrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "defaultroleid", role.id)
            await interaction.response.send_message(
                content=f"""You server's default role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="pingrole", description="Admin command to set ping role")
    async def pingrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "pingroleid", role.id)
            await interaction.response.send_message(content=f"""Ping role has been set to {role.name}""",
                                                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


    @welcomechannel.error
    @defaultrole.error
    @pingrole.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(setcmd(bot))