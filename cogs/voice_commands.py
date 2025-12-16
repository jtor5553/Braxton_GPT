"""Voice channel commands and audio processing."""
import discord
from discord.ext import commands
from discord.sinks import MP3Sink
import asyncio
import io
import os
import tempfile
from services.speech_to_text import SpeechToText
from services.text_to_speech import TextToSpeech
from services.ai_handler import AIHandler
from utils.audio_processor import AudioSink, convert_pcm_to_wav
from utils.context_manager import ContextManager


class VoiceCommands(commands.Cog):
    """Cog for handling voice channel interactions."""
    
    def __init__(self, bot: commands.Bot):
        """Initialize voice commands cog."""
        self.bot = bot
        self.voice_clients: dict[int, discord.VoiceClient] = {}
        self.audio_sinks: dict[int, AudioSink] = {}
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.ai_handler = AIHandler()
        self.context_manager = ContextManager()
        self.processing_users = set()  # Track users currently being processed
    
    @commands.command(name="join")
    async def join_voice(self, ctx: commands.Context):
        """Join the voice channel of the command author."""
        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel!")
            return
        
        channel = ctx.author.voice.channel
        guild_id = ctx.guild.id
        
        # Leave existing connection if any
        if guild_id in self.voice_clients:
            await self.leave_voice(ctx)
        
        # Connect to voice channel
        try:
            vc = await channel.connect()
            self.voice_clients[guild_id] = vc
            
            # Create audio sink for capturing audio
            sink = AudioSink()
            self.audio_sinks[guild_id] = sink
            
            # Start recording with callback
            vc.start_recording(
                sink,
                self.on_audio_received,
                sync_start=False
            )
            
            # Start background task to process audio periodically
            self.bot.loop.create_task(self.process_audio_periodically(guild_id))
            
            await ctx.send(f"Joined {channel.name} and started listening!")
        except Exception as e:
            await ctx.send(f"Error joining voice channel: {e}")
    
    @commands.command(name="leave")
    async def leave_voice(self, ctx: commands.Context):
        """Leave the voice channel."""
        guild_id = ctx.guild.id
        
        if guild_id not in self.voice_clients:
            await ctx.send("I'm not in a voice channel!")
            return
        
        vc = self.voice_clients[guild_id]
        
        # Stop recording
        vc.stop_recording()
        
        # Disconnect
        await vc.disconnect()
        
        # Cleanup
        del self.voice_clients[guild_id]
        if guild_id in self.audio_sinks:
            del self.audio_sinks[guild_id]
        
        await ctx.send("Left the voice channel!")
    
    async def on_audio_received(self, sink: AudioSink, user: discord.Member):
        """
        Callback when audio is received from a user.
        This is called by discord.py when audio data is available.
        
        Args:
            sink: The audio sink
            user: The user who spoke
        """
        # This callback is mainly for notification
        # Actual processing happens in process_audio_periodically
        pass
    
    async def process_audio_periodically(self, guild_id: int):
        """
        Periodically process accumulated audio data.
        
        Args:
            guild_id: Guild ID to process audio for
        """
        while guild_id in self.voice_clients:
            try:
                await asyncio.sleep(3)  # Process every 3 seconds
                
                if guild_id not in self.audio_sinks:
                    continue
                
                sink = self.audio_sinks[guild_id]
                
                # Process audio for each user
                for user_id in list(sink.audio_data.keys()):
                    if user_id in self.processing_users:
                        continue
                    
                    audio_data = sink.get_audio_for_user(user_id)
                    
                    # Need sufficient audio data (at least 1 second)
                    if len(audio_data) < 48000 * 2:  # ~1 second of 48kHz stereo
                        continue
                    
                    # Process this user's audio
                    await self.process_user_audio(guild_id, user_id, audio_data)
                    sink.clear_user_audio(user_id)
                    
            except Exception as e:
                print(f"Error in audio processing loop: {e}")
                await asyncio.sleep(1)
    
    async def process_user_audio(self, guild_id: int, user_id: int, audio_data: bytes):
        """
        Process audio data for a specific user.
        
        Args:
            guild_id: Guild ID
            user_id: User ID
            audio_data: Raw PCM audio data
        """
        if user_id in self.processing_users:
            return
        
        self.processing_users.add(user_id)
        
        try:
            # Convert PCM to WAV for Whisper
            wav_data = convert_pcm_to_wav(audio_data)
            
            # Transcribe speech
            text = await self.stt.transcribe_audio(wav_data, format="wav")
            
            if not text or len(text.strip()) < 2:
                return
            
            print(f"Transcribed from user {user_id}: {text}")
            
            # Get user context
            context = self.context_manager.get_context(user_id)
            
            # Generate AI response
            response = await self.ai_handler.generate_response(text, context)
            
            # Update context
            self.context_manager.add_message(user_id, "user", text)
            self.context_manager.add_message(user_id, "assistant", response)
            
            # Convert response to speech
            audio_response = await self.tts.synthesize_speech(response)
            
            if not audio_response:
                return
            
            # Play audio response
            if guild_id in self.voice_clients:
                vc = self.voice_clients[guild_id]
                
                # Create temporary file for audio
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tmp_file.write(audio_response)
                    tmp_path = tmp_file.name
                
                try:
                    # Create audio source from file
                    audio_source = discord.FFmpegPCMAudio(tmp_path)
                    
                    # Wait if already playing
                    while vc.is_playing():
                        await asyncio.sleep(0.1)
                    
                    vc.play(audio_source)
                    
                    # Wait for playback to finish
                    while vc.is_playing():
                        await asyncio.sleep(0.1)
                    
                finally:
                    # Clean up temp file
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
            
        except Exception as e:
            print(f"Error processing audio for user {user_id}: {e}")
        finally:
            self.processing_users.discard(user_id)


async def setup(bot: commands.Bot):
    """Setup function for loading the cog."""
    await bot.add_cog(VoiceCommands(bot))

