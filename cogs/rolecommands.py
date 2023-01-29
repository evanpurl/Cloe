import os

import discord
from discord import app_commands
from discord.ext import commands

from database.database import setmodrole, setauthuser, getmodrole, setsupprole, setplayerrole, getplayerrole, \
    getsupprole, setLeader, getLeader

SEServer = discord.Object(id=955962668756385792)
class rolecommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setmodrole", description="Slash command for setting Moderation role.")
    @app_commands.checks.has_permissions(administrator=True)
    async def self(self, interaction: discord.Interaction, role: discord.Role):
        try:
            await setmodrole(role.id, interaction.guild.id)
            await interaction.response.send_message(
                content=f"Mod role has been set to {role.name}",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="setauthorized", description="Slash command for setting cloe's authorized users.")
    @app_commands.checks.has_permissions(administrator=True)
    async def self(self, interaction: discord.Interaction, user: discord.User):
        try:
            await setauthuser(user.id)
            await interaction.response.send_message(
                content=f"{user.name} has been authorized.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="setsupporter", description="Slash command for setting supporter role.")
    async def self(self, interaction: discord.Interaction, role: discord.Role):
        try:
            modr = await getmodrole(interaction.guild.id)
            modrole = discord.utils.get(interaction.guild.roles, id=modr[0])
            if modrole in interaction.user.roles:
                await setsupprole(role.id, interaction.guild.id)
                await interaction.response.send_message(
                    content=f"Supporter role has been set to {role.name}",
                    ephemeral=True)
            else:
                await interaction.response.send_message(
                    content=f"""You don't have proper permissions to run this command.""",
                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="setplayer", description="Slash command for setting player role.")
    async def self(self, interaction: discord.Interaction, role: discord.Role):
        try:
            modr = await getmodrole(interaction.guild.id)
            modrole = discord.utils.get(interaction.guild.roles, id=modr[0])
            if modrole in interaction.user.roles:
                await setplayerrole(role.id, interaction.guild.id)
                await interaction.response.send_message(
                    content=f"Player role has been set to {role.name}",
                    ephemeral=True)
            else:
                await interaction.response.send_message(
                    content=f"""You don't have proper permissions to run this command.""",
                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="player", description="Slash command to add people to the player role.")
    async def self(self, interaction: discord.Interaction, user: discord.User):
        try:
            modr = await getmodrole(interaction.guild.id)
            modrole = discord.utils.get(interaction.guild.roles, id=modr[0])
            if modrole in interaction.user.roles:
                player = await getplayerrole(interaction.guild.id)
                role = discord.utils.get(interaction.guild.roles, id=player[0])
                if role:
                    if role in user.roles:

                        await interaction.response.send_message(
                            content=f"""{user.name} already has the role {role.name}.""",
                            ephemeral=True)
                    else:
                        await user.add_roles(role)
                        await interaction.response.send_message(
                            content=f"""{user.name} has been added to role {role.name}.""",
                            ephemeral=True)
                else:
                    await interaction.response.send_message(content=f"""Role does not exist.""",
                                                            ephemeral=True)
            else:
                await interaction.response.send_message(
                    content=f"""You don't have proper permissions to run this command.""",
                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="supporter", description="Slash command to add people to the supporter role.")
    async def self(self, interaction: discord.Interaction, user: discord.User):
        try:
            modr = await getmodrole(interaction.guild.id)
            modrole = discord.utils.get(interaction.guild.roles, id=modr[0])
            if modrole in interaction.user.roles:
                supr = await getsupprole(interaction.guild.id)
                role = discord.utils.get(interaction.guild.roles, id=supr[0])
                if role:
                    if role in user.roles:

                        await interaction.response.send_message(
                            content=f"""{user.name} already has the role {role.name}.""",
                            ephemeral=True)
                    else:
                        await user.add_roles(role)
                        await interaction.response.send_message(
                            content=f"""{user.name} has been added to role {role.name}.""",
                            ephemeral=True)
                else:
                    await interaction.response.send_message(content=f"""Role does not exist.""",
                                                            ephemeral=True)
            else:
                await interaction.response.send_message(
                    content=f"""You don't have proper permissions to run this command.""",
                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="remsupporter", description="Slash command to remove people from the supporter role.")
    async def self(self, interaction: discord.Interaction, user: discord.User):
        try:
            modr = await getmodrole(interaction.guild.id)
            modrole = discord.utils.get(interaction.guild.roles, id=modr[0])
            if modrole in interaction.user.roles:
                supr = await getsupprole(interaction.guild.id)
                role = discord.utils.get(interaction.guild.roles, id=supr[0])
                if role:
                    if role in user.roles:
                        await user.remove_roles(role)
                        await interaction.response.send_message(
                            content=f"""{user.name} has been removed from the role {role.name}.""",
                            ephemeral=True)
                    else:
                        await interaction.response.send_message(
                            content=f"""{user.name} does not have the role {role.name}.""",
                            ephemeral=True)
                else:
                    await interaction.response.send_message(content=f"""Role does not exist.""",
                                                            ephemeral=True)
            else:
                await interaction.response.send_message(
                    content=f"""You don't have proper permissions to run this command.""",
                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    # ------------------- SE Section

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.guilds(SEServer)
    @app_commands.command(name="factionlead", description="Slash command to add faction role leader.")
    async def self(self, interaction: discord.Interaction, role: discord.Role, user: discord.User):
        try:
            leadrole = discord.utils.get(interaction.guild.roles, id=role.id)
            if leadrole:
                if leadrole not in user.roles:
                    await user.add_roles(leadrole)
                await setLeader(role.id, user.id)
                await interaction.response.send_message(
                    content=f"""Player __{user.name}__ has been added as a faction lead to faction **{role.name}**""",
                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.guilds(SEServer)
    @app_commands.command(name="factionadd", description="Slash command to add player to faction role")
    async def self(self, interaction: discord.Interaction, user: discord.User):
        try:
            leader = await getLeader(interaction.user.id)
            if leader:
                leadrole = discord.utils.get(interaction.guild.roles, id=leader[0])
                if leadrole not in user.roles:
                    await user.add_roles(leadrole)
                    await interaction.response.send_message(
                        content=f"""Player __{user.name}__ has been added to faction **{leadrole.name}**""",
                        ephemeral=True)
                else:
                    await interaction.response.send_message(
                        content=f"""Player __{user.name}__ is already in faction **{leadrole.name}**""", ephemeral=True)
            else:
                await interaction.response.send_message(
                    content=f"""You don't have proper permissions to run this command.""",
                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.guilds(SEServer)
    @app_commands.command(name="factionremove", description="Slash command to remove players from faction role")
    async def self(self, interaction: discord.Interaction, user: discord.User):
        try:
            leader = await getLeader(interaction.user.id)
            if leader:
                leadrole = discord.utils.get(interaction.guild.roles, id=leader[0])
                if leadrole in user.roles:
                    await user.remove_roles(leadrole)
                    await interaction.response.send_message(
                        content=f"""Player __{user.name}__ has been removed from faction **{leadrole.name}**""",
                        ephemeral=True)
                else:
                    await interaction.response.send_message(
                        content=f"""Player __{user.name}__ is not in faction **{leadrole.name}**""", ephemeral=True)
            else:
                await interaction.response.send_message(
                    content=f"""You don't have proper permissions to run this command.""",
                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

async def setup(bot):
    await bot.add_cog(rolecommands(bot))