import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from database.database import getmodrole


class admincommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Admin command for Purging a channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def self(self, interaction: discord.Interaction, number: int):
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


async def setup(bot):
    await bot.add_cog(admincommands(bot))