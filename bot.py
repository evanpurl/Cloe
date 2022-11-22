import asyncio

import discord
from discord import app_commands
from discord.ext import tasks
from mysql.connector import Error, MySQLConnection
from python_mysql_dbconfig import read_db_config
from database import getgreeting, getily, getcompliment, createserver, deleteserver, setmodrole, getmodrole, \
    setsupprole, getsupprole, setauthuser, getauthuser
from updatesite import update_wordpress_post
import string
import time
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

starttime = 0.0

syncguild = discord.Object(id=766120148826193942)


def connect():  # Initial DB connection test
    """ Connect to MySQL database """

    db_config = read_db_config()
    conn = None
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connection established.')
        else:
            print('Connection failed.')

    except Error as error:
        print("error")
        print(error)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print('Connection closed.')


class Aclient(discord.Client):

    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        connect()
        global starttime
        starttime = time.time()  # Get time in seconds at start
        status_message.start()  # Start task loop

        print(f"Logged in as {self.user}")


client = Aclient()
tree = app_commands.CommandTree(client)


# Task loop
@tasks.loop(minutes=1)
async def status_message():
    update_wordpress_post()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name=f"Uptime: {datetime.timedelta(seconds=round(time.time() - starttime))}"))


@status_message.before_loop
async def status_beforeloop():
    await client.wait_until_ready()


# End of task loop

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="welcome")
    await channel.send(f"Welcome to the server {member.mention}!")
    role = discord.utils.get(member.guild.roles, name="Player")
    if role:
        await member.add_roles(role)
    else:
        pass


@client.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name="welcome")
    await channel.send(f"Goodbye {member.mention} :(")


@client.event
async def on_guild_join(guild):
    createserver(guild.id)  # Creates server row in database


@client.event
async def on_guild_remove(guild):
    deleteserver(guild.id)  # Deletes server row in database.


@client.event
async def on_message(message):
    if message.author == client.user:  # If message is from itself, do nothing
        return
    if message.author.bot:  # If message is a bot, do nothing
        return
    auth = await getauthuser(message.author.id)
    if auth:
        if any(substring in message.content.lower() for substring in ["cloe"]):  # Trigger word
            response = await getgreeting(
                message.content.lower().replace('cloe', '').translate(str.maketrans('', '', string.punctuation)))
            ily = await getily(message.content.lower().replace('cloe', '').translate(str.maketrans('', '', string.punctuation)))
            compliment = await getcompliment(
                message.content.lower().replace('cloe', '').translate(str.maketrans('', '', string.punctuation)))
            if response:
                await message.reply(f"{response} {message.author.name}!")
            elif ily:
                await message.reply(f"{ily} {message.author.name}!")
            elif compliment:
                await message.reply(f"{compliment} {message.author.name}!")
            await asyncio.sleep(3)
            # elif any(substring in message.content.lower() for substring in ["what can you do", "what do you do",
            # "what are you capable of"]): await message.channel.send( f"Hello {message.author.name}, currently I am able
            # to welcome people to the server, say goodbye to people who leave, auto add people to the player role,
            # and understand basic questions!")


# Slash commands:
@tree.command(name="version", description="Slash command for Cloe's version.")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(
        content=f"""{interaction.user.mention}, this is the 2.0 version of Cloe. My features are as follows:
        **Saying hello.** 
        **Welcoming people to the server.**
        **Auto adding people to the 'Player' role.**""",
        ephemeral=True)


# @tree.command(name="creator", description="Tells you about who created the bot")
# async def self(interaction: discord.Interaction):
#     await interaction.response.send_message(
#         content=f"""{interaction.user.mention}, this is the 2.0 version of Cloe. My features are as follows:
#         **Saying hello.**
#         **Welcoming people to the server.**
#         **Auto adding people to the 'Player' role.**""",
#         ephemeral=True)


@tree.command(name="setmodrole", description="Slash command for setting Moderation role.")
@app_commands.checks.has_permissions(administrator=True)
async def self(interaction: discord.Interaction, role: discord.Role):
    try:
        await setmodrole(role.id, interaction.guild.id)
        await interaction.response.send_message(
            content=f"Mod role has been set to {role.name}",
            ephemeral=True)
    except Exception as e:
        print(e)
        await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


@tree.command(name="setauthorized", description="Slash command for setting cloe's authorized users.")
@app_commands.checks.has_permissions(administrator=True)
async def self(interaction: discord.Interaction, user: discord.User):
    try:
        await setauthuser(user.id)
        await interaction.response.send_message(
            content=f"{user.name} has been authorized.",
            ephemeral=True)
    except Exception as e:
        print(e)
        await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


@tree.command(name="setsupporter", description="Slash command for setting supporter role.")
async def self(interaction: discord.Interaction, role: discord.Role):
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


@tree.command(name="supporter", description="Slash command to add people to the supporter role.")
async def self(interaction: discord.Interaction, user: discord.User):
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


@tree.error
async def on_app_command_error(interaction, error):
    if isinstance(error, app_commands.BotMissingPermissions):
        await interaction.response.send_message(error, ephemeral=True)
    else:
        await interaction.response.send_message(error, ephemeral=True)


@tree.command(name="remsupporter", description="Slash command to remove people from the supporter role.")
async def self(interaction: discord.Interaction, user: discord.User):
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


@tree.command(name="purge", description="Slash command for Purging a channel.")
async def self(interaction: discord.Interaction, channel: discord.TextChannel, number: int):
    try:
        if number > 50:
            await interaction.response.send_message(
                content=f"""Cannot purge more than 50 messages at a time.""",
                ephemeral=True)
        else:
            modr = await getmodrole(interaction.guild.id)
            modrole = discord.utils.get(interaction.guild.roles, id=modr[0])
            if modrole in interaction.user.roles:
                await interaction.response.defer(ephemeral=True)
                messages = channel.history(limit=number)
                async for a in messages:
                    await a.delete()
                    await asyncio.sleep(3)
                await interaction.followup.send(f"Deleted {number} message(s)")
            else:
                await interaction.response.send_message(
                    content=f"""You don't have proper permissions to run this command.""",
                    ephemeral=True)
    except Exception as e:
        print(e)
        await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


# End of slash commands


def grabtoken():
    token = open('stuff/token/token.txt', 'r')
    if token:
        print('Token grabbed, Staring bot.')
        client.run(token.read())


grabtoken()
