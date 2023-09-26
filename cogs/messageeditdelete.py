import datetime

import discord
from discord.ext import commands
from retiredcogs.dbsetget import dbget


class messageeditdeletecmds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        try:
            msgchnl = await dbget(message.guild.id, self.bot.user.name, "messagechannelid")
            channel = discord.utils.get(message.guild.channels, id=msgchnl[0])
            if channel:
                embed = discord.Embed(
                    title="Message Deleted", color=discord.Color.red(),
                    timestamp=datetime.datetime.now())
                embed.set_author(name=message.author.name, icon_url=message.author.avatar)
                embed.add_field(name="Channel", value=message.channel.mention)
                if len(message.content) <= 1024:
                    embed.add_field(name="Message", value=message.content)
                    await channel.send(embed=embed)
                else:
                    embed.add_field(name="Message", value="Message too long to process")
                    await channel.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before: discord.Message, message_after: discord.Message):
        try:
            msgchnl = await dbget(message_before.guild.id, self.bot.user.name, "messagechannelid")
            channel = discord.utils.get(message_before.guild.channels, id=msgchnl[0])
            if channel:
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
                    await channel.send(embed=embed)
                else:
                    embed.add_field(name="Before", value="Message too long")
                    embed.add_field(name="After", value=message_after.jump_url)
                    await channel.send(embed=embed)
        except Exception as e:
            print(e)


async def setup(bot: commands.Cog):
    await bot.add_cog(messageeditdeletecmds(bot))
