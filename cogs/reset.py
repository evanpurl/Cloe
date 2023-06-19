import discord
from discord import app_commands
from discord.ext import commands

from util.dbsetget import dbset, dbget

botsdiscord = discord.Object(id=1081357638954123276)  # Bots by Purls Discord

class resetcmd(commands.GroupCog, name="reset"):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="welcome-channel", description="Command to set your server's welcome channel.")
    async def welcomechannel(self, interaction: discord.Interaction):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "welcomechannelid", 0)
            await interaction.response.send_message(
                f"Welcome Channel has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="report-category", description="Command to set your server's report category.")
    async def reportcategory(self, interaction: discord.Interaction):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "categoryid", 0)
            await interaction.response.send_message(
                f"Report Category has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="ping-role", description="Slash command to set the Ping role.")
    async def ping(self, interaction: discord.Interaction):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "pingroleid", 0)
            await interaction.response.send_message(content=f"""Ping role has been reset.""",
                                                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="message-log-channel", description="Command to reset your server's message log channel.")
    async def msglogchannel(self, interaction: discord.Interaction):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "messagechannelid", 0)
            await interaction.response.send_message(
                f"Message log channel has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="transcript-log-channel",
                          description="Command to reset your server's transcript log channel.")
    async def transcriptlogchannel(self, interaction: discord.Interaction):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "transcriptchannelid", 0)
            await interaction.response.send_message(
                f"Transcript log channel has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="default-role", description="Command for resetting your server's Default role.")
    async def defaultrole(self, interaction: discord.Interaction):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "defaultroleid", 0)
            await interaction.response.send_message(
                content=f"""Default Role has been reset.""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="verified-role", description="Command used to reset your server's Verified role")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def verifiedrole(self, interaction: discord.Interaction):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "verifiedroleid", 0)
            await interaction.response.send_message(content=f"Verified role has been reset.", ephemeral=True)
        except Exception as e:
            print(e)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.guilds(botsdiscord)
    @app_commands.command(name="ticket-channel",
                          description="Command used by admin to reset the ticket log channel.")
    async def resetmessagechannel(self, interaction: discord.Interaction):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "ticketchannelid", 0)
            await interaction.response.send_message(f"Ticket log channel config has been reset.", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @welcomechannel.error
    @reportcategory.error
    @ping.error
    @msglogchannel.error
    @transcriptlogchannel.error
    @defaultrole.error
    @verifiedrole.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(resetcmd(bot))
