import discord
from discord import app_commands
from discord.ext import commands


# Needs "manage role" perms

class ticketcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket", description="Command used by members to create a ticket.")
    async def ticket(self, interaction: discord.Interaction) -> None:
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True)}
        existticket = discord.utils.get(interaction.guild.categories, name=f"ticket-{interaction.user.name}")
        if existticket:
            await interaction.response.send_message(content=f"You already have an existing ticket you silly goose. {existticket.mention}", ephemeral=True)
        else:
            ticketcat = discord.utils.get(interaction.guild.channels, name="Tickets")
            if ticketcat:
                ticketchan = await interaction.guild.create_text_channel(f"ticket {interaction.user.name}", category=ticketcat, overwrites=overwrites)
                await interaction.response.send_message(content=f"Ticket created in {ticketchan.mention}!", ephemeral=True)
                await ticketchan.send(content=f"Hey there {interaction.user.mention}! Let us know what you need below!")

            else:
                ticketchan = await interaction.guild.create_text_channel(f"ticket {interaction.user.name}", overwrites=overwrites)
                await interaction.response.send_message(content=f"Ticket created in {ticketchan.mention}!", ephemeral=True)
                await ticketchan.send(content=f"Hey there {interaction.user.mention}! Let us know what you need below!")


async def setup(bot):
    await bot.add_cog(ticketcmd(bot))
