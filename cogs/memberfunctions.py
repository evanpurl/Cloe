import datetime

import discord
from discord import app_commands
from discord.ext import commands
from util.dbsetget import dbget, dbset

"needs welcomechannelid in db"


def userembed(bot, user, server):
    embed = discord.Embed(title="**Welcome!**", description=f"Welcome to {server.name} {user.mention}! Please make sure "
                                                            f"to review the rules!", color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
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
                await channel.send(embed=userembed(self.bot, member, member.guild))
            roleid = await dbget(member.guild.id, self.bot.user.name, "defaultroleid")
            role = discord.utils.get(member.guild.roles, id=roleid[0])
            if role:
                await member.add_roles(role)
        except Exception as e:
            print(e)
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

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="setwelcomechannel", description="Command to set your server's welcome channel.")
    async def welcomechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "welcomechannelid", channel.id)
            await interaction.response.send_message(
                f"Your welcome channel has been set to {discord.utils.get(interaction.guild.channels, id=channel.id)}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="resetwelcomechannel", description="Command to reset your server's welcome channel.")
    async def resetwelcomechannel(self, interaction: discord.Interaction):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "welcomechannelid", 0)
            await interaction.response.send_message(f"Welcome channel config has been reset.", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @welcomechannel.error
    @resetwelcomechannel.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(memberfunctions(bot))