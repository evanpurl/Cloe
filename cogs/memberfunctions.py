import datetime

import discord
from discord.ext import commands
from util.dbsetget import dbget


def userembed(bot, user):
    embed = discord.Embed(title="**Welcome!**", description=f"Welcome to the server {user.mention}! Please make sure to review the rules!", color=discord.Color.blue(), timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class memberfunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            wchannel = await dbget(member.guild.id, self.bot.user.name, "welcomechannelid")
            channel = discord.utils.get(member.guild.channels, id=wchannel[0])
            if channel:
                await channel.send(embed=userembed(self.bot, member))
            roleid = await dbget(member.guild.id, self.bot.user.name, "defaultroleid")
            role = discord.utils.get(member.guild.roles, id=roleid[0])
            if role:
                await member.add_roles(role)
        except discord.Forbidden:
            wchannel = await dbget(member.guild.id, self.bot.user.name, "welcomechannelid")
            channel = discord.utils.get(member.guild.channels, id=wchannel[0])
            if channel:
                await channel.send(content=f"""Unable to set your role, make sure my role is higher than the role you're trying to add!""")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        wchannel = await dbget(member.guild.id, self.bot.user.name, "welcomechannelid")
        channel = discord.utils.get(member.guild.channels, id=wchannel[0])
        if channel:
            await channel.send(f"Goodbye {member.mention} :(")


async def setup(bot):
    await bot.add_cog(memberfunctions(bot))