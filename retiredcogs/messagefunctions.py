import asyncio
from discord.ext import commands
from retiredcogs.database.database import getgreeting, getily, getcompliment, getanswer
import string


class messagefunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:  # If message is from itself, do nothing
            return
        if message.author.bot:  # If message is a bot, do nothing
            return

        if message.mentions:
            tagged = message.mentions
            if tagged[0].id == self.bot.user.id:
                msg = message.content.lower().translate(str.maketrans('', '', string.punctuation)).replace(
                        str(self.bot.user.id), "").split(" ")
                while "" in msg:
                    msg.remove("")
                msg = " ".join(msg)
                answer = await getanswer(msg)
                response = await getgreeting(msg)
                ily = await getily(msg)
                compliment = await getcompliment(msg)
                if answer:
                    await message.reply(f"{answer}!")
                if response:
                    await message.reply(f"{response} {message.author.name}!")
                elif ily:
                    await message.reply(f"{ily} {message.author.name}!")
                elif compliment:
                    await message.reply(f"{compliment} {message.author.name}!")
                await asyncio.sleep(3)


async def setup(bot):
    await bot.add_cog(messagefunctions(bot))
