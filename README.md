# Braxton GPT - Discord Voice Bot

A Discord bot that can join voice channels, listen to users speaking, transcribe their speech using OpenAI Whisper, generate responses using OpenAI's GPT models, and speak back to users with text-to-speech capabilities.

## Features

- 🎤 **Voice Channel Integration**: Join and interact in Discord voice channels
- 🗣️ **Speech-to-Text**: Real-time transcription using OpenAI Whisper API
- 🤖 **AI Responses**: Intelligent conversation using OpenAI GPT models
- 🔊 **Text-to-Speech**: Natural-sounding voice responses using OpenAI TTS
- 💬 **Text Commands**: Chat with the bot via text commands
- 📝 **Context Management**: Maintains conversation history for better responses

## Prerequisites

- Python 3.9 or higher
- FFmpeg installed on your system
- Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))
- OpenAI API Key (from [OpenAI Platform](https://platform.openai.com/))

## Installation

### 1. Clone or navigate to the project directory

```bash
cd /Users/james/Desktop/Folders/Braxton_GPT
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install system dependencies

**macOS:**
```bash
brew install ffmpeg opus
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg libopus0 libffi-dev libnacl-dev python3-dev
```

**Windows:**
Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your PATH.

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Set up environment variables

Create a `.env` file in the project root:

```bash
# Discord Bot Configuration
DISCORD_BOT_TOKEN=your_discord_token_here

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_key_here

# Optional Configuration
GUILD_ID=your_server_id_here
MAX_CONTEXT_LENGTH=10
TTS_VOICE=alloy
```

**Getting your Discord Bot Token:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application or select an existing one
3. Go to the "Bot" section
4. Click "Add Bot" if needed
5. Copy the token and enable these privileged gateway intents:
   - MESSAGE CONTENT INTENT
   - SERVER MEMBERS INTENT (if needed)

**Getting your OpenAI API Key:**
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key

### 6. Invite the bot to your server

1. In Discord Developer Portal, go to OAuth2 > URL Generator
2. Select scopes: `bot` and `applications.commands`
3. Select bot permissions:
   - Connect
   - Speak
   - Use Voice Activity
   - Read Message History
   - Send Messages
4. Copy the generated URL and open it in your browser to invite the bot

## Usage

### Running the bot

```bash
python bot.py
```

You should see a message indicating the bot has connected to Discord.

### Commands

**Text Commands:**
- `!ping` - Check bot responsiveness
- `!help` - Show help information
- `!chat <message>` - Chat with the AI via text
- `!clear` - Clear your conversation context

**Voice Commands:**
- `!join` - Bot joins your voice channel and starts listening
- `!leave` - Bot leaves the voice channel

Once the bot joins a voice channel, it will automatically:
1. Listen to users speaking
2. Transcribe speech to text
3. Generate AI responses
4. Speak responses back to the channel

## Project Structure

```
Braxton_GPT/
├── bot.py                    # Main bot entry point
├── cogs/
│   ├── voice_commands.py     # Voice channel commands
│   └── chat_commands.py      # Text commands
├── services/
│   ├── speech_to_text.py     # STT service (Whisper)
│   ├── text_to_speech.py     # TTS service (OpenAI TTS)
│   └── ai_handler.py         # OpenAI API integration
├── utils/
│   ├── audio_processor.py    # Audio capture and processing
│   ├── context_manager.py    # Conversation context handling
│   └── config.py             # Configuration management
├── .env                      # Environment variables (create this)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Configuration

### TTS Voices

Available OpenAI TTS voices:
- `alloy` (default)
- `echo`
- `fable`
- `onyx`
- `nova`
- `shimmer`

Change the voice in your `.env` file:
```
TTS_VOICE=nova
```

### Context Length

Control how many previous messages are kept in context:
```
MAX_CONTEXT_LENGTH=10
```

## Troubleshooting

### Bot won't connect
- Verify your `DISCORD_BOT_TOKEN` is correct
- Check that the bot has been invited to your server with proper permissions

### FFmpeg errors
- Ensure FFmpeg is installed and accessible in your PATH
- Test with: `ffmpeg -version`

### Audio not working
- Verify the bot has "Connect" and "Speak" permissions
- Check that you're in a voice channel when using `!join`
- Ensure your system has audio output capabilities

### OpenAI API errors
- Verify your `OPENAI_API_KEY` is valid and has credits
- Check API rate limits and usage quotas

## Costs

Estimated costs per hour of usage:
- **OpenAI Whisper API**: ~$0.36 per hour of audio
- **OpenAI GPT-3.5-turbo**: ~$0.002 per 1K tokens
- **OpenAI TTS**: ~$15 per 1M characters

## Development

### Testing

Test each component individually:
1. Test bot connection: `!ping`
2. Test text chat: `!chat hello`
3. Test voice join: `!join`
4. Test voice interaction: Speak in voice channel

### Extending the Bot

- Add new commands in `cogs/chat_commands.py` or `cogs/voice_commands.py`
- Modify AI prompts in `services/ai_handler.py`
- Adjust audio processing in `utils/audio_processor.py`

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions, refer to:
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
