import discord
import asyncio
from discord import app_commands
from discord.ext import commands

class Newsletter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="newsletter_setup", description="Create the Subscribe button")
    @app_commands.default_permissions(administrator=True)
    async def newsletter_setup(self, interaction: discord.Interaction):
        view = SubscribeView()
        embed = discord.Embed(
            title="📬 Weekly Newsletter",
            description="Click the button below to receive announcements via DM!",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="announce_dm", description="Send a DM to all subscribers")
    @app_commands.default_permissions(administrator=True)
    async def announce_dm(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)
        
        # 1. Get the Subscriber Role
        role = discord.utils.get(interaction.guild.roles, name="Newsletter Subscriber")
        if not role:
            await interaction.followup.send("❌ Role 'Newsletter Subscriber' not found.")
            return

        # 2. Iterate and Send (Slowly)
        count = 0
        failed = 0
        
        for member in role.members:
            if member.bot: continue
            
            try:
                # Send the DM
                await member.send(f"**📢 Announcement from {interaction.guild.name}**\n\n{message}")
                count += 1
                
                # CRITICAL: Wait 2 seconds between DMs to avoid Ban/Rate Limit
                await asyncio.sleep(2) 
                
            except discord.Forbidden:
                # User has DMs blocked
                failed += 1
            except Exception as e:
                print(f"Failed to DM {member.name}: {e}")
                failed += 1

        await interaction.followup.send(f"✅ Sent to {count} subscribers. (Failed: {failed})")

class SubscribeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Subscribe/Unsubscribe", style=discord.ButtonStyle.primary, custom_id="newsletter_sub_btn")
    async def subscribe(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Create the role if it doesn't exist
        role = discord.utils.get(interaction.guild.roles, name="Newsletter Subscriber")
        if not role:
            role = await interaction.guild.create_role(name="Newsletter Subscriber")

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message("❌ Unsubscribed from DMs.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Subscribed! You will now receive DM updates.", ephemeral=True)

async def setup(bot):
    # Register the view so it works after restart
    bot.add_view(SubscribeView())
    await bot.add_cog(Newsletter(bot))