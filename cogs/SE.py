from mysql.connector import MySQLConnection, Error
from database.python_mysql_dbconfig import read_db_config
import discord
from discord import app_commands
from discord.ext import commands


# ----------------------- SE Section

async def getLeader(userid):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()
            sql = f"SELECT roleid from factions where userid=%(userid)s;"
            user_data = {
                'userid': userid,
            }
            c.execute(sql, user_data)
            response = c.fetchone()
            if not response:
                return None
            c.close()
            conn.close()
            return response
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e


async def setLeader(roleid, userid):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"INSERT INTO factions (userid, roleid) VALUES (%(userid)s, %(roleid)s);"
            user_data = {
                'roleid': roleid,
                'userid': userid,
            }
            c.execute(sql, user_data)
            conn.commit()
            c.close()  # Closes Cursor
            conn.close()  # Closes Connection
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e


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
    async def factionadd(self, interaction: discord.Interaction, user: discord.User):
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
    async def factionremove(self, interaction: discord.Interaction, user: discord.User):
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
    await bot.add_cog(SEcommands(bot))
