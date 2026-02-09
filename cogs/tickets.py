import discord
import io
import datetime
from discord import app_commands
from discord.ext import commands

# --- CONFIGURATION ---
TICKET_CATEGORY_ID = 1468579644163887196
TRANSCRIPT_CHANNEL_ID = 1468678137939230993

ROLE_MAPPING = {
    "Cohort Dashboard": 1468579316164984832,
    "ViBe Issue": 1468579316164984832,
    "Query": 1468579316164984832,
    "Moderation": 1468578894482374746,
    "Report Discord": 1468578894482374746,
    "Feedback" : 1468578894482374746
}

# --- UI CLASSES ---
class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close & Save Transcript", style=discord.ButtonStyle.red, custom_id="close_ticket_btn")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Closing ticket...", ephemeral=True)
        
        # Generate Transcript
        transcript_text = f"TRANSCRIPT {interaction.channel.name}\n" + "-"*30 + "\n"
        async for msg in interaction.channel.history(limit=500, oldest_first=True):
            transcript_text += f"{msg.author.name}: {msg.content}\n"
        
        buffer = io.BytesIO(transcript_text.encode('utf-8'))
        file = discord.File(buffer, filename=f"{interaction.channel.name}.txt")

        # Send to Log Channel
        log_channel = interaction.guild.get_channel(TRANSCRIPT_CHANNEL_ID)
        if log_channel: 
            await log_channel.send(content=f"Ticket **{interaction.channel.name}** closed by {interaction.user.mention}.", file=file)
        
        await interaction.channel.delete()

class TicketForm(discord.ui.Modal):
    def __init__(self, category_name, role_id):
        self.category_name = category_name
        self.role_id = role_id
        super().__init__(title=f"Open {category_name} Ticket")

    reason = discord.ui.TextInput(label="Reason", style=discord.TextStyle.paragraph, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        category = guild.get_channel(TICKET_CATEGORY_ID)
        staff_role = guild.get_role(self.role_id)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        if staff_role: overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True)

        channel_name = f"{self.category_name.lower().replace(' ', '-')}-{interaction.user.name}"
        ticket_channel = await guild.create_text_channel(name=channel_name, category=category, overwrites=overwrites)

        embed = discord.Embed(title="Reason", description=self.reason.value, color=discord.Color.green())
        mention_str = staff_role.mention if staff_role else ""
        
        await ticket_channel.send(content=f"Hey {interaction.user.mention}! {mention_str}", embed=embed, view=CloseTicketView())
        await interaction.followup.send(f"Ticket created: {ticket_channel.mention}", ephemeral=True)

class CategorySelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=cat, value=cat) for cat in ROLE_MAPPING.keys()]
        super().__init__(placeholder="Select Category...", options=options)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TicketForm(self.values[0], ROLE_MAPPING.get(self.values[0])))

class CategoryView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(CategorySelect())

class TicketLauncher(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.blurple, custom_id="ticket_launch_btn")
    async def ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(view=CategoryView(), ephemeral=True)

# --- COG CLASS ---
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup", description="Deploy the Ticket Panel (Admin Only)")
    @app_commands.default_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Support Center", description="Click the button below to open a ", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, view=TicketLauncher())

async def setup(bot):
    # Register the views so buttons work after restart
    bot.add_view(TicketLauncher())
    bot.add_view(CloseTicketView())
    await bot.add_cog(Tickets(bot))