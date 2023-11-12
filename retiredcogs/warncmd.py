import discord
from discord import app_commands
from discord.ext import commands


# Needs "manage role" perms

class warncmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="warn", description="Command used by a moderator or admin to warn people.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, user: discord.User, reason: str) -> None:
        msg = f"""You have been warned on __{interaction.guild.name}__ for reason **{reason}**. Please contact an 
admin if you have any questions. """
        await user.send(msg)
        await interaction.response.send_message(content=f"Warning sent to user __{user.name}__ for reason **{reason}**", ephemeral=True)


async def setup(bot):
    await bot.add_cog(warncmd(bot))
