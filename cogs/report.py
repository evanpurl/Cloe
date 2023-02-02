import discord
from discord import app_commands
from discord.ext import commands


# Needs "manage role" perms

class reportcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="report", description="Command used by members to report people")
    @app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild.id, i.user.id))
    async def report(self, interaction: discord.Interaction, user: discord.User) -> None:
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True)}

        reportcat = discord.utils.get(interaction.guild.categories, name="Reports")
        if reportcat:
            reportchan = await interaction.guild.create_text_channel(f"Report number", category=reportcat, overwrites=overwrites, reason=f"User {interaction.user.name} reported {user.name}")
            await interaction.response.send_message(content=f"Report created in {reportchan.mention}", ephemeral=True)
            await reportchan.send(content=f"{interaction.user.mention} reported {user.name}. Please lay out any evidence you have here!")

        else:
            reportchan = await interaction.guild.create_text_channel(f"Report number", overwrites=overwrites, reason=f"User {interaction.user.name} reported {user.name}")
            await interaction.response.send_message(content=f"Report created in {reportchan.mention}", ephemeral=True)
            await reportchan.send(content=f"{interaction.user.mention} reported {user.name}. Please lay out any evidence you have here!")

    @report.error
    async def reporterror(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(content=str(error), ephemeral=True)


async def setup(bot):
    await bot.add_cog(reportcmd(bot))
