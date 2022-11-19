import discord
from discord import app_commands
from mysql.connector import Error, MySQLConnection
from python_mysql_dbconfig import read_db_config
from database import getgreeting, getily, getcompliment, createserver, deleteserver, setmodrole, getmodrole, setsupprole, getsupprole
import string
import operator

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

activity = discord.Activity(name='Your every move', type=discord.ActivityType.watching)

syncguild = discord.Object(id=766120148826193942)


def connect():
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
        super().__init__(intents=intents, activity=activity)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        connect()

        print(f"Logged in as {self.user}")


client = Aclient()
tree = app_commands.CommandTree(client)


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
    createserver(guild.id)


@client.event
async def on_guild_remove(guild):
    deleteserver(guild.id)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if any(substring in message.content.lower() for substring in ["cloe"]):  # Trigger word
        response = getgreeting(
            message.content.lower().replace('cloe', '').translate(str.maketrans('', '', string.punctuation)))
        ily = getily(message.content.lower().replace('cloe', '').translate(str.maketrans('', '', string.punctuation)))
        compliment = getcompliment(
            message.content.lower().replace('cloe', '').translate(str.maketrans('', '', string.punctuation)))
        if response:
            await message.channel.send(f"{response} {message.author.name}!")
        elif ily:
            await message.channel.send(f"{ily} {message.author.name}!")
        elif compliment:
            await message.channel.send(f"{compliment} {message.author.name}!")
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


@tree.command(name="setmodrole", description="Slash command for setting Moderation role.")
@app_commands.checks.has_permissions(administrator=True)
async def self(interaction: discord.Interaction, role: discord.Role):
    try:
        setmodrole(role.id, interaction.guild.id)
        await interaction.response.send_message(
            content=f"Mod role has been set to {role.name}",
            ephemeral=True)
    except Exception as e:
        print(e)


@tree.command(name="setsupporter", description="Slash command for setting supporter role.")
async def self(interaction: discord.Interaction, role: discord.Role):
    try:
        modrole = discord.utils.get(interaction.guild.roles, id=getmodrole(interaction.guild.id)[0])
        if modrole in interaction.user.roles:
            setsupprole(role.id, interaction.guild.id)
            await interaction.response.send_message(
                content=f"Supporter role has been set to {role.name}",
                ephemeral=True)
        else:
            await interaction.response.send_message(
                content=f"""You don't have proper permissions to run this command.""",
                ephemeral=True)
    except Exception as e:
        print(e)


@tree.command(name="supporter", description="Slash command to add people to the supporter role.")
async def self(interaction: discord.Interaction, user: discord.User):
    try:
        modrole = discord.utils.get(interaction.guild.roles, id=getmodrole(interaction.guild.id)[0])
        if modrole in interaction.user.roles:
            role = discord.utils.get(interaction.guild.roles, id=getsupprole(interaction.guild.id)[0])
            if role:
                if role in user.roles:

                    await interaction.response.send_message(content=f"""{user.name} already has the role {role.name}.""",
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
        modrole = discord.utils.get(interaction.guild.roles, id=getmodrole(interaction.guild.id)[0])
        if modrole in interaction.user.roles:
            role = discord.utils.get(interaction.guild.roles, id=getsupprole(interaction.guild.id)[0])
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


def grabtoken():
    token = open('stuff/token/token.txt', 'r')
    if token:
        print('Token grabbed, Staring bot.')
        client.run(token.read())


grabtoken()
