import discord
from discord import app_commands
from discord.ext import commands

from util.databasefunctions import create_pool, get
from util.sqlitefunctions import setSEleader, getSEleader, create_db, getconfig

# ----------------------- SE Section


SEServer = discord.Object(id=955962668756385792)  # SE Discord


class SEcommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.guilds(SEServer)
    @app_commands.command(name="factionlead", description="Slash command to add faction role leader.")
    async def factionlead(self, interaction: discord.Interaction, role: discord.Role, user: discord.User):
        try:
            leadrole = discord.utils.get(interaction.guild.roles, id=role.id)
            if leadrole:
                if leadrole not in user.roles:
                    rolewrite = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                    await user.add_roles(leadrole)

                conn = await create_db(f"storage/{interaction.guild.id}/SE.db")
                await setSEleader(conn, [user.id, role.id])
                await interaction.response.send_message(
                    content=f"""Player __{user.name}__ has been added as a faction lead to faction **{role.name}**""",
                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.guilds(SEServer)
    @app_commands.command(name="factionadd", description="Slash command to add player to faction role")
    async def factionadd(self, interaction: discord.Interaction, user: discord.User):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/SE.db")
            leader = await getSEleader(conn, interaction.user.id)
            if leader:
                leadrole = discord.utils.get(interaction.guild.roles, id=leader)
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
    async def factionremove(self, interaction: discord.Interaction, user: discord.User):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/SE.db")
            leader = await getSEleader(conn, interaction.user.id)
            if leader:
                leadrole = discord.utils.get(interaction.guild.roles, id=leader)
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

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.guilds(SEServer)
    @app_commands.command(name="create-faction", description="Slash command to create faction role and channels.")
    async def factioncreate(self, interaction: discord.Interaction, factionname: str):
        try:
            await interaction.response.defer(ephemeral=True)
            pool = await create_pool()
            defrole = await get(pool, f"SELECT defaultroleid FROM {self.bot.user.name} WHERE serverid={interaction.guild.id}")
            role = discord.utils.get(interaction.guild.roles, id=defrole[0])

            faction = await interaction.guild.create_role(name=factionname)

            if role:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
                    role: discord.PermissionOverwrite(read_messages=False, connect=False),
                    faction: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True,
                                                         speak=True)
                }
            else:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
                    faction: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True,
                                                         speak=True)
                }
            category = await interaction.guild.create_category(name=factionname, overwrites=overwrites)
            textchannel = await interaction.guild.create_text_channel(name=f"{factionname}-general", category=category)
            voicechannel = await interaction.guild.create_voice_channel(name=f"{factionname} voice", category=category)

            await interaction.followup.send(
                content=f"""Faction {factionname} role and channels created. {textchannel.mention}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @factioncreate.error
    @factionadd.error
    @factionlead.error
    @factionremove.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(SEcommands(bot))
