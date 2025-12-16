"""Conversation context management for maintaining chat history."""
from collections import deque
from typing import List, Dict


class ContextManager:
    """Manages conversation context for AI interactions."""
    
    def __init__(self, max_length: int = 10):
        """
        Initialize context manager.
        
        Args:
            max_length: Maximum number of messages to keep in context
        """
        self.max_length = max_length
        self.contexts: Dict[int, deque] = {}  # user_id -> message history
    
    def add_message(self, user_id: int, role: str, content: str):
        """
        Add a message to the conversation context.
        
        Args:
            user_id: Discord user ID
            role: Message role ('user' or 'assistant')
            content: Message content
        """
        if user_id not in self.contexts:
            self.contexts[user_id] = deque(maxlen=self.max_length)
        
        self.contexts[user_id].append({
            "role": role,
            "content": content
        })
    
    def get_context(self, user_id: int) -> List[Dict[str, str]]:
        """
        Get conversation context for a user.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            List of message dictionaries with 'role' and 'content'
        """
        if user_id not in self.contexts:
            return []
        return list(self.contexts[user_id])
    
    def clear_context(self, user_id: int):
        """Clear conversation context for a user."""
        if user_id in self.contexts:
            del self.contexts[user_id]
    
    def clear_all(self):
        """Clear all conversation contexts."""
        self.contexts.clear()

