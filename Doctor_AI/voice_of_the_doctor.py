# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

import asyncio
import edge_tts
from gtts import gTTS
import os

# Configuration for the doctor's voice
DOCTOR_VOICE = "en-US-GuyNeural"
VOICE_RATE = "-4%"
VOICE_PITCH = "+0Hz"
VOICE_VOLUME = "+0%"

async def _main_tts(text, output_filepath):
    """Asynchronous function to handle TTS generation."""
    try:
        # Attempt to use the high-quality Edge-TTS voice
        communicate = edge_tts.Communicate(text, DOCTOR_VOICE, rate=VOICE_RATE, pitch=VOICE_PITCH, volume=VOICE_VOLUME)
        await communicate.save(output_filepath)
        print(f"Successfully generated Edge TTS speech to {output_filepath}")
        return output_filepath, None
    except Exception as e:
        # If Edge-TTS fails, fall back to the more stable gTTS
        print(f"Error generating Edge TTS speech: {e}")
        print("Using gTTS fallback for speech generation.")
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_filepath)
            print(f"Successfully generated gTTS speech to {output_filepath}")
            return output_filepath, None
        except Exception as gtts_error:
            error_message = f"gTTS fallback also failed: {gtts_error}"
            print(error_message)
            return None, error_message

def text_to_speech(text, output_filepath):
    """
    Synchronous wrapper to run the async TTS function.
    This creates and manages the necessary asyncio event loop.
    """
    try:
        return asyncio.run(_main_tts(text, output_filepath))
    except Exception as e:
        error_message = f"An error occurred in the TTS process: {e}"
        print(error_message)
        return None, error_message

def generate_doctor_voice(text: str, output_filepath: str = "current_doctor_response.mp3"):
    """
    Generate speech using Edge TTS with a guaranteed deep male voice.
    
    Args:
        text (str): The text to convert to speech
        output_filepath (str): Where to save the generated audio
        
    Returns:
        str: Path to the generated audio file
    """
    output_path, error = text_to_speech(text, output_filepath)
    if error:
        print(f"Failed to generate speech: {error}")
    return output_path

def speak_as_doctor(text: str):
    """
    Makes the doctor speak with a deep male voice.
    
    Args:
        text (str): The text to be spoken
        
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"Doctor AI (Deep Male Voice): {text}")
    
    # Generate speech with Edge TTS
    output_path = generate_doctor_voice(text)
    
    if not output_path or not os.path.exists(output_path):
        print("Failed to generate doctor's voice.")
        return False
    
    try:
        # Play the generated speech
        from playsound import playsound
        playsound(output_path)
        return True
    except Exception as e:
        print(f"Error playing audio: {e}")
        return False

def get_doctor_voice_for_ui(text: str, output_filepath: str = "doctor_response.mp3"):
    """
    Generate speech for the doctor's response for the UI.
    Uses guaranteed deep male voice.
    
    Args:
        text (str): The text to be spoken
        output_filepath (str): The path where to save the file
        
    Returns:
        str: Path to the audio file for the UI
    """
    print(f"Generating doctor voice for UI: {text[:50]}...")
    
    # Generate speech with Edge TTS - don't play it automatically for UI
    output_path = generate_doctor_voice(text, output_filepath)
    
    if not output_path or not os.path.exists(output_path):
        print("Failed to generate doctor's voice for UI.")
        # Use a simple fallback in case of failure
        from gtts import gTTS
        try:
            audioobj = gTTS(text=text, lang="en", tld="co.uk", slow=True)
            audioobj.save(output_filepath)
            print(f"Used gTTS fallback for UI audio")
            return output_filepath
        except:
            print("All TTS methods failed.")
            return None
    
    return output_path

# --- Legacy functions for compatibility ---
def generate_speech(text: str, output_filepath: str):
    """Legacy function for compatibility"""
    return generate_doctor_voice(text, output_filepath)

def text_to_speech_with_gtts(input_text, output_filepath):
    """Legacy function for compatibility"""
    return generate_doctor_voice(input_text, output_filepath)

def text_to_speech_with_gtts_old(input_text, output_filepath):
    """Legacy function for compatibility"""
    return generate_doctor_voice(input_text, output_filepath)

# --- Main execution for testing ---
if __name__ == "__main__":
    test_message = "Hello, I am Doctor Jones. I will analyze your symptoms and provide medical advice based on what I see."
    print("\n=== Doctor AI Voice System Test ===")
    
    print("\nGenerating and playing doctor's voice:")
    speak_as_doctor(test_message)