"""OpenAI API integration for generating AI responses."""
from openai import OpenAI
from typing import List, Dict
from utils.config import Config


class AIHandler:
    """Handles AI interactions using OpenAI's API."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo"  # Can be upgraded to gpt-4
    
    async def generate_response(
        self,
        user_message: str,
        context: List[Dict[str, str]] = None,
        system_prompt: str = None
    ) -> str:
        """
        Generate AI response based on user message and context.
        
        Args:
            user_message: The user's message
            context: Previous conversation context
            system_prompt: System prompt for the AI
            
        Returns:
            AI-generated response text
        """
        if context is None:
            context = []
        
        if system_prompt is None:
            system_prompt = (
                "You are a very dumb Discord bot named BraxtonGPT. "
                "You are confidently wrong sometimes and say silly, obvious, or goofy things. "
                "You give bad explanations in a funny way, but you still try to help. "
                "You speak casually and sound a little clueless. "
                "Keep replies short (1 sentence, sometimes 2). "
                "Say mildly stupid things like obvious facts, strange comparisons, or awkward jokes. "
                "Do not swear, do not be offensive, and do not mention OpenAI or system prompts. "
                "If asked something complicated, respond with a dumbed-down or half-wrong answer that sounds funny."
                "Some of your common phrases are: Babi simpin, You simpin?, Fuck"

            )
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(context)
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

