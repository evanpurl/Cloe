import datetime

import discord
from discord import app_commands
from discord.ext import commands
from util.dbsetget import dbset, dbget


class messageeditdeletecmds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        try:
            ison = await dbget(message.guild.id, self.bot.user.name, "ismsglogon")
            if ison[0]:
                embed = discord.Embed(
                    title="Message Deleted", color=discord.Color.red(),
                    timestamp=datetime.datetime.now())
                embed.set_author(name=message.author.name, icon_url=message.author.avatar)
                embed.add_field(name="Channel", value=message.channel.mention)
                if len(message.content) <= 1024:
                    embed.add_field(name="Message", value=message.content)
                    msgchnl = await dbget(message.guild.id, self.bot.user.name, "messagechannelid")
                    channel = discord.utils.get(message.guild.channels, id=msgchnl[0])
                    if channel:
                        await channel.send(embed=embed)
                else:
                    embed.add_field(name="Message", value="Message too long to process")
                    msgchnl = await dbget(message.guild.id, self.bot.user.name, "messagechannelid")
                    channel = discord.utils.get(message.guild.channels, id=msgchnl[0])
                    if channel:
                        await channel.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before: discord.Message, message_after: discord.Message):
        try:
            ison = await dbget(message_before.guild.id, self.bot.user.name, "ismsglogon")
            if ison[0]:
                embed = discord.Embed(
                    title="Message Edit", color=discord.Color.blue(),
                    timestamp=datetime.datetime.now())
                embed.set_author(name=message_before.author.name, icon_url=message_before.author.avatar)
                beforemsglength = len(message_before.content)
                aftermsglength = len(message_after.content)
                embed.add_field(name="Channel", value=message_before.channel.mention)
                if beforemsglength <= 1024:
                    embed.add_field(name="Before", value=message_before.content)
                    embed.add_field(name="After", value=message_after.jump_url)
                    msgchnl = await dbget(message_before.guild.id, self.bot.user.name, "messagechannelid")
                    channel = discord.utils.get(message_before.guild.channels, id=msgchnl[0])
                    if channel:
                        await channel.send(embed=embed)
                else:
                    embed.add_field(name="Before", value="Message too long")
                    embed.add_field(name="After", value=message_after.jump_url)
                    msgchnl = await dbget(message_before.guild.id, self.bot.user.name, "messagechannelid")
                    channel = discord.utils.get(message_before.guild.channels, id=msgchnl[0])
                    if channel:
                        await channel.send(embed=embed)
        except Exception as e:
            print(e)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="resetlogchannel", description="Command to reset your server's log channel.")
    async def resetlogchannel(self, interaction: discord.Interaction):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "messagechannelid", 0)
            await interaction.response.send_message(f"Log channel config has been reset.", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="setlogchannel", description="Command to set your server's log channel.")
    async def setlogchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "messagechannelid", channel.id)
            await interaction.response.send_message(
                f"Your log channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


async def setup(bot: commands.Cog):
    await bot.add_cog(messageeditdeletecmds(bot))
