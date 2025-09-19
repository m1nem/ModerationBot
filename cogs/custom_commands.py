import discord
from discord.ext import commands
from discord import app_commands, Embed
from discord.ext.commands import Cog

PURPLE = discord.Color(0x9b59b6)

class CustomCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.content.startswith("!"):
            return
        name = message.content.split()[0][1:].lower()
        async with self.bot.pg_pool.acquire() as con:
            row = await con.fetchrow(
                "SELECT content FROM custom_cmds WHERE guild_id=$1 AND name=$2",
                message.guild.id, name
            )
        if row:
            await message.channel.send(row["content"])

    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.command(name="addcmd", description="Create or overwrite a custom command")
    @app_commands.describe(name="Command name (without !)", content="Text to send")
    async def addcmd_slash(self, interaction: discord.Interaction,
                           name: str, content: str):
        async with self.bot.pg_pool.acquire() as con:
            await con.execute(
                "INSERT INTO custom_cmds(guild_id,name,content) VALUES($1,$2,$3) ON CONFLICT (guild_id,name) DO UPDATE SET content=$3",
                interaction.guild.id, name.lower(), content
            )
        embed = Embed(
            title="✅ Custom Command Added",
            description=f"Command `!{name}` saved.",
            color=PURPLE
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.command(name="delcmd", description="Delete a custom command")
    @app_commands.describe(name="Command name (without !)")
    async def delcmd_slash(self, interaction: discord.Interaction, name: str):
        async with self.bot.pg_pool.acquire() as con:
            await con.execute(
                "DELETE FROM custom_cmds WHERE guild_id=$1 AND name=$2",
                interaction.guild.id, name.lower()
            )
        embed = Embed(
            title="🗑️ Custom Command Deleted",
            description=f"Command `!{name}` removed.",
            color=PURPLE
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(CustomCommands(bot))