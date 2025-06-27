"""
Doctor AI Voice System Test Script
=================================
This script tests if the doctor voice system is working correctly.

IMPORTANT NOTE: The current implementation uses a pre-recorded
voice file (test_male_prabhat.mp3) that contains a single greeting
message. No matter what text is provided, it will always play the
same voice recording. This is by design to ensure a consistent,
high-quality doctor voice.

This script tests:
1. File existence
2. Audio playback capabilities 
3. The Gradio UI integration
"""

import os
import sys
import time
from colorama import init, Fore, Style
init()  # Initialize colorama for colored output

# Import the doctor voice system
try:
    from voice_of_the_doctor import speak_as_doctor, get_doctor_voice_for_ui, DEFAULT_DOCTOR_VOICE, VOICE_CONTENT
    print(f"{Fore.GREEN}✓ Successfully imported the doctor voice module{Style.RESET_ALL}")
except ImportError as e:
    print(f"{Fore.RED}✗ Failed to import the doctor voice module: {e}{Style.RESET_ALL}")
    sys.exit(1)

def print_header(text):
    """Prints a formatted header for test sections"""
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{text.center(70)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

def test_file_existence():
    """Tests if the required voice file exists"""
    print_header("Testing Voice File Existence")
    
    # Get the path to the voice file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    voice_file_path = os.path.join(script_dir, DEFAULT_DOCTOR_VOICE)
    
    # Check if the file exists
    if os.path.exists(voice_file_path):
        file_size_mb = os.path.getsize(voice_file_path) / (1024 * 1024)
        print(f"{Fore.GREEN}✓ Found voice file: {DEFAULT_DOCTOR_VOICE} ({file_size_mb:.2f} MB){Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}✗ Voice file not found: {voice_file_path}{Style.RESET_ALL}")
        print(f"  Please ensure '{DEFAULT_DOCTOR_VOICE}' exists in the folder: {script_dir}")
        return False

def test_voice_playback():
    """Tests the pre-recorded voice playback"""
    print_header("Testing Pre-recorded Voice Playback")
    
    print(f"{Fore.YELLOW}IMPORTANT: This system uses a pre-recorded voice file.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}No matter what text is provided, it will always play the same greeting:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}\"{VOICE_CONTENT}\"{Style.RESET_ALL}")
    print("\nLet's play the pre-recorded voice once to verify it works:")
    
    input("\nPress Enter to play the doctor's voice...")
    
    success = speak_as_doctor("This is a test message (will be spoken as pre-recorded greeting)")
    
    if success:
        print(f"\n{Fore.GREEN}✓ Voice playback test passed!{Style.RESET_ALL}")
        return True
    else:
        print(f"\n{Fore.RED}✗ Voice playback test failed!{Style.RESET_ALL}")
        return False

def test_gradio_integration():
    """Tests the Gradio UI integration function"""
    print_header("Testing Gradio UI Integration")
    
    test_output_path = "gradio_test_output.mp3"
    test_phrase = "This is a test of the Gradio UI integration."
    
    print(f"Testing UI voice function with output to {test_output_path}")
    print(f"{Fore.YELLOW}Note: This will also play the pre-recorded greeting.{Style.RESET_ALL}")
    
    try:
        # Test the UI function
        output_path = get_doctor_voice_for_ui(test_phrase, test_output_path)
        
        if os.path.exists(output_path):
            print(f"{Fore.GREEN}✓ Audio file for UI successfully created at: {output_path}{Style.RESET_ALL}")
            
            # Clean up
            try:
                os.remove(output_path)
                print(f"{Fore.GREEN}✓ Test file cleaned up{Style.RESET_ALL}")
            except:
                print(f"{Fore.YELLOW}! Could not clean up test file{Style.RESET_ALL}")
                
            return True
        else:
            print(f"{Fore.RED}✗ Failed to create audio file for UI{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}✗ Error during UI integration test: {e}{Style.RESET_ALL}")
        return False

def main():
    print_header("DOCTOR AI VOICE SYSTEM TEST")
    
    print(f"{Fore.YELLOW}IMPORTANT NOTE: This doctor voice system uses a pre-recorded voice file.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}It will always play the same greeting message regardless of the text input.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}This is by design to ensure consistent, high-quality voice output.{Style.RESET_ALL}")
    
    # Test file existence first
    if not test_file_existence():
        print(f"{Fore.RED}Cannot continue testing without the voice file.{Style.RESET_ALL}")
        return
    
    # Test voice playback
    voice_test_passed = test_voice_playback()
    
    # Test Gradio integration
    gradio_test_passed = test_gradio_integration()
    
    print_header("TEST RESULTS")
    print(f"Voice playback test: {'PASSED' if voice_test_passed else 'FAILED'}")
    print(f"Gradio UI integration test: {'PASSED' if gradio_test_passed else 'FAILED'}")
    
    if voice_test_passed and gradio_test_passed:
        print(f"\n{Fore.GREEN}All tests passed! The Doctor AI voice system is working correctly.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}Some tests failed. Please check the issues above.{Style.RESET_ALL}")
    
    print("\nOptions for the future:")
    print(f"{Fore.CYAN}1. Keep using the pre-recorded greeting (current implementation){Style.RESET_ALL}")
    print(f"{Fore.CYAN}2. Record multiple phrases with the Prabhat voice and use them selectively{Style.RESET_ALL}")
    print(f"{Fore.CYAN}3. Use gTTS to generate dynamic responses (but lower voice quality){Style.RESET_ALL}")

if __name__ == "__main__":
    main()
