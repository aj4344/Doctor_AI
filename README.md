MedMind AI: Virtual Doctor with Eyes and Ears
MedMind AI Screenshot
![Screenshot 2025-06-27 173018](https://github.com/user-attachments/assets/f75515ae-1c48-43eb-aefa-c445a30e29e1)


Overview
MedMind AI is a sophisticated, interactive web application that simulates a consultation with a medical professional. It leverages cutting-edge multimodal AI to analyze medical images and spoken symptoms, providing users with a preliminary analysis and spoken feedback in a natural, deep male voice.

This project is designed to be a proof-of-concept for how AI can be used to create more engaging, accessible, and "human-like" digital health experiences. The user interface is built to be modern, professional, and intuitive, mimicking the look and feel of a high-end medical application.

Features
Modern & Professional UI: A sleek, hospital-themed interface built with Gradio, featuring custom CSS for a polished user experience.
Voice & Image Input: Users can record their symptoms using their microphone and upload a relevant medical image (e.g., a skin rash, an X-ray).
AI-Powered Transcription: Utilizes Groq's ultra-fast Whisper-large-v3 model to accurately transcribe the user's spoken symptoms.
Multimodal Analysis: Employs a powerful multimodal language model (meta-llama/llama-4-scout-17b-16e-instruct) to analyze both the transcribed text and the uploaded image simultaneously for a comprehensive understanding.
Realistic Voice Output: Generates a doctor's response using Edge-TTS with a highly customized, deep, and professional-sounding male voice (en-US-GuyNeural). Includes a fallback to gTTS for reliability.
Dynamic & Interactive: The entire experience is dynamic, from the loading animations to the autoplaying audio response, making the consultation feel more real.
Clean & Organized Code: The project is structured into logical modules for the UI (gradio_app.py), the AI brain (brain_of_the_doctor.py), and the voice components (voice_of_the_doctor.py, voice_of_the_patient.py).
How It Works
Patient Input: The user records their symptoms and uploads a medical image through the Gradio web interface.
Speech-to-Text: The recorded audio is sent to the Groq API and transcribed into text.
Image Encoding: The uploaded image is converted into a base64-encoded string.
AI Analysis: The transcribed text and the encoded image are sent to the multimodal LLM with a detailed system prompt that instructs the AI to act as a professional doctor.
Text Response: The AI generates a concise, paragraph-style analysis and recommendation.
Text-to-Speech: The AI's text response is passed to the Edge-TTS engine, which generates a high-quality MP3 audio file using the pre-configured deep male voice.
Display Results: The UI is updated to display the transcribed symptoms, the doctor's text analysis, the original image, and automatically plays the doctor's spoken response.
Tech Stack & Dependencies
UI: Gradio
AI/ML: Groq (for LLM and Whisper), SpeechRecognition
TTS: Edge-TTS, gTTS
Audio: PyAudio, playsound
Configuration: python-dotenv
All dependencies are listed in the requirements.txt file.

Setup and Installation
Follow these steps to run the Doctor AI project locally.

1. Clone the Repository
git clone https://github.com/aj4344/Doctor_AI.git
cd Doctor_AI
2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Install all the required Python packages using the requirements.txt file.

pip install -r requirements.txt
4. Set Up Environment Variables
The application requires an API key from Groq to function.

Create a file named .env in the root directory of the project.

Add your Groq API key to the file like this:

GROQ_API_KEY="YOUR_API_KEY_HERE"
Usage
Once the setup is complete, you can launch the application by running the gradio_app.py script.

python gradio_app.py
The application will start, and you can access it in your web browser at the local URL provided (usually http://127.0.0.1:7860).

Docker Deployment
You can also build and run the application using Docker for a consistent and isolated environment.

Option 1: Using Docker Commands
The most straightforward method is to use standard Docker commands:

# Build the Docker image
docker build -t medmind-ai .

# Run the Docker container
docker run --rm -it -p 7860:7860 --env-file .env medmind-ai
Option 2: Using Docker Compose (Requires Docker Compose installation)
If you have Docker Compose installed, you can use these simpler commands:

# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
Note: If you get an error like "'docker-compose' is not recognized", you need to install Docker Compose first. It comes bundled with Docker Desktop for Windows.

If you prefer using Docker commands directly:

# Build the Docker image
docker build -t doctor-ai .

# Run the Docker container
docker run --rm -it -p 7860:7860 --env-file .env doctor-ai
Web Platform Deployment
Doctor AI can be deployed to various web platforms:

Deploying to Hugging Face Spaces
Create a new Space on Hugging Face (https://huggingface.co/spaces)
Select Gradio as the SDK
Upload all project files (including .dockerignore and Dockerfile)
Add your GROQ_API_KEY as a secret in the Space settings
The Space will automatically build and deploy your application
Deploying to Render
Sign up for a Render account (https://render.com)
Create a new Web Service
Connect your GitHub repository
Configure as a Docker service
Add the GROQ_API_KEY as an environment variable
Deploy the application
Project Structure
.d_MLDL-Pro_Doctor_AI/
├── audio_outputs/ # Directory for generated audio files
├── .env # Stores API keys and other secrets
├── brain_of_the_doctor.py # Handles image encoding and LLM analysis
├── gradio_app.py # Main application file, defines the Gradio UI
├── README.md # This file
├── requirements.txt # Python dependencies
├── voice_of_the_doctor.py # Handles Text-to-Speech (TTS) generation
└── voice_of_the_patient.py # Handles audio recording and Speech-to-Text (STT)
Customization
You can easily customize the doctor's voice by modifying the configuration variables at the top of the voice_of_the_doctor.py file:

DOCTOR_VOICE: Change the voice model (e.g., "en-GB-RyanNeural").
VOICE_RATE, VOICE_PITCH, VOICE_VOLUME: Adjust the speed, pitch, and volume of the voice.
