"""Audio capture and processing utilities."""
import discord
import io
import wave
from typing import Dict, List


class AudioSink(discord.sinks.Sink):
    """Custom audio sink for capturing Discord voice audio."""
    
    def __init__(self):
        """Initialize audio sink with storage for user audio data."""
        super().__init__()
        self.audio_data: Dict[int, List[bytes]] = {}
    
    def write(self, data: bytes, user: discord.Member):
        """
        Write audio data from a user.
        
        Args:
            data: PCM audio data
            user: Discord member who is speaking
        """
        user_id = user.id if user else 0
        if user_id not in self.audio_data:
            self.audio_data[user_id] = []
        self.audio_data[user_id].append(data)
    
    def get_audio_for_user(self, user_id: int) -> bytes:
        """
        Get concatenated audio data for a specific user.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            Combined audio bytes
        """
        if user_id not in self.audio_data:
            return b""
        return b"".join(self.audio_data[user_id])
    
    def clear_user_audio(self, user_id: int):
        """Clear audio data for a specific user."""
        if user_id in self.audio_data:
            del self.audio_data[user_id]
    
    def clear_all(self):
        """Clear all audio data."""
        self.audio_data.clear()


def convert_pcm_to_wav(pcm_data: bytes, sample_rate: int = 48000, channels: int = 2) -> bytes:
    """
    Convert PCM audio data to WAV format.
    
    Args:
        pcm_data: Raw PCM audio bytes
        sample_rate: Audio sample rate (default 48000 for Discord)
        channels: Number of audio channels (default 2 for stereo)
        
    Returns:
        WAV formatted audio bytes
    """
    wav_buffer = io.BytesIO()
    
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)  # 16-bit audio
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_data)
    
    wav_buffer.seek(0)
    return wav_buffer.read()

