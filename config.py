import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

#if not DISCORD_TOKEN or not GEMINI_API_KEY:
    #raise ValueError("❌ Error: API Keys not found. Check your .env file.")

# Map keywords/topics to specific URLs
TOPIC_MAP = {
    "blogs": "https://sudarshansudarshan.github.io/vinternship/blogs/",
    "vlogs": "https://sudarshansudarshan.github.io/vinternship/vlogs/",
    "linkedin_posts": "https://sudarshansudarshan.github.io/vinternship/linkedin_post/",
    "endorsements": "https://sudarshansudarshan.github.io/vinternship/endorsements/",
    "projects": "https://sudarshansudarshan.github.io/vinternship/projects/",
    "case_studies": "https://sudarshansudarshan.github.io/vinternship/case-studies/",
    "git_guide": "https://sudarshansudarshan.github.io/vinternship/git-guide/",
    "policies": "https://sudarshansudarshan.github.io/vinternship/protocols_and_policies/",
    "homepage": "https://sudarshansudarshan.github.io/vinternship/hp/"
}