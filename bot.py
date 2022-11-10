import discord
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

activity = discord.Activity(name='Your every move', type=discord.ActivityType.watching)

syncguild = discord.Object(id=766120148826193942)


class aclient(discord.Client):

    def __init__(self):
        super().__init__(intents=intents, activity=activity)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"Logged in as {self.user}")


client = aclient()
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
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith(f"hello <@{client.user.id}>"):
        await message.channel.send(f"Hello {message.author.mention}!")

    elif message.content.lower().startswith(f"i love you <@{client.user.id}>") or message.content.lower().startswith(
            f"love you <@{client.user.id}>"):
        await message.channel.send(f"I love you too {message.author.mention}!")


# Slash commands:
@tree.command(name="version", description="Slash command for Cloe's version.")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(
        content=f"""{interaction.user.mention}, this is the 2.0 version of Cloe. My features are as follows:
        **Saying hello.** 
        **Welcoming people to the server.**
        **Auto adding people to the 'Player' role.**""",
        ephemeral=True)


def grabtoken():
    token = open('stuff/token/token.txt', 'r')
    if token:
        print('Token grabbed, Staring bot.')
        client.run(token.read())


grabtoken()
