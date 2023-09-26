import discord
from discord import app_commands
from discord.ext import commands
from util.sqlitefunctions import create_db, insertconfig


class setcmd(commands.GroupCog, name="set"):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="welcome-channel", description="Command to set your server's welcome channel.")
    async def welcomechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            await insertconfig(conn, ["welcomechannelid", channel.id])
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
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            await insertconfig(conn, ["goodbyechannelid", channel.id])
            await interaction.response.send_message(
                f"Goodbye Channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="ticket-category", description="Command to set your server's ticket category.")
    async def ticketcategory(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            await insertconfig(conn, ["ticketcategoryid", category.id])
            await interaction.response.send_message(
                f"Ticket Category has been set to {discord.utils.get(interaction.guild.categories, id=category.id)}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="transcript-log-channel",
                          description="Command to set your server's transcript log channel.")
    async def transcriptlogchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            await insertconfig(conn, ["transcriptchannelid", channel.id])
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
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            await insertconfig(conn, ["defaultroleid", role.id])
            await interaction.response.send_message(
                content=f"""Default Role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="verified-role", description="Command for setting your server's Verified role.")
    async def verifiedrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            await insertconfig(conn, ["verifiedroleid", role.id])
            await interaction.response.send_message(
                content=f"""Default Role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @welcomechannel.error
    @goodbyechannel.error
    @transcriptlogchannel.error
    @defaultrole.error
    @ticketcategory.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


class resetcmd(commands.GroupCog, name="reset"):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="welcome-channel", description="Command to reset your server's welcome channel.")
    async def welcomechannel(self, interaction: discord.Interaction):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            await insertconfig(conn, ["welcomechannelid", 0])
            await interaction.response.send_message(
                f"Welcome Channel has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="goodbye-channel", description="Command to reset your server's goodbye channel.")
    async def goodbyechannel(self, interaction: discord.Interaction):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            await insertconfig(conn, ["goodbyechannelid", 0])
            await interaction.response.send_message(
                f"Goodbye Channel has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="ticket-category", description="Command to reset your server's ticket category.")
    async def ticketcategory(self, interaction: discord.Interaction):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            await insertconfig(conn, ["ticketcategoryid", 0])
            await interaction.response.send_message(
                f"Ticket Category has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="transcript-log-channel",
                          description="Command to reset your server's transcript log channel.")
    async def transcriptlogchannel(self, interaction: discord.Interaction):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            await insertconfig(conn, ["transcriptchannelid", 0])
            await interaction.response.send_message(
                f"Transcript log channel has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="default-role", description="Command to reset your server's Default role.")
    async def defaultrole(self, interaction: discord.Interaction):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            await insertconfig(conn, ["defaultroleid", 0])
            await interaction.response.send_message(
                content=f"""Default Role has been reset.""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="verified-role", description="Command to reset your server's Verified role.")
    async def verifiedrole(self, interaction: discord.Interaction):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            await insertconfig(conn, ["defaultroleid", 0])
            await interaction.response.send_message(
                content=f"""Verified Role has been reset.""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @welcomechannel.error
    @goodbyechannel.error
    @transcriptlogchannel.error
    @defaultrole.error
    @ticketcategory.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(setcmd(bot))
    await bot.add_cog(resetcmd(bot))
