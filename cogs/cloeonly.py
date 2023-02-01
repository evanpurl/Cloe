import discord
from discord import app_commands
from discord.ext import commands
from database.database import setauthuser


class cloeonly(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="setauthorized", description="Slash command for setting cloe's authorized users.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setauthorized(self, interaction: discord.Interaction, user: discord.User):
        try:
            await setauthuser(user.id)
            await interaction.response.send_message(
                content=f"{user.name} has been authorized.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


async def setup(bot):
    await bot.add_cog(cloeonly(bot))