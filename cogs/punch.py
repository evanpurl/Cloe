import discord
from discord import app_commands
from discord.ext import commands


class punchcmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="punch", description="Command to get punched")
    async def pat(self, interaction: discord.Interaction, user: discord.User = None):
        try:
            if user is None:
                await interaction.response.send_message(content=f"""{self.bot.user.name} punches you 👊""", ephemeral=True)
            else:
                if user.id == self.bot.user.id:
                    await interaction.response.send_message(content=f"""I can't punch myself, duh.""", ephemeral=True)
                else:
                    await interaction.response.send_message(content=f"""{self.bot.user.name} punches {user.mention} 👊""")
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


async def setup(bot):
    await bot.add_cog(punchcmd(bot))
