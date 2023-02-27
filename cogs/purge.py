import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions


class admincommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Admin command for Purging a channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild.id, i.user.id))
    async def purge(self, interaction: discord.Interaction, number: int):
        try:
            if number > 100:
                await interaction.response.send_message(
                    content=f"""Cannot purge more than 100 messages at a time.""",
                    ephemeral=True)
            else:
                await interaction.response.defer(ephemeral=True)
                deleted = await interaction.channel.purge(limit=number)
                await interaction.followup.send(f"Deleted {len(deleted)} message(s)")
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)
    @purge.error
    async def purgeerror(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(content="You don't have permission to use this command.", ephemeral=True)
        elif isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(content=str(error), ephemeral=True)


async def setup(bot):
    await bot.add_cog(admincommands(bot))