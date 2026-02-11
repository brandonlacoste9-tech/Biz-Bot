from typing import Optional
import httpx
from app.core.config import settings


class ElevenLabsService:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.base_url = "https://api.elevenlabs.io/v1"

    async def text_to_speech(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> Optional[bytes]:
        """Convert text to speech using ElevenLabs API"""
        if not self.api_key:
            print("ElevenLabs API key not configured. Skipping text-to-speech.")
            return None
        
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data, headers=headers)
                if response.status_code == 200:
                    return response.content
                else:
                    print(f"ElevenLabs API error: {response.status_code} - {response.text}")
                    return None
        except Exception as e:
            print(f"Error calling ElevenLabs API: {e}")
            return None


elevenlabs_service = ElevenLabsService()
