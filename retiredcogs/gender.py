import discord
from discord import app_commands
from discord.ext import commands


# Needs "manage role" perms

class gendercmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="gender", description="Command used to assign someone to a role for their gender.")
    @app_commands.choices(genders=[
        app_commands.Choice(name='Male', value=1),
        app_commands.Choice(name='Female', value=2),
        app_commands.Choice(name='Non-Binary', value=3),
        app_commands.Choice(name='Genderfluid', value=4),
        app_commands.Choice(name='Demigirl', value=5),
        app_commands.Choice(name='Demiboy', value=6),
    ])
    async def gender(self, interaction: discord.Interaction, genders: app_commands.Choice[int]) -> None:
        try:
            role = discord.utils.get(interaction.guild.roles, name=genders.name)
            if not role:
                await interaction.guild.create_role(name=genders.name)
            role = discord.utils.get(interaction.guild.roles, name=genders.name)
            if role:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"You have been added to the {genders.name} role.", ephemeral=True)
            else:
                await interaction.response.send_message(f"This bot cannot run this function at this time.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                content=f"""Unable to set your role, make sure my role is higher than the role you're trying to add!""",
                ephemeral=True)


async def setup(bot):
    await bot.add_cog(gendercmd(bot))
