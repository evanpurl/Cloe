import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import MissingPermissions

from util.dbsetget import dbset


# Needs "manage role" perms

class resetcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="reset", description="Command used to reset a config option.")
    @app_commands.choices(config=[
        app_commands.Choice(name='Welcome Channel', value=1),
        app_commands.Choice(name='Default Role', value=2),
        app_commands.Choice(name='Ping Role', value=3),
    ])
    async def reset(self, interaction: discord.Interaction, config: app_commands.Choice[int]) -> None:
        if config.value == 1:
            await dbset(interaction.guild.id, self.bot.user.name, "welcomechannelid", 0)
            await interaction.response.send_message(f"Welcome channel config has been reset.",ephemeral=True)
        elif config.value == 2:
            await dbset(interaction.guild.id, self.bot.user.name, "defaultroleid", 0)
            await interaction.response.send_message(f"Default role config has been reset.", ephemeral=True)
        elif config.value == 3:
            await dbset(interaction.guild.id, self.bot.user.name, "pingroleid", 0)
            await interaction.response.send_message(f"Ping Role config has been reset.", ephemeral=True)

    @reset.error
    async def reseterror(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(content="You need admin permissions to use this command.",
                                                    ephemeral=True)
        else:
            print(error)

async def setup(bot):
    await bot.add_cog(resetcmd(bot))
