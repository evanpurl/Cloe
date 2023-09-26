import datetime

import discord
from discord import app_commands
from discord.ext import commands
from util.sqlitefunctions import getconfig, create_db

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
            conn = await create_db(f"storage/{member.guild.id}/configuration.db")
            wchannel = await getconfig(conn, "welcomechannelid")
            channel = discord.utils.get(member.guild.channels, id=wchannel)
            if channel:
                await channel.send(embed=userembed(member, member.guild))
            roleid = await getconfig(conn, "defaultroleid")
            role = discord.utils.get(member.guild.roles, id=roleid)
            conn.close()
            if role:
                await member.add_roles(role)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        conn = await create_db(f"storage/{member.guild.id}/configuration.db")
        wchannel = await getconfig(conn, "goodbyechannelid")
        conn.close()
        channel = discord.utils.get(member.guild.channels, id=wchannel)
        if channel:
            await channel.send(embed=userembedbye(member))


async def setup(bot):
    await bot.add_cog(memberfunctions(bot))
