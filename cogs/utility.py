import discord
from discord.ext import commands
from discord import app_commands, Embed
from discord.ext.commands import Cog

PURPLE = discord.Color(0x9b59b6)

class Utility(Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Bot latency")
    async def ping_slash(self, interaction: discord.Interaction):
        embed = Embed(title="🏓 Pong", description=f"Latency: `{round(self.bot.latency*1000)} ms`", color=PURPLE)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="Display user's avatar")
    @app_commands.describe(user="User (defaults to you)")
    async def avatar_slash(self, interaction: discord.Interaction,
                           user: discord.Member = None):
        user = user or interaction.user
        embed = Embed(title=str(user), color=PURPLE)
        embed.set_image(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))