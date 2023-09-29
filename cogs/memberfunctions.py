import datetime

import discord
from discord.ext import commands

from util.databasefunctions import get, create_pool, getmultiple

"needs welcomechannelid in db"


def userembed(user, server):
    embed = discord.Embed(title="**Welcome!**",
                          description=f"Welcome to {server.name} {user.mention}! Please make sure "
                                      f"to review the rules!", color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=user.name, icon_url=user.avatar)
    return embed


def userembedbye(user):
    embed = discord.Embed(title="**Goodbye**", description=f"Goodbye {user.name}.", color=discord.Color.dark_red(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=user.name, icon_url=user.avatar)
    return embed


class memberfunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            pool = await create_pool()
            data = await getmultiple(pool, f"SELECT welcomechannelid, defaultroleid FROM {self.bot.user.name} WHERE "
                                           f"serverid={member.guild.id}")
            channel = discord.utils.get(member.guild.channels, id=data[0])
            if channel:
                await channel.send(embed=userembed(member, member.guild))
            role = discord.utils.get(member.guild.roles, id=data[1])
            if role:
                await member.add_roles(role)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        pool = await create_pool()
        data = await get(pool,
                         f"SELECT goodbyechannelid FROM {self.bot.user.name} WHERE serverid={member.guild.id}")
        channel = discord.utils.get(member.guild.channels, id=data)
        if channel:
            await channel.send(embed=userembedbye(member))


async def setup(bot):
    await bot.add_cog(memberfunctions(bot))
