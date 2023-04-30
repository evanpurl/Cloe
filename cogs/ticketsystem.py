import asyncio
import datetime
import io
import chat_exporter
import discord
from discord import app_commands, ui
from discord.ext import commands
from util.dbsetget import dbget, dbset

timeout = 300  # seconds

botsdiscord = discord.Object(id=1081357638954123276)  # Bots by Purls Discord


# Needs "manage role" perms
# ticket-usernamediscriminator

def ticketembed(bot):
    embed = discord.Embed(description=f"When you are finished, click the close ticket button below. This ticket will "
                                      f"close in 5 minutes if no message is sent.", color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed

class ticketbuttonpanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", emoji="🗑️", style=discord.ButtonStyle.red,
                       custom_id="Cloe:close")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            lchanid = await dbget(interaction.guild.id, interaction.client.user.name, "ticketchannelid")
            logchannel = discord.utils.get(interaction.guild.channels,
                                           id=lchanid[0])
            if logchannel:
                transcript = await chat_exporter.export(
                    interaction.channel,
                )
                if transcript is None:
                    return

                transcript_file = discord.File(
                    io.BytesIO(transcript.encode()),
                    filename=f"transcript-{interaction.channel.name}.html",
                )

                await logchannel.send(file=transcript_file)
            await interaction.channel.delete()
        except Exception as e:
            print(e)

    @commands.has_permissions(manage_channels=True)
    @discord.ui.button(label="Auto-Close Ticket", emoji="⏲️", style=discord.ButtonStyle.gray,
                       custom_id="Cloe:autoclose")
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
                    lchanid = await dbget(interaction.guild.id, interaction.client.user.name, "ticketchannelid")
                    logchannel = discord.utils.get(interaction.guild.channels,
                                                   id=lchanid[0])
                    if logchannel:
                        transcript = await chat_exporter.export(
                            interaction.channel,
                        )
                        if transcript is None:
                            return

                        transcript_file = discord.File(
                            io.BytesIO(transcript.encode()),
                            filename=f"transcript-{interaction.channel.name}.html",
                        )

                        await logchannel.send(file=transcript_file)
                    await interaction.channel.delete()
                    return
            else:
                await interaction.response.send_message(content="You don't have permission to do that.", ephemeral=True)
        except Exception as e:
            print(e)


class ticketbutton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", emoji="📨", style=discord.ButtonStyle.blurple,
                       custom_id="ticketbutton")
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            existticket = discord.utils.get(interaction.guild.channels,
                                            name=f"ticket-{interaction.user.name.lower()}{interaction.user.discriminator}")
            if existticket:
                await interaction.response.send_message(
                    content=f"You already have an existing ticket you silly goose. {existticket.mention}",
                    ephemeral=True)
            else:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True)}
                ticketcat = discord.utils.get(interaction.guild.categories, name="Tickets")
                if ticketcat:
                    ticketchan = await interaction.guild.create_text_channel(
                        f"ticket-{interaction.user.name}{interaction.user.discriminator}", category=ticketcat,
                        overwrites=overwrites)
                    await interaction.response.send_message(content=f"Ticket created in {ticketchan.mention}!",
                                                            ephemeral=True)
                    await ticketchan.send(
                        content=f"{interaction.user.mention} created a ticket!")
                    await ticketchan.send(
                        embed=ticketembed(interaction.client),
                        view=ticketbuttonpanel())

                    def check(m: discord.Message):  # m = discord.Message.
                        return m.author.id == interaction.user.id and m.channel.id == ticketchan.id

                    try:
                        msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
                    except asyncio.TimeoutError:
                        lchanid = await dbget(interaction.guild.id, interaction.client.user.name, "ticketchannelid")
                        logchannel = discord.utils.get(interaction.guild.channels,
                                                       id=lchanid[0])
                        if logchannel:
                            transcript = await chat_exporter.export(
                                ticketchan,
                            )
                            if transcript is None:
                                return

                            transcript_file = discord.File(
                                io.BytesIO(transcript.encode()),
                                filename=f"transcript-{ticketchan.name}.html",
                            )

                            await logchannel.send(file=transcript_file)

                        await ticketchan.delete()

                else:
                    ticketchan = await interaction.guild.create_text_channel(
                        f"ticket-{interaction.user.name}{interaction.user.discriminator}", overwrites=overwrites)
                    await interaction.response.send_message(content=f"Ticket created in {ticketchan.mention}!",
                                                            ephemeral=True)
                    await ticketchan.send(
                        content=f"{interaction.user.mention} created a ticket!")
                    await ticketchan.send(
                        embed=ticketembed(interaction.client),
                        view=ticketbuttonpanel())

                    def check(m: discord.Message):  # m = discord.Message.
                        return m.author.id == interaction.user.id and m.channel.id == ticketchan.id

                    try:
                        msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
                    except asyncio.TimeoutError:
                        lchanid = await dbget(interaction.guild.id, interaction.client.user.name, "ticketchannelid")
                        logchannel = discord.utils.get(interaction.guild.channels,
                                                       id=lchanid[0])
                        if logchannel:
                            transcript = await chat_exporter.export(
                                ticketchan,
                            )
                            if transcript is None:
                                return

                            transcript_file = discord.File(
                                io.BytesIO(transcript.encode()),
                                filename=f"transcript-{ticketchan.name}.html",
                            )

                            await logchannel.send(file=transcript_file)
                        await ticketchan.delete()
        except Exception as e:
            print(e)


def ticketmessageembed(bot):
    embed = discord.Embed(title="**Tickets**",
                          description=f"If you are interested in my services, or need help with an existing one, click the button below!",
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class ticketcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_roles=True)
    @app_commands.guilds(botsdiscord)
    @app_commands.command(name="ticket", description="Command used by admin to create the ticket message.")
    async def ticket(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.send_message(embed=ticketmessageembed(self.bot), view=ticketbutton())
        except Exception as e:
            print(e)

    @commands.has_permissions(manage_roles=True)
    @app_commands.guilds(botsdiscord)
    @app_commands.command(name="setticketchannel", description="Command used by admin to set the ticket log channel.")
    async def setticketchannel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "ticketchannelid", channel.id)
            await interaction.response.send_message(
                f"Your ticket log channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.",
                ephemeral=True)

        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.guilds(botsdiscord)
    @app_commands.command(name="resetticketchannel", description="Command used by admin to reset the ticket log channel.")
    async def resetmessagechannel(self, interaction: discord.Interaction):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "ticketchannelid", 0)
            await interaction.response.send_message(f"Message log channel config has been reset.", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @setticketchannel.error
    @resetmessagechannel.error
    @ticket.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(ticketcmd(bot))
    bot.add_view(ticketbutton())  # line that inits persistent view
    bot.add_view(ticketbuttonpanel())
