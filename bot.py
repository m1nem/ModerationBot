import os, discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncpg

load_dotenv()
TOKEN   = os.getenv("BOT_TOKEN")
PG_DSN  = os.getenv("PG_DSN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# -----------  GLOBAL PURPLE COLOR  -----------
PURPLE = discord.Color(0x9b59b6)

# -----------  POSTGRES POOL  -----------
async def create_pool():
    bot.pg_pool = await asyncpg.create_pool(PG_DSN)
    async with bot.pg_pool.acquire() as con:
        await con.execute("""
            CREATE TABLE IF NOT EXISTS warns(
                id SERIAL PRIMARY KEY,
                user_id BIGINT, guild_id BIGINT, mod_id BIGINT,
                reason TEXT, created_at TIMESTAMP DEFAULT NOW()
            );
            CREATE TABLE IF NOT EXISTS custom_cmds(
                guild_id BIGINT, name TEXT, content TEXT,
                PRIMARY KEY(guild_id, name)
            );
        """)

# -----------  STARTUP  -----------
@bot.event
async def on_ready():
    await create_pool()
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.custom_commands")
    await bot.load_extension("cogs.utility")
    await bot.tree.sync()          # global slash sync
    print(f"{bot.user} ready! + slash synced")

bot.run(TOKEN)