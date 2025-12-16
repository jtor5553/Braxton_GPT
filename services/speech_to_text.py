"""Speech-to-text service using OpenAI Whisper API."""
import io
from openai import OpenAI
from utils.config import Config


class SpeechToText:
    """Handles speech-to-text conversion using OpenAI Whisper."""
    
    def __init__(self):
        """Initialize OpenAI client for Whisper."""
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    async def transcribe_audio(self, audio_data: bytes, format: str = "wav") -> str:
        """
        Transcribe audio data to text using Whisper API.
        
        Args:
            audio_data: Raw audio bytes
            format: Audio format (wav, mp3, etc.)
            
        Returns:
            Transcribed text
        """
        try:
            # Create a file-like object from bytes
            audio_file = io.BytesIO(audio_data)
            audio_file.name = f"audio.{format}"
            
            # Transcribe using Whisper
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
            
            return transcript.text
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return ""

