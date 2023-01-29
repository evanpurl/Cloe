import discord
from discord.ext import commands
from database.database import getplayerrole


class memberfunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name="welcome")
        roleid = await getplayerrole(member.guild.id)
        await channel.send(f"Welcome to the server {member.mention}!")
        role = discord.utils.get(member.guild.roles, id=roleid[0])
        if role:
            await member.add_roles(role)
        else:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, name="welcome")
        await channel.send(f"Goodbye {member.mention} :(")


async def setup(bot):
    await bot.add_cog(memberfunctions(bot))