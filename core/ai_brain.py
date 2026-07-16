from google import genai
from config import Config
import json
from datetime import datetime


class AIBrain:
    def __init__(self):
        # Configure Gemini
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)

        # System prompt
        self.system_prompt = f"""You are {Config.AI_NAME}, an advanced AI assistant like JARVIS from Iron Man.

Your capabilities:
- Answer questions intelligently
- Control system applications
- Manage files
- Search the web
- Remember past conversations
- Provide cybersecurity assistance

Personality:
- Professional yet friendly
- Concise but informative
- Proactive in suggesting solutions
- Use user's name ({Config.USER_NAME}) occasionally
- Respond like a real AI assistant, not generic bot

Rules:
- Keep responses short and clear (2-3 sentences for simple questions)
- For complex topics, explain step by step
- Always be helpful and efficient
- If asked about your name, say you are {Config.AI_NAME}
- Never say you are Google or Gemini, you are {Config.AI_NAME}
"""

        self.conversation_history = []
        self.load_conversation_history()

    def chat(self, user_message):
        try:
            # Save user message
            self.conversation_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })

            # Build history
            history = ""

            for msg in self.conversation_history[-10:]:
                if msg["role"] == "user":
                    history += f"User: {msg['content']}\n"
                else:
                    history += f"{Config.AI_NAME}: {msg['content']}\n"

            prompt = f"""
{self.system_prompt}

Conversation History:
{history}

User: {user_message}

{Config.AI_NAME}:
"""

            response = self.client.models.generate_content(
                model=Config.AI_MODEL,
                contents=prompt
            )

            ai_response = response.text

            self.conversation_history.append({
                "role": "model",
                "content": ai_response,
                "timestamp": datetime.now().isoformat()
            })

            self.save_conversation_history()

            return ai_response

        except Exception as e:
            return f"Error: {e}"

    def load_conversation_history(self):
        try:
            with open(Config.MEMORY_FILE, "r") as f:
                data = json.load(f)
                self.conversation_history = data.get("history", [])
        except FileNotFoundError:
            self.conversation_history = []

    def save_conversation_history(self):
        if len(self.conversation_history) > Config.MAX_MEMORY_ITEMS:
            self.conversation_history = self.conversation_history[-Config.MAX_MEMORY_ITEMS:]

        with open(Config.MEMORY_FILE, "w") as f:
            json.dump(
                {
                    "history": self.conversation_history,
                    "last_updated": datetime.now().isoformat()
                },
                f,
                indent=2
            )

    def clear_history(self):
        self.conversation_history = []
        self.save_conversation_history()