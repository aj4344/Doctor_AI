import gradio as gr
import os
import time
from dotenv import load_dotenv

# Attempt to load environment variables from .env if present
load_dotenv()

# Import core functions from other modules
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import get_doctor_voice_for_ui

# --- Configuration ---
# Create a dedicated folder for audio outputs
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# System prompt for the doctor
system_prompt ="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 5 sentences). No preamble, start your answer right away please"""


# --- Core Processing Logic ---
def process_input(audio_filepath, image_filepath):
    """
    Process the patient's audio and image inputs and generate a doctor's response
    """
    # Create a timestamp for unique filenames
    timestamp = int(time.time())
    
    # Ensure we have valid inputs
    if not audio_filepath:
        return "No audio input detected.", "Please record your question for the doctor. I need to hear your symptoms to provide an assessment.", None, None

    if not image_filepath:
        return "Audio detected, but no image uploaded.", "I need both your audio description and a medical image to provide an accurate diagnosis. Please upload an image for me to analyze.", None, None
    
    # Convert patient's speech to text
    try:
        speech_to_text_output = transcribe_with_groq(audio_filepath)
    except Exception as e:
        print(f"Error transcribing speech: {e}")
        speech_to_text_output = "Error transcribing your speech. Please try again."
    
    # Handle the image input and generate doctor's response
    try:
        if image_filepath:
            doctor_response = analyze_image_with_query(
                query=system_prompt + speech_to_text_output,
                encoded_image=encode_image(image_filepath),
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
        else:
            doctor_response = "No image provided for me to analyze. Please upload an image for a proper diagnosis."
    except Exception as e:
        print(f"Error generating doctor response: {e}")
        doctor_response = "I apologize, but I encountered an error while analyzing your image. Please try again."
    
    # Generate the doctor's voice response using our deep male voice
    try:
        # Create a unique filename for this response
        audio_output_path = os.path.join(OUTPUT_DIR, f"doctor_response_{timestamp}.mp3")
        
        # Generate the voice
        get_doctor_voice_for_ui(
            text=doctor_response,
            output_filepath=audio_output_path
        )
        
        # Check if file was created successfully
        if os.path.exists(audio_output_path):
            return speech_to_text_output, doctor_response, audio_output_path, image_filepath
        else:
            print("Warning: Audio file not created")
            return speech_to_text_output, doctor_response, None, image_filepath
            
    except Exception as e:
        print(f"Error generating voice: {e}")
        return speech_to_text_output, doctor_response, None, image_filepath

# Create the Gradio interface
def create_gradio_interface():
    """Creates and returns the Gradio interface for MedMind AI"""
    
    # CSS for styling
    css = """
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; }
    .main-container { display: flex; flex-direction: row; gap: 2rem; padding: 1rem; }
    .panel { border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); padding: 1.5rem; background-color: white; flex: 1; }
    .panel-header { font-size: 1.5rem; font-weight: 600; color: #1a73e8; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem; }
    .panel-subheader { font-size: 0.9rem; color: #5f6368; margin-bottom: 1.5rem; }
    .input-group { margin-bottom: 1.5rem; }
    .label { font-weight: 500; margin-bottom: 0.5rem; }
    #audio_input, .image-uploader { border: 2px dashed #d0d0d0; border-radius: 8px; }
    .submit-button { background-color: #1a73e8 !important; color: white !important; font-weight: 600 !important; border-radius: 8px !important; padding: 0.75rem 1.5rem !important; }
    """
    
    with gr.Blocks(css=css) as iface:
        gr.Markdown("# MedMind AI: Virtual Doctor with Eyes and Ears")
        
        with gr.Row(elem_classes="main-container"):
            # Left Panel for Patient Inputs
            with gr.Column(elem_classes="panel"):
                gr.HTML("""<div class="panel-header">🧑‍⚕️ Patient Input</div>
                           <p class="panel-subheader">Record your symptoms and upload a medical image.</p>""")
                
                with gr.Column(elem_classes="input-group"):
                    gr.Markdown("**1. Record your symptoms**", elem_classes="label")
                    audio_input = gr.Audio(
                        sources=["microphone", "upload"],
                        type="filepath",
                        label="Record or upload your symptoms",
                        elem_id="audio_input"
                    )
                
                with gr.Column(elem_classes="input-group"):
                    gr.Markdown("**2. Upload a clear medical image**", elem_classes="label")
                    image_input = gr.Image(
                        type="filepath",
                        label="Upload image for diagnosis",
                        elem_classes="image-uploader"
                    )
                
                submit_btn = gr.Button("Get Doctor's Diagnosis", elem_classes="submit-button")
            
            # Right Panel for Doctor's Consultation
            with gr.Column(elem_classes="panel"):
                gr.HTML("""<div class="panel-header">👨‍⚕️ Doctor's Consultation</div>
                           <p class="panel-subheader">Review the analysis and listen to the audio consultation.</p>""")
                
                with gr.Column():
                    gr.Markdown("**Analyzed Image**")
                    analyzed_image = gr.Image(label="")
                    
                    gr.Markdown("**Your Symptoms (Transcribed)**")
                    speech_output = gr.Textbox(label="", lines=3)
                    
                    gr.Markdown("**Doctor's Analysis**")
                    doctor_response = gr.Textbox(label="", lines=5)
                    
                    gr.Markdown("**Audio Consultation**")
                    voice_output = gr.Audio(label="", autoplay=True)
        
        # Event handlers
        submit_btn.click(
            fn=process_input,
            inputs=[audio_input, image_input],
            outputs=[speech_output, doctor_response, voice_output, analyzed_image]
        )
        
    return iface

# Create and launch the interface
demo = create_gradio_interface()

# Launch with share enabled for Hugging Face Spaces
if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0")
else:
    # This is the part used by Hugging Face Spaces
    app = demo
