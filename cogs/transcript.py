import io

import discord
from chat_exporter import chat_exporter
from discord import app_commands
from discord.ext import commands


class transcriptcmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="transcript", description="Command to transcript current channel.")
    async def transcript(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            transcript = await chat_exporter.export(
                interaction.channel,
            )
            if transcript is None:
                return

            transcript_file = discord.File(
                io.BytesIO(transcript.encode()),
                filename=f"transcript-{interaction.channel.name}.html",
            )

            await interaction.user.send(file=transcript_file)
            await interaction.followup.send(content="Transcript created.", ephemeral=True)
        except Exception as e:
            print(e)

    @transcript.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(transcriptcmd(bot))
