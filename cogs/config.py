from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from util.dbsetget import dbset, dbget


class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=f"Message Log", description="Toggle Message Log Functionality."),
            discord.SelectOption(label="Report Transcript", description="Toggle Report Transcript Functionality.")
        ]
        super().__init__(placeholder="Select an option", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        try:
            if self.values[0] == "Message Log":
                ison = await dbget(interaction.guild.id, interaction.client.user.name, "ismsglogon")
                if ison[0] == 1:
                    await dbset(interaction.guild.id, interaction.client.user.name, "ismsglogon", 0)
                    await interaction.response.send_message(content=f"Message log **Disabled**", ephemeral=True)
                    await interaction.followup.edit(view=SelectView())
                else:
                    await dbset(interaction.guild.id, interaction.client.user.name, "ismsglogon", 1)
                    await interaction.response.send_message(content=f"Message log **Enabled**", ephemeral=True)
                    await interaction.followup.edit(view=SelectView())
            if self.values[0] == "Report Transcript":
                ison = await dbget(interaction.guild.id, interaction.client.user.name, "isreporttranscripton")
                if ison[0] == 1:
                    await dbset(interaction.guild.id, interaction.client.user.name, "isreporttranscripton", 0)
                    await interaction.response.send_message(content=f"Report Transcript **Disabled**", ephemeral=True)
                    await interaction.followup.edit(view=SelectView())
                else:
                    await dbset(interaction.guild.id, interaction.client.user.name, "isreporttranscripton", 1)
                    await interaction.response.send_message(content=f"Report Transcript **Enabled**", ephemeral=True)
                    await interaction.followup.edit(view=SelectView())
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


class SelectView(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        self.add_item(Select())


class configcmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="config", description="Command to toggle some bot features.")
    async def config(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(content=f"""Configure me to your liking!""", view=SelectView(), ephemeral=True)

        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


async def setup(bot):
    await bot.add_cog(configcmd(bot))
