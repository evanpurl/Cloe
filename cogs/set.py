import discord
from discord import app_commands
from discord.ext import commands

from util.dbsetget import dbset, dbget

botsdiscord = discord.Object(id=1081357638954123276)  # Bots by Purls Discord


class setcmd(commands.GroupCog, name="set"):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="welcome-channel", description="Command to set your server's welcome channel.")
    async def welcomechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "welcomechannelid", channel.id)
            await interaction.response.send_message(
                f"Welcome Channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="goodbye-channel", description="Command to set your server's goodbye channel.")
    async def goodbyechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "goodbyechannelid", channel.id)
            await interaction.response.send_message(
                f"Goodbye Channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="report-category", description="Command to set your server's report category.")
    async def reportcategory(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "categoryid", category.id)
            await interaction.response.send_message(
                f"Report Category has been set to {discord.utils.get(interaction.guild.categories, id=category.id)}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="ping-role", description="Slash command to set the Ping role.")
    async def ping(self, interaction: discord.Interaction, role: discord.Role):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "pingroleid", role.id)
            await interaction.response.send_message(content=f"""Ping Role has been set to {role.name}""",
                                                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="message-log-channel", description="Command to set your server's message log channel.")
    async def msglogchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "messagechannelid", channel.id)
            await interaction.response.send_message(
                f"Message Log Channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="transcript-log-channel",
                          description="Command to set your server's transcript log channel.")
    async def transcriptlogchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "transcriptchannelid", channel.id)
            await interaction.response.send_message(
                f"Transcript Log Channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="default-role", description="Command for setting your server's Default role.")
    async def defaultrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "defaultroleid", role.id)
            await interaction.response.send_message(
                content=f"""Default Role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="verified-role", description="Command used to set the Verified role")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def verifiedrole(self, interaction: discord.Interaction, role: discord.Role) -> None:
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "verifiedroleid", role.id)
            await interaction.response.send_message(content=f"Verified role set to {role.mention}", ephemeral=True)
        except Exception as e:
            print(e)

    @commands.has_permissions(manage_roles=True)
    @app_commands.guilds(botsdiscord)
    @app_commands.command(name="ticket-channel", description="Command used by admin to set the ticket log channel.")
    async def setticketchannel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "ticketchannelid", channel.id)
            await interaction.response.send_message(
                f"Your ticket log channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.",
                ephemeral=True)

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
    await bot.add_cog(setcmd(bot))
