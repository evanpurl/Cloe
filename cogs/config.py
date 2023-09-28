import discord
from discord import app_commands
from discord.ext import commands

from util.databasefunctions import create_pool, insert
from util.sqlitefunctions import create_db, insertconfig


class setcmd(commands.GroupCog, name="set"):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="welcome-channel", description="Command to set your server's welcome channel.")
    async def welcomechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            mysql = f"UPDATE C1o3 SET welcomechannelid = {channel.id}  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                f"Welcome Channel has been set to {channel.mention}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="goodbye-channel", description="Command to set your server's goodbye channel.")
    async def goodbyechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            mysql = f"UPDATE C1o3 SET goodbyechannelid = {channel.id}  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                f"Goodbye Channel has been set to {channel.mention}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="ticket-category", description="Command to set your server's ticket category.")
    async def ticketcategory(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        try:
            mysql = f"UPDATE C1o3 SET ticketcategoryid = {category.id}  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                f"Ticket Category has been set to {category.mention}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="transcript-log-channel",
                          description="Command to set your server's transcript log channel.")
    async def transcriptlogchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            mysql = f"UPDATE C1o3 SET transcriptchannelid = {channel.id}  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                f"Transcript Log Channel has been set to {channel.mention}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="message-log-channel",
                          description="Command to set your server's message log channel.")
    async def messagelogchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            mysql = f"UPDATE C1o3 SET messagechannelid = {channel.id}  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                f"Message Log Channel has been set to {channel.mention}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="default-role", description="Command for setting your server's Default role.")
    async def defaultrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            mysql = f"UPDATE C1o3 SET defaultroleid = {role.id}  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                content=f"""Default Role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="verified-role", description="Command for setting your server's Verified role.")
    async def verifiedrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            mysql = f"UPDATE C1o3 SET verifiedroleid = {role.id}  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                content=f"""Default Role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="ping-role", description="Command for setting your server's Ping role.")
    async def pingrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            mysql = f"UPDATE C1o3 SET pingroleid = {role.id}  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                content=f"""Ping Role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @welcomechannel.error
    @goodbyechannel.error
    @transcriptlogchannel.error
    @defaultrole.error
    @ticketcategory.error
    @pingrole.error
    @messagelogchannel.error
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
            mysql = f"UPDATE C1o3 SET welcomechannelid = 0  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
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
            mysql = f"UPDATE C1o3 SET goodbyechannelid = 0  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
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
            mysql = f"UPDATE C1o3 SET ticketcategoryid = 0  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
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
            mysql = f"UPDATE C1o3 SET transcriptchannelid = 0  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                f"Transcript log channel has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="message-log-channel",
                          description="Command to reset your server's message log channel.")
    async def messagelogchannel(self, interaction: discord.Interaction):
        try:
            mysql = f"UPDATE C1o3 SET messagechannelid = 0  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                f"Message log channel has been reset.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="default-role", description="Command to reset your server's Default role.")
    async def defaultrole(self, interaction: discord.Interaction):
        try:
            mysql = f"UPDATE C1o3 SET defaultroleid = 0  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                content=f"""Default Role has been reset.""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="verified-role", description="Command to reset your server's Verified role.")
    async def verifiedrole(self, interaction: discord.Interaction):
        try:
            mysql = f"UPDATE C1o3 SET verifiedroleid = 0  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                content=f"""Verified Role has been reset.""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="ping-role", description="Command to reset your server's Ping role.")
    async def pingrole(self, interaction: discord.Interaction):
        try:
            mysql = f"UPDATE C1o3 SET pingroleid = 0  WHERE serverid = {interaction.guild.id};"
            pool = await create_pool()
            await insert(pool, mysql)
            await interaction.response.send_message(
                content=f"""Ping Role has been reset.""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @welcomechannel.error
    @goodbyechannel.error
    @transcriptlogchannel.error
    @defaultrole.error
    @ticketcategory.error
    @pingrole.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(setcmd(bot))
    await bot.add_cog(resetcmd(bot))
