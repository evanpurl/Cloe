import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from database.database import getmodrole


class admincommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Slash command for Purging a channel.")
    async def self(self, interaction: discord.Interaction, channel: discord.TextChannel, number: int):
        try:
            if number > 50:
                await interaction.response.send_message(
                    content=f"""Cannot purge more than 50 messages at a time.""",
                    ephemeral=True)
            else:
                modr = await getmodrole(interaction.guild.id)
                modrole = discord.utils.get(interaction.guild.roles, id=modr[0])
                if modrole in interaction.user.roles:
                    await interaction.response.defer(ephemeral=True)
                    messages = channel.history(limit=number)
                    async for a in messages:
                        await a.delete()
                        await asyncio.sleep(3)
                    await interaction.followup.send(f"Deleted {number} message(s)")
                else:
                    await interaction.response.send_message(
                        content=f"""You don't have proper permissions to run this command.""",
                        ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


async def setup(bot):
    await bot.add_cog(admincommands(bot))