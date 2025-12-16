"""Text-based chat commands for the Discord bot."""
import discord
from discord.ext import commands
from services.ai_handler import AIHandler
from utils.context_manager import ContextManager


class ChatCommands(commands.Cog):
    """Cog for handling text-based chat commands."""
    
    def __init__(self, bot: commands.Bot):
        """Initialize chat commands cog."""
        self.bot = bot
        self.ai_handler = AIHandler()
        self.context_manager = ContextManager()
    
    @commands.command(name="botping")
    async def botping(self, ctx: commands.Context):
        """Check if the bot is responsive (namespaced to avoid conflicts)."""
        await ctx.send(f"Brax Pong! Latency: {round(self.bot.latency * 1000)}ms")
    
    @commands.command(name="bothelp")
    async def bothelp(self, ctx: commands.Context):
        """Display help information (namespaced to avoid conflicts)."""
        help_text = """
**Available Commands:**
`!botping` - Check bot responsiveness
`!bothelp` - Show this help message
`!ask <message>` - Chat with the AI
`!clearctx` - Clear conversation context
`!join` - Join your voice channel
`!leave` - Leave the voice channel

**Voice Commands:**
Once in a voice channel, the bot will listen and respond to your speech!
        """
        await ctx.send(help_text)
    
    @commands.command(name="ask")
    async def ask(self, ctx: commands.Context, *, message: str):
        """Chat with the AI bot (namespaced to avoid conflicts)."""
        await ctx.typing()
        
        # Get user context
        user_id = ctx.author.id
        context = self.context_manager.get_context(user_id)
        
        # Generate AI response
        response = await self.ai_handler.generate_response(message, context)
        
        # Add messages to context
        self.context_manager.add_message(user_id, "user", message)
        self.context_manager.add_message(user_id, "assistant", response)
        
        await ctx.send(response)
    
    @commands.command(name="clearctx")
    async def clear_context(self, ctx: commands.Context):
        """Clear conversation context for the user (namespaced to avoid conflicts)."""
        self.context_manager.clear_context(ctx.author.id)
        await ctx.send("Conversation context cleared!")


async def setup(bot: commands.Bot):
    """Setup function for loading the cog."""
    await bot.add_cog(ChatCommands(bot))

