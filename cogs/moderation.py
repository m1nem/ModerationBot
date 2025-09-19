import discord
from discord.ext import commands
from discord import app_commands, Embed
from discord.ext.commands import Cog

PURPLE = discord.Color(0x9b59b6)

class Moderation(Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------- KICK ----------
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.describe(member="Member to kick", reason="Reason (optional)")
    async def kick_slash(self, interaction: discord.Interaction,
                         member: discord.Member, reason: str = "No reason provided"):
        embed = Embed(title="👢 Kick", description=f"{member.mention} was kicked.", color=PURPLE)
        embed.add_field(name="Reason", value=reason, inline=False)
        await member.kick(reason=reason)
        await interaction.response.send_message(embed=embed)

    # ---------- BAN ----------
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.command(name="ban", description="Ban a member permanently")
    @app_commands.describe(member="Member to ban", reason="Reason (optional)")
    async def ban_slash(self, interaction: discord.Interaction,
                        member: discord.Member, reason: str = "No reason provided"):
        embed = Embed(title="🔨 Ban", description=f"{member.mention} was banned.", color=PURPLE)
        embed.add_field(name="Reason", value=reason, inline=False)
        await member.ban(reason=reason)
        await interaction.response.send_message(embed=embed)

    # ---------- UNBAN ----------
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.command(name="unban", description="Unban a user by ID")
    @app_commands.describe(user_id="Discord ID of the user to unban")
    async def unban_slash(self, interaction: discord.Interaction, user_id: str):
        user = discord.Object(id=int(user_id))
        await interaction.guild.unban(user)
        embed = Embed(title="🔓 Unban", description=f"User `<@{user_id}>` has been unbanned.", color=PURPLE)
        await interaction.response.send_message(embed=embed)

    # ---------- WARN ----------
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.command(name="warn", description="Issue a warning to a member")
    @app_commands.describe(member="Member to warn", reason="Reason")
    async def warn_slash(self, interaction: discord.Interaction,
                         member: discord.Member, reason: str):
        async with self.bot.pg_pool.acquire() as con:
            await con.execute(
                "INSERT INTO warns(user_id,guild_id,mod_id,reason) VALUES($1,$2,$3,$4)",
                member.id, interaction.guild.id, interaction.user.id, reason
            )
        embed = Embed(title="⚠️ Warning", description=f"{member.mention} has been warned.", color=PURPLE)
        embed.add_field(name="Reason", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

    # ---------- WARNS LIST ----------
    @app_commands.command(name="warns", description="List warnings for a member")
    @app_commands.describe(member="Member to check (defaults to you)")
    async def warns_slash(self, interaction: discord.Interaction,
                          member: discord.Member = None):
        member = member or interaction.user
        async with self.bot.pg_pool.acquire() as con:
            rows = await con.fetch(
                "SELECT reason,created_at FROM warns WHERE user_id=$1 AND guild_id=$2 ORDER BY created_at DESC",
                member.id, interaction.guild.id
            )
        if not rows:
            return await interaction.response.send_message("No warnings found.", ephemeral=True)
        embed = Embed(title=f"Warnings for {member}", color=PURPLE)
        for r in rows:
            embed.add_field(name=r["created_at"].strftime("%Y-%m-%d %H:%M"), value=r["reason"], inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))