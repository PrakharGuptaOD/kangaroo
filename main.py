import discord
import asyncio
from discord.ext import commands
import config

# Setup the Bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True # Needed for tickets
intents.voice_states = True # Needed for voice logs

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    # Load all modules
    await bot.load_extension("cogs.general") # clear, resource
    await bot.load_extension("cogs.ai_chat") # AI logic
    await bot.load_extension("cogs.voice")   # getlogs
    await bot.load_extension("cogs.tickets") # setup (ticket panel)
    await bot.load_extension("cogs.newsletter") # 

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")
    
    print(f'✅ Logged in as {bot.user}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass