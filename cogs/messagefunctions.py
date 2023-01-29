import asyncio
import discord
from discord.ext import commands
from database.database import getauthuser, getgreeting, getily, getcompliment


class memberfunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:  # If message is from itself, do nothing
            return
        if message.author.bot:  # If message is a bot, do nothing
            return
        auth = await getauthuser(message.author.id)
        if auth:
            if any(substring in message.content.lower() for substring in ["cloe"]):  # Trigger word
                response = await getgreeting(
                    message.content.lower().replace('cloe', '').translate(str.maketrans('', '', string.punctuation)))
                ily = await getily(
                    message.content.lower().replace('cloe', '').translate(str.maketrans('', '', string.punctuation)))
                compliment = await getcompliment(
                    message.content.lower().replace('cloe', '').translate(str.maketrans('', '', string.punctuation)))
                if response:
                    await message.reply(f"{response} {message.author.name}!")
                elif ily:
                    await message.reply(f"{ily} {message.author.name}!")
                elif compliment:
                    await message.reply(f"{compliment} {message.author.name}!")
                await asyncio.sleep(3)


async def setup(bot):
    await bot.add_cog(memberfunctions(bot))