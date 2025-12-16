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
                "You are a helpful Discord bot assistant. "
                "You can provide gaming tips, answer questions, and have casual conversations. "
                "Keep responses concise and friendly."
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

