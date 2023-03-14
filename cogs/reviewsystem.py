import datetime
import discord
from discord import app_commands, ui
from discord.ext import commands


def reviewembed(bot, user, botmade, details, rating):
    star = "⭐"
    embed = discord.Embed(title=f"**Review from {user.mention}**",
                          description=f"Created using {bot.user.mention}'s review system.",
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.add_field(name="Rating:", value=rating * star)
    embed.add_field(name="Bot:", value=botmade)
    embed.add_field(name="Details:", value=details)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class Reviewmodal(ui.Modal, title="Purls' Bot Review."):
    rating = ui.TextInput(label='What would you rate your bot?', style=discord.TextStyle.short, max_length=1,
                          placeholder="(1-5)")
    whatbot = ui.TextInput(label='What bot was made for you?', style=discord.TextStyle.short,
                           max_length=45, placeholder="(bot)")
    details = ui.TextInput(label='Any details you want to share on the service?',
                           style=discord.TextStyle.paragraph,
                           max_length=1000, placeholder="(details)")

    async def on_submit(self, interaction: discord.Interaction):
        reviewchan = 1085335105733673071
        reviewchannel = discord.utils.get(interaction.guild.channels, id=reviewchan)
        await reviewchannel.send(
            embed=reviewembed(interaction.client, interaction.user, self.whatbot, self.details, int(self.rating)))


class reviewbutton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Review", emoji="📨", style=discord.ButtonStyle.blurple,
                       custom_id="reviewbutton")
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(Reviewmodal())
        except Exception as e:
            print(e)


def reviewmessageembed(bot):
    embed = discord.Embed(title="**Reviews**",
                          description=f"If you are a customer and would like to review your bot, click the button below!",
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class reviewcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_roles=True)
    @app_commands.command(name="review", description="Command used by admin to create the review message.")
    async def ticket(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.send_message(embed=reviewmessageembed(self.bot), view=reviewbutton())
        except Exception as e:
            print(e)

    @ticket.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(reviewcmd(bot))
    bot.add_view(reviewbutton())  # line that inits persistent view
