import discord
import os
import datetime
from discord import app_commands
from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def log_voice_event(self, event_text):
        """Writes voice events to a daily log file."""
        today = datetime.date.today()
        filename = f"voice_log_{today}.txt"
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        log_entry = f"{timestamp} {event_text}\n"
        
        # Append to file
        with open(filename, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(log_entry.strip())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot: return
        user_name = f"{member.name}#{member.discriminator}" if member.discriminator != "0" else member.name

        if before.channel is None and after.channel is not None:
            self.log_voice_event(f"🟢 JOIN: {user_name} joined '{after.channel.name}'")
        elif before.channel is not None and after.channel is None:
            self.log_voice_event(f"🔴 LEAVE: {user_name} left '{before.channel.name}'")
        elif before.channel != after.channel:
            self.log_voice_event(f"🔄 MOVE: {user_name} moved to '{after.channel.name}'")
        elif not before.self_video and after.self_video:
            self.log_voice_event(f"🎥 CAMERA ON: {user_name} in '{after.channel.name}'")
        elif before.self_video and not after.self_video:
            self.log_voice_event(f"🖤 CAMERA OFF: {user_name} in '{after.channel.name}'")
        elif not before.self_stream and after.self_stream:
            self.log_voice_event(f"🖥️ STREAM START: {user_name} in '{after.channel.name}'")
        elif before.self_stream and not after.self_stream:
            self.log_voice_event(f"🛑 STREAM END: {user_name} in '{after.channel.name}'")

    @app_commands.command(name="getlogs", description="Get today's voice activity logs (Admin Only)")
    @app_commands.default_permissions(administrator=True)
    async def getlogs(self, interaction: discord.Interaction):
        today = datetime.date.today()
        filename = f"voice_log_{today}.txt"
        if os.path.exists(filename):
            await interaction.response.send_message(f"Here are the voice logs for **{today}**:", file=discord.File(filename), ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ No logs found for today ({today}).", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Voice(bot))