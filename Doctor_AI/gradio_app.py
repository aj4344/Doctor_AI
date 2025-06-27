#voiceBot UI with Gradio
import gradio as gr
import os
import time
import shutil
from pathlib import Path

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import get_doctor_voice_for_ui

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




def process_input(audio_filepath, image_filepath):
    """
    Process the patient's audio and image inputs and generate a doctor's response
    
    Args:
        audio_filepath: Path to the patient's audio recording
        image_filepath: Path to the patient's uploaded image
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


def show_loading():
    """Show the loading indicators while processing"""
    return gr.update(visible=True), gr.update(visible=False)


def hide_loading():
    """Hide the loading indicators after processing"""
    return gr.update(visible=False), gr.update(visible=True, elem_classes="fade-in")


# Create the Gradio interface with the new modern UI
with gr.Blocks(head='<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">') as iface:
    gr.Markdown("# MedMind AI: Virtual Doctor with Eyes and Ears")
    with gr.Row(elem_classes="main-container"):
        # Left Panel for Patient Inputs
        with gr.Column(elem_classes="patient-panel"):
            gr.HTML("""<div class="panel-header"><i class="fa-solid fa-user-plus"></i>Patient Input</div>
                       <p class="panel-subheader">Describe your symptoms and upload a medical image.</p>""")
            
            with gr.Column(elem_classes="input-group"):
                gr.Markdown("**1. Describe your symptoms**", elem_classes="label")
                audio_input = gr.Microphone(
                    type="filepath",
                    label="Record Your Symptoms (Click the microphone)",
                    elem_id="audio_input"
                )
            
            with gr.Column(elem_classes="input-group"):
                gr.Markdown("**2. Upload a clear medical image**", elem_classes="label")
                image_input = gr.Image(
                    type="filepath",
                    label="Upload image for diagnosis",
                    elem_classes="image-uploader"
                )

            submit_btn = gr.Button(
                "Get Doctor's Diagnosis",
                elem_classes="submit-button"
            )

        # Right Panel for Doctor's Consultation
        with gr.Column(elem_classes="doctor-panel"):
            with gr.Group(visible=False, elem_classes="loading-overlay") as loading_indicator:
                gr.HTML("""<div class="loading-spinner"></div>
                           <p class="loading-text">Consulting with Dr. AI...</p>""")

            with gr.Column(visible=True, elem_classes="results-container") as results_container:
                gr.HTML("""<div class="panel-header"><i class="fa-solid fa-stethoscope"></i>Doctor's Consultation</div>
                           <p class="panel-subheader">Review the analysis and listen to the audio consultation.</p>""")
                
                with gr.Column(elem_classes="results-content"):
                    with gr.Group(elem_classes="analyzed-image-container"):
                        gr.Markdown("**Analyzed Image**")
                        analyzed_image = gr.Image(label="", elem_classes="analyzed-image")
                    
                    with gr.Group(elem_classes="transcribed-text"):
                        gr.Markdown("**Your Symptoms (Transcribed)**")
                        speech_output = gr.Textbox(label="", lines=2)
                    
                    with gr.Group(elem_classes="doctor-analysis"):
                        gr.Markdown("**Doctor's Analysis**")
                        doctor_response = gr.Textbox(label="", lines=8)
                    
                    with gr.Group(elem_classes="audio-consultation"):
                        gr.Markdown("**Audio Consultation**")
                        voice_output = gr.Audio(label="", autoplay=True)

    # Event handlers for UI interactions
    submit_btn.click(
        fn=show_loading,
        outputs=[loading_indicator, results_container],
    ).then(
        fn=process_input,
        inputs=[audio_input, image_input],
        outputs=[speech_output, doctor_response, voice_output, analyzed_image],
    ).then(
        fn=hide_loading,
        outputs=[loading_indicator, results_container],
    )

# Launch the app
if __name__ == "__main__":
    try:
        iface.launch(
            debug=True,
            share=False,
            inbrowser=True,
            server_name="0.0.0.0",
            server_port=7860
        )
    finally:
        # Clean up any temporary files on exit
        print("Cleaning up temporary files...")