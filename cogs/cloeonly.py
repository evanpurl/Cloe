import string
import discord
from discord import app_commands
from discord.ext import commands
from database.cloeonly import setauthuser, getauthuser, getgreeting, getily, getcompliment
from util.accessutils import whohasaccess


class cloeonly(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="setauthorized", description="Slash command for setting cloe's authorized users.")
    async def setauthorized(self, interaction: discord.Interaction, user: discord.User):
        if await whohasaccess(interaction.user.id):
            try:
                await setauthuser(user.id)
                await interaction.response.send_message(
                    content=f"{user.name} has been authorized.",
                    ephemeral=True)
            except Exception as e:
                print(e)
                await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)
        else:
            await interaction.response.send_message(content=f"""You don't have permission to run this command""", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:  # If message is from itself, do nothing
            return
        if message.author.bot:  # If message is a bot, do nothing
            return
        if await getauthuser(message.author.id):
            msg = message.content.lower().translate(str.maketrans('', '', string.punctuation)).split(" ")
            for substring in msg:
                if substring == "cloe":  # Trigger word
                    msg.remove(substring)
                    msg = " ".join(msg)
                    response = await getgreeting(msg)
                    ily = await getily(msg)
                    compliment = await getcompliment(msg)
                    if response:
                        await message.reply(f"{response} {message.author.name}!")
                    elif ily:
                        await message.reply(f"{ily} {message.author.name}!")
                    elif compliment:
                        await message.reply(f"{compliment} {message.author.name}!")


async def setup(bot):
    await bot.add_cog(cloeonly(bot))