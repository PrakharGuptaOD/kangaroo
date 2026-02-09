import discord
from discord.ext import commands
import config
import ai_helper

class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bot itself
        if message.author == self.bot.user:
            return
        
        # Only reply if mentioned
        if self.bot.user not in message.mentions:
            return

        async with message.channel.typing():
            try:
                print("🤔 Classifying intent...")
                # 1. Classify
                chosen_topic = ai_helper.classify_intent(message.content)

                # Fallback if topic invalid
                if chosen_topic not in config.TOPIC_MAP:
                    chosen_topic = "general_faq"
                    # Note: You might want to define a URL for general_faq in config.py
                    # or handle it differently. For now, we assume it exists or fail gracefully.
                
                if chosen_topic in config.TOPIC_MAP:
                    target_url = config.TOPIC_MAP[chosen_topic]
                    print(f"👉 Classified as: {chosen_topic} | Fetching: {target_url}")

                    # 2. Fetch & Answer
                    answer = await ai_helper.get_ai_answer(target_url, message.content)
                    await message.reply(f"**Topic:** {chosen_topic}\n{answer}")
                else:
                    await message.reply("I'm not sure which resource to check for that question.")

            except Exception as e:
                print(f"Error: {e}")
                await message.reply("Sorry, I encountered an error processing your request.")

async def setup(bot):
    await bot.add_cog(AIChat(bot))