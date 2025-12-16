"""Main entry point for the Discord voice bot."""
import discord
from discord.ext import commands
import asyncio
from utils.config import Config

# Validate configuration
Config.validate()

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    print(f"{bot.user} has connected to Discord!")
    print(f"Bot is in {len(bot.guilds)} guild(s)")
    
    # Load cogs
    try:
        await bot.load_extension("cogs.chat_commands")
        await bot.load_extension("cogs.voice_commands")
        print("All cogs loaded successfully!")
    except Exception as e:
        print(f"Error loading cogs: {e}")


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    """Handle command errors."""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore unknown commands
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
    else:
        await ctx.send(f"An error occurred: {str(error)}")
        print(f"Command error: {error}")


def main():
    """Main function to run the bot."""
    try:
        bot.run(Config.DISCORD_BOT_TOKEN)
    except KeyboardInterrupt:
        print("\nBot shutting down...")
    except Exception as e:
        print(f"Fatal error: {e}")


if __name__ == "__main__":
    main()

