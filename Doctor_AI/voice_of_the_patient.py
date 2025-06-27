#step1 : Setup Audio recorder (ffmpeg & portaudio)

import os
import logging
import httpx
from groq import Groq
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Explicitly create an httpx client that does NOT trust the environment's proxy settings.
# This is a robust way to avoid proxy-related issues inside Docker.
transport = httpx.HTTPTransport(retries=2)
http_client = httpx.Client(transport=transport, trust_env=False)

client = Groq(
    api_key=GROQ_API_KEY,
    http_client=http_client,
)

def transcribe_with_groq(audio_path):
    """
    Transcribes the given audio file using the Groq API.
    """
    stt_model = "whisper-large-v3"
    if not GROQ_API_KEY:
        logger.error("GROQ_API_KEY not found.")
        return "ERROR: Groq API key is not configured."

    if not audio_path or not os.path.exists(audio_path):
        logger.warning(f"No audio path provided or file does not exist: {audio_path}")
        return "ERROR: No audio file submitted or file not found."

    try:
        with open(audio_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(audio_path), file.read()),
                model=stt_model,
            )
        logger.info("Transcription successful.")
        return transcription.text
    except Exception as e:
        logger.error(f"An error occurred during transcription: {e}")
        return f"ERROR: An error occurred during transcription: {e}"

# Test the complete workflow
if __name__ == "__main__":
    try:
        audio_filepath="patient_voice_test_for_patient.wav"
        
        # Transcribe the recorded audio
        patient_text = transcribe_with_groq(audio_filepath)
        
        if patient_text:
            print(f"\nPatient said: {patient_text}")
        else:
            print("Failed to transcribe audio")
            
    except FileNotFoundError:
        print(f"Audio file {audio_filepath} not found. Make sure recording completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

