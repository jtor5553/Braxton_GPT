# Discord Voice Bot Implementation Plan

## Project Overview
Build a Discord bot that can join voice channels, listen to users speaking, transcribe their speech, generate responses using OpenAI's API, and speak back to users with text-to-speech capabilities.

## Core Components

### 1. Bot Framework & Authentication
- **Discord.js** or **Discord.py** for bot framework
- Discord Bot Token (from Discord Developer Portal)
- OpenAI API Key for AI responses
- Register bot with appropriate permissions:
  - Connect to voice channels
  - Speak in voice channels
  - Read messages
  - Send messages

### 2. Voice Channel Integration
- Connect to voice channels on command
- Handle voice channel join/leave events
- Manage audio stream connections
- Handle multiple users speaking simultaneously

### 3. Speech-to-Text (STT)
- **Option A**: OpenAI Whisper API (recommended for accuracy)
- **Option B**: Google Cloud Speech-to-Text
- **Option C**: Local Whisper model (more complex, but cheaper)
- Capture audio streams from Discord voice channels
- Process audio in real-time or chunks
- Convert speech to text for processing

### 4. AI Processing with OpenAI
- Use GPT-4 or GPT-3.5-turbo for conversation
- Implement context management (conversation history)
- Create specialized prompts for:
  - Gaming tips and strategies
  - Casual conversation
  - Context-aware responses
- Token management to stay within API limits

### 5. Text-to-Speech (TTS)
- **Option A**: OpenAI TTS API (natural-sounding voices)
- **Option B**: Google Cloud Text-to-Speech
- **Option C**: Discord.js native TTS (limited quality)
- Convert AI responses to audio
- Stream audio back to Discord voice channel

## Technical Architecture (Python)

### Required Libraries
```
- discord.py[voice] (Discord API wrapper with voice support)
- PyNaCl (voice encryption)
- openai (OpenAI API client)
- pydub (audio processing)
- python-dotenv (environment variables)
- aiohttp (async HTTP requests)
- asyncio (asynchronous programming)
- wave (audio file handling)
- numpy (audio data processing)
```

### System Dependencies
```
- FFmpeg (audio/video processing)
- libopus (audio codec)
- libffi-dev (foreign function interface)
- libnacl-dev (encryption library)
- python3-dev (Python development headers)
```

### Installation Commands
```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install ffmpeg libopus0 libffi-dev libnacl-dev python3-dev

# Install Python packages
pip install discord.py[voice]
pip install openai
pip install pydub
pip install python-dotenv
pip install aiohttp
pip install numpy
```

## Project Structure (Python)

```
discord-voice-bot/
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
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation
```

### Phase 1: Basic Bot Setup
1. Create Discord application and bot in Developer Portal
2. Set up project structure and install dependencies
3. Implement basic bot connection and command handling
4. Test basic text commands (ping, help, etc.)

### Phase 2: Voice Channel Integration
1. Implement voice channel join/leave commands
2. Set up audio stream reception
3. Handle voice state updates
4. Test basic voice connectivity

### Phase 3: Speech Recognition
1. Integrate speech-to-text service
2. Capture and buffer audio from voice channels
3. Process audio chunks and convert to text
4. Implement user detection (who is speaking)
5. Test transcription accuracy

### Phase 4: AI Integration
1. Set up OpenAI API client
2. Design prompt templates for gaming tips and conversation
3. Implement conversation context management
4. Add rate limiting and error handling
5. Test response quality and relevance

### Phase 5: Text-to-Speech
1. Integrate TTS service
2. Convert AI responses to audio
3. Stream audio back to voice channel
4. Optimize audio quality and latency
5. Test end-to-end conversation flow

### Phase 6: Advanced Features
1. Multi-user conversation handling
2. Game-specific knowledge bases
3. Voice activation detection (reduce noise)
4. Custom wake words or mention detection
5. Conversation history persistence

## Python-Specific Challenges & Solutions

### Challenge 1: Audio Format Conversion
- **Issue**: Discord provides PCM audio, Whisper needs MP3/WAV
- **Solution**: Use pydub to convert formats, or save as WAV with wave library

### Challenge 2: Async Audio Processing
- **Issue**: Audio capture and API calls must not block bot
- **Solution**: Use asyncio tasks, create background workers for processing

### Challenge 3: Memory Management
- **Issue**: Audio buffers can consume significant memory
- **Solution**: Process in chunks, clear buffers after transcription, use temporary files

### Challenge 4: Voice State Synchronization
- **Issue**: Tracking who's speaking and when
- **Solution**: Use discord.py voice state events, implement user session tracking

### Challenge 5: FFmpeg Integration
- **Issue**: FFmpeg must be installed and accessible
- **Solution**: Check FFmpeg availability at startup, provide clear error messages

### Python Code Example: Audio Capture
```python
import discord
import asyncio
import io
from pydub import AudioSegment

class AudioSink(discord.sinks.Sink):
    def __init__(self):
        super().__init__()
        self.audio_data = {}
    
    def write(self, data, user):
        if user not in self.audio_data:
            self.audio_data[user] = []
        self.audio_data[user].append(data)
    
    async def process_audio(self, user_id):
        # Convert PCM to format for Whisper
        audio_bytes = b''.join(self.audio_data[user_id])
        # Process with OpenAI Whisper
        # Return transcribed text
```

## Environment Variables Needed
```
DISCORD_BOT_TOKEN=your_discord_token
OPENAI_API_KEY=your_openai_key
GUILD_ID=your_server_id (optional)
MAX_CONTEXT_LENGTH=10
TTS_VOICE=alloy (or preferred voice)
```

## Estimated Costs
- **Discord Bot**: Free
- **OpenAI Whisper API**: ~$0.006 per minute of audio
- **OpenAI GPT-4**: ~$0.03 per 1K tokens (input), $0.06 per 1K tokens (output)
- **OpenAI TTS**: ~$15 per 1M characters
- **Hosting**: $5-20/month (VPS or cloud hosting)

## Testing Strategy
1. Test bot connection and basic commands
2. Test voice channel join/leave
3. Test speech recognition with clear audio
4. Test AI responses for accuracy and relevance
5. Test TTS quality and clarity
6. Test full conversation loops
7. Load testing with multiple users
8. Edge case testing (poor audio, multiple speakers, etc.)

## Deployment Options (Python)
- **Local Development**: Run on personal computer during development
- **VPS**: DigitalOcean, Linode, AWS EC2 with Ubuntu/Debian
- **Cloud Platform**: Heroku, Railway, Render, PythonAnywhere
- **Docker**: Containerize with Dockerfile for easy deployment
- **Dedicated**: For production with high usage

### Docker Deployment (Recommended)
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg libopus0 libffi-dev libnacl-dev

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "bot.py"]
```

### Keeping Bot Running
- **systemd service** (Linux servers)
- **screen/tmux** (simple solution)
- **PM2** (process manager)
- **Docker with restart policy**
- **Cloud platform's built-in process management**

## Next Steps (Python Development)
1. Set up Python 3.9+ virtual environment
2. Install system dependencies (FFmpeg, libopus, etc.)
3. Create Discord application and obtain bot token
4. Set up OpenAI account and obtain API key
5. Create basic project structure with files outlined above
6. Start with Phase 1: Basic bot that responds to text commands
7. Progress through phases, testing each component
8. Iterate based on testing feedback

### Quick Start Commands
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install discord.py[voice] openai pydub python-dotenv

# Create .env file
echo "DISCORD_BOT_TOKEN=your_token_here" > .env
echo "OPENAI_API_KEY=your_key_here" >> .env

# Run bot
python bot.py
```