import asyncio
import datetime
import io

import discord
from discord import app_commands
from discord.ext import commands
from chat_exporter import chat_exporter

from util.databasefunctions import create_pool, get

timeout = 300  # seconds


# Needs "manage role" perms
# report-usernamediscriminator

def ticketembed(bot):
    embed = discord.Embed(description=f"When you are finished, click the close report button below. This report will "
                                      f"close in 5 minutes if no message is sent.", color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class reportbuttonpanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Report", emoji="🗑️", style=discord.ButtonStyle.red,
                       custom_id="cloereport:close")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            pool = await create_pool()
            lchanid = await get(pool,
                                f"SELECT transcriptchannelid FROM {self.bot.user.name} WHERE serverid={interaction.guild.id}")
            channel = discord.utils.get(interaction.guild.channels, id=lchanid[0])
            if channel:
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

                await channel.send(file=transcript_file)
            await interaction.channel.delete()
        except Exception as e:
            print(e)

    @commands.has_permissions(manage_channels=True)
    @discord.ui.button(label="Auto-Close Report", emoji="⏲️", style=discord.ButtonStyle.gray,
                       custom_id="cloereport:autoclose")
    async def auto_close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if interaction.user.guild_permissions.manage_channels:
                await interaction.response.send_message(content="Timer started.", ephemeral=True)

                def check(m: discord.Message):  # m = discord.Message.
                    return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

                try:
                    while True:
                        msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
                except asyncio.TimeoutError:
                    pool = await create_pool()
                    lchanid = await get(pool,
                                        f"SELECT transcriptchannelid FROM {self.bot.user.name} WHERE serverid={interaction.guild.id}")
                    channel = discord.utils.get(interaction.guild.channels, id=lchanid[0])
                    if channel:
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

                        await channel.send(file=transcript_file)
                    await interaction.channel.delete()
                    return
            else:
                await interaction.response.send_message(content="You don't have permission to do that.", ephemeral=True)
        except Exception as e:
            print(e)


class reportbutton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Report", emoji="📨", style=discord.ButtonStyle.blurple,
                       custom_id="reportbutton")
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            pool = await create_pool()
            cat = await get(pool,
                            f"SELECT ticketcategoryid FROM {self.bot.user.name} WHERE serverid={interaction.guild.id}")
            existticket = discord.utils.get(interaction.guild.channels,
                                            name=f"report-{interaction.user.name.lower()}")
            if existticket:
                await interaction.response.send_message(
                    content=f"You already have an existing report you silly goose. {existticket.mention}",
                    ephemeral=True)
            else:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True)}
                ticketcat = discord.utils.get(interaction.guild.categories, id=cat[0])
                if ticketcat:
                    ticketchan = await interaction.guild.create_text_channel(
                        f"report-{interaction.user.name}", category=ticketcat,
                        overwrites=overwrites)
                    await interaction.response.send_message(content=f"Report created in {ticketchan.mention}!",
                                                            ephemeral=True)
                    await ticketchan.send(
                        content=f"{interaction.user.mention} created a report!")
                    await ticketchan.send(
                        embed=ticketembed(interaction.client),
                        view=reportbuttonpanel())

                    def check(m: discord.Message):  # m = discord.Message.
                        return m.author.id == interaction.user.id and m.channel.id == ticketchan.id

                    try:
                        msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
                    except asyncio.TimeoutError:
                        await ticketchan.delete()

                else:
                    ticketchan = await interaction.guild.create_text_channel(
                        f"report-{interaction.user.name}", overwrites=overwrites)
                    await interaction.response.send_message(content=f"Report created in {ticketchan.mention}!",
                                                            ephemeral=True)
                    await ticketchan.send(
                        content=f"{interaction.user.mention} created a Report!")
                    await ticketchan.send(
                        embed=ticketembed(interaction.client),
                        view=reportbuttonpanel())

                    def check(m: discord.Message):  # m = discord.Message.
                        return m.author.id == interaction.user.id and m.channel.id == ticketchan.id

                    try:
                        msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
                    except asyncio.TimeoutError:
                        await ticketchan.delete()
        except Exception as e:
            print(e)


def reportmessageembed(bot):
    embed = discord.Embed(title="**Reports**",
                          description=f"Someone breaking a rule? Making you feel unsafe either in public or private? "
                                      f"Feel free to create a report!",
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class reportsystemcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_roles=True)
    @app_commands.command(name="report", description="Command used by admin to create the report message.")
    async def report(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.send_message(embed=reportmessageembed(self.bot), view=reportbutton())
        except Exception as e:
            print(e)

    @report.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(reportsystemcmd(bot))
    bot.add_view(reportbutton())  # line that inits persistent view
    bot.add_view(reportbuttonpanel())
