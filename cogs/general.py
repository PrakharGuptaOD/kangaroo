import discord
from discord import app_commands
from discord.ext import commands
import config

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Delete messages (Admin Only)")
    @app_commands.default_permissions(administrator=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)
        if isinstance(interaction.channel, discord.TextChannel):
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.followup.send(f"🗑️ Deleted {len(deleted)} messages.", ephemeral=True)
        else:
             await interaction.followup.send("❌ Cannot purge messages in this channel type.", ephemeral=True)

    @app_commands.command(name="resource", description="Get a direct link to a specific resource")
    @app_commands.choices(topic=[
        app_commands.Choice(name="Git Guide", value="git_guide"),
        app_commands.Choice(name="Project Policies", value="policies"),
        app_commands.Choice(name="Blogs", value="blogs"),
        app_commands.Choice(name="Projects", value="projects")
    ])
    async def resource(self, interaction: discord.Interaction, topic: app_commands.Choice[str]):
        url = config.TOPIC_MAP.get(topic.value)
        await interaction.response.send_message(f"Here is the link for **{topic.name}**:\n🔗 {url}")

async def setup(bot):
    await bot.add_cog(General(bot))