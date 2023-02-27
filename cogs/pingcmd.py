import discord
from discord import app_commands
from discord.ext import commands
from util.dbsetget import dbget, dbset


class pingcmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Slash command to add people to the Ping role.")
    async def ping(self, interaction: discord.Interaction):
        try:
            prole = await dbget(interaction.guild.id, self.bot.user.name, "pingroleid")
            role = discord.utils.get(interaction.guild.roles, id=prole[0])
            if role:
                if role in interaction.user.roles:

                    await interaction.response.send_message(
                        content=f"""You're already in the role {role.name}.""",
                        ephemeral=True)
                else:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(
                        content=f"""You have been added to role {role.name}.""",
                        ephemeral=True)
            else:
                await interaction.response.send_message(content=f"""No ping role exists.""",
                                                        ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(content=f"""Unable to set your role, make sure my role is higher than the role you're trying to add!""",
                                                    ephemeral=True)



async def setup(bot):
    await bot.add_cog(pingcmd(bot))