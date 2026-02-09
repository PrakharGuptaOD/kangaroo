import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import config

# Configure Gemini once
genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def get_website_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text[:30000] # Limit per page
    except Exception as e:
        print(f"⚠️ Error fetching {url}: {e}")
        return ""

def classify_intent(user_question):
    topics_list = list(config.TOPIC_MAP.keys())
    classification_prompt = f"""
    Classify this user question into one of these topics: {topics_list}.
    Return ONLY the exact topic name as a string. If unsure, return "general_faq".
    User Question: "{user_question}"
    """
    try:
        classification = model.generate_content(classification_prompt).text.strip()
        # Clean up response
        return classification.replace('"', '').replace("'", "").strip()
    except Exception as e:
        print(f"Classification Error: {e}")
        return "general_faq"

async def get_ai_answer(url, question):
    context = get_website_text(url)
    if not context:
        return "I couldn't read the website for that topic."

    prompt = f"""
    You are a helpful support bot. Answer the question using ONLY the context below.
    CONTEXT (from {url}):
    {context}
    INSTRUCTIONS:
    1. Answer clearly and professionally.
    2. If the answer is not in the text, say "I couldn't find that specific detail on the page."
    User Question: "{question}"
    """
    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"