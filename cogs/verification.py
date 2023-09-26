import discord
from discord import app_commands
from discord.ext import commands
from util.sqlitefunctions import getconfig, create_db

# Needs "manage role" perms
"Requires verifiedroleid in db"


def verifymessageembed(server):
    embed = discord.Embed(title=f"**{server.name} Verification Process**",
                          description=f"This server requires you to verify that you're a human. To do so, click the "
                                      f"Verify button below.",
                          color=discord.Color.blue())
    return embed


class Verifybuttonpanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", emoji="✅", style=discord.ButtonStyle.green,
                       custom_id="Cloe:verify")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            verrole = await getconfig(conn, "verifiedroleid")
            role = discord.utils.get(interaction.guild.roles, id=verrole)
            if role:
                if role in interaction.user.roles:
                    await interaction.response.send_message(f"You have already been verified.", ephemeral=True)
                else:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"You have been added to the Verified role.",
                                                            ephemeral=True)
            else:
                await interaction.response.send_message(f"Verified role does not exist, please contact an admin.",
                                                        ephemeral=True)

        except discord.Forbidden:
            await interaction.response.send_message(
                content=f"""Unable to set your role, make sure my role is higher than the role you're trying to add!""",
                ephemeral=True)


class verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="verifybutton", description="Command used by an admin to send the verify button message")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def vbutton(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.send_message(embed=verifymessageembed(interaction.guild),
                                                    view=Verifybuttonpanel())
        except Exception as e:
            print(e)

    @app_commands.command(name="verifyfor", description="Command used by an admin to add user to the Verified role")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def verifyfor(self, interaction: discord.Interaction, user: discord.User) -> None:
        try:
            conn = await create_db(f"storage/{interaction.guild.id}/configuration.db")
            verrole = await getconfig(conn, "verifiedroleid")
            role = discord.utils.get(interaction.guild.roles, id=verrole)
            if role:
                if role in user.roles:
                    await interaction.response.send_message(f"User has already been verified.", ephemeral=True)
                else:
                    await user.add_roles(role)
                    await interaction.response.send_message(f"User has been added to the Verified role.",
                                                            ephemeral=True)
            else:
                await interaction.response.send_message(f"No verified role found, have you ran /setverifiedrole?",
                                                        ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                content=f"""Unable to set your role, make sure my role is higher than the role you're trying to add!""",
                ephemeral=True)

    @verifyfor.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(verification(bot))
    bot.add_view(Verifybuttonpanel())
