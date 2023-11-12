import discord
from discord import app_commands
from discord.ext import commands


# Needs "manage role" perms

class pronouncmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pronouns", description="Command used to assign someone to a role for their pronouns.")
    @app_commands.choices(pronouns=[
        app_commands.Choice(name='He/Him', value=1),
        app_commands.Choice(name='She/Her', value=2),
        app_commands.Choice(name='They/Them', value=3),
        app_commands.Choice(name='Something Else', value=4),
    ])
    async def pronouns(self, interaction: discord.Interaction, pronouns: app_commands.Choice[int]) -> None:
        try:
            role = discord.utils.get(interaction.guild.roles, name=pronouns.name)
            if not role:
                await interaction.guild.create_role(name=pronouns.name)
            role = discord.utils.get(interaction.guild.roles, name=pronouns.name)
            if role:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"You have been added to the {pronouns.name} role.", ephemeral=True)
            else:
                await interaction.response.send_message(f"This bot cannot run this function at this time.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                content=f"""Unable to set your role, make sure my role is higher than the role you're trying to add!""",
                ephemeral=True)


async def setup(bot):
    await bot.add_cog(pronouncmd(bot))
