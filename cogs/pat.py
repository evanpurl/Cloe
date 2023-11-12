import discord
from discord import app_commands
from discord.ext import commands


class patcmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pat", description="Command to get patted")
    async def pat(self, interaction: discord.Interaction, user: discord.User = None):
        try:
            if user is None:
                await interaction.response.send_message(content=f"""{self.bot.user.name} pats your head <a:c1o3pet:1102370970460770304>""", ephemeral=True)
            else:
                if user.id == self.bot.user.id:
                    await interaction.response.send_message(content=f"""I can't pet my own head, silly.""", ephemeral=True)
                else:
                    await interaction.response.send_message(content=f"""{self.bot.user.name} pats {user.mention}'s head <a:c1o3pet:1102370970460770304>""")
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


async def setup(bot):
    await bot.add_cog(patcmd(bot))
