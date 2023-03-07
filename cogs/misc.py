import discord
from discord import app_commands
from discord.ext import commands

from util.accessutils import whohasaccess
from util.dbsetget import dbsetbotnetwork


class misccommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="version", description="Slash command for Cloe's version.")
    async def version(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            content=f"""{interaction.user.mention}, this is the 2.0 version of Cloe. My features are as follows:
            **Saying hello.** 
            **Welcoming people to the server.**
            **Auto adding people to the 'Player' role.**
            **I'll add to this later.**""",
            ephemeral=True)

    @app_commands.command(name="addbot", description="Command for Purls to add bots to the bot network.")
    async def addbot(self, interaction: discord.Interaction, bot: discord.User, connection: str, owner: discord.User):
        try:
            if await whohasaccess(interaction.user.id):
                await interaction.response.defer(ephemeral=True)
                await dbsetbotnetwork(bot.name, bot.id, connection, owner.id)
                await interaction.response.send_message(content=f"{bot.name} with connection address {connection} and "
                                                                f"owner {owner.name} has been added to the bot "
                                                                f"network.", ephemeral=True)
            else:
                await interaction.response.send_message(content=f"You can't run this command.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(content=f"Something went wrong", ephemeral=True)


async def setup(bot):
    await bot.add_cog(misccommands(bot))