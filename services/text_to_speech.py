"""Text-to-speech service using OpenAI TTS API."""
import io
from openai import OpenAI
from utils.config import Config


class TextToSpeech:
    """Handles text-to-speech conversion using OpenAI TTS."""
    
    def __init__(self):
        """Initialize OpenAI client for TTS."""
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.voice = Config.TTS_VOICE
    
    async def synthesize_speech(self, text: str) -> bytes:
        """
        Convert text to speech audio.
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Audio data as bytes (MP3 format)
        """
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=self.voice,
                input=text
            )
            
            # Read audio data
            audio_data = b""
            for chunk in response.iter_bytes():
                audio_data += chunk
            
            return audio_data
        except Exception as e:
            print(f"Error synthesizing speech: {e}")
            return b""

