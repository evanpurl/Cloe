import discord
from discord import app_commands
from discord.ext import commands
from util.sqlitefunctions import create_db, getconfig

"Needs pingroleid column in db"


class pingcmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Slash command to add people to the Ping role.")
    async def ping(self, interaction: discord.Interaction):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            prole = await getconfig(conn, "pingroleid")
            role = discord.utils.get(interaction.guild.roles, id=prole)
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
            await interaction.response.send_message(content=f"""Unable to set your role, make sure my role is higher 
            than the role you're trying to add!""",
                                                    ephemeral=True)

    @ping.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(pingcmd(bot))
