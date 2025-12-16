# Quick Setup Checklist

Follow these steps to get your Discord voice bot running:

## ✅ Prerequisites Checklist

- [ ] Python 3.9+ installed (`python --version`)
- [ ] FFmpeg installed (`ffmpeg -version`)
- [ ] Discord Bot Token (from Discord Developer Portal)
- [ ] OpenAI API Key (from OpenAI Platform)

## 🚀 Setup Steps

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies (Pycord)
```bash
pip install -r requirements.txt
```

### 3. Install System Dependencies

**macOS:**
```bash
brew install ffmpeg opus
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg libopus0 libffi-dev libnacl-dev python3-dev
```

### 4. Create `.env` File

Create a `.env` file in the project root with:

```env
DISCORD_BOT_TOKEN=your_discord_token_here
OPENAI_API_KEY=your_openai_key_here
MAX_CONTEXT_LENGTH=10
TTS_VOICE=alloy
```

### 5. Invite Bot to Server

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your bot application
3. Go to OAuth2 > URL Generator
4. Select scopes: `bot`, `applications.commands`
5. Select permissions:
   - ✅ Connect
   - ✅ Speak
   - ✅ Use Voice Activity
   - ✅ Read Message History
   - ✅ Send Messages
6. Copy URL and open in browser to invite bot

### 6. Run the Bot
```bash
python bot.py
```

## 🧪 Test Commands

1. **Test connection:** `!botping` in Discord
2. **Test text chat:** `!ask hello`
3. **Join voice:** `!join` (while in a voice channel)
4. **Test voice:** Speak in the voice channel
5. **Leave voice:** `!leave`

## ❗ Common Issues

**"FFmpeg not found"**
- Install FFmpeg and ensure it's in your PATH
- Test with: `ffmpeg -version`

**"Invalid token"**
- Double-check your `.env` file
- Ensure token is copied correctly (no extra spaces)

**"Bot can't join voice"**
- Verify bot has "Connect" and "Speak" permissions
- Make sure you're in a voice channel when using `!join`

**"OpenAI API errors"**
- Check your API key is valid
- Verify you have API credits/quota
- Check rate limits

## 📝 Next Steps

- Customize AI prompts in `services/ai_handler.py`
- Adjust TTS voice in `.env` file
- Modify context length for conversation history
- Add custom commands in `cogs/` directory

