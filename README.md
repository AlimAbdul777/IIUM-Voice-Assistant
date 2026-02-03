# Mira: IIUM KOE AI Voice Assistant
Mira is an AI-driven voice assistant specifically customized for the IIUM Kulliyyah of Engineering (KOE). This project was developed as part of the Natural Language Processing (SEM12526) course to demonstrate a complete speech-to-speech pipeline.

## 🚀 Features

Speech-to-Text (STT): High-accuracy transcription using the Whisper-large-v3 model via Groq API.


NLP Engine: Intelligent response generation powered by Llama-3.1-8b-instant.


Domain Customization: Local knowledge integration through a specialized FAQ and knowledge base (knowledge.txt).


Text-to-Speech (TTS): Natural human-like voice responses using Microsoft Edge-TTS (en-US-AriaNeural).


Local Action Handling: Real-time system queries for date and time.

## 🛠️ System Architecture
The assistant operates on a modular pipeline:

Input: Captures user audio via the SpeechRecognition library.

Transcription: Converts audio to text using Whisper.


Processing: Llama 3.1 processes the text using a system prompt that includes the local KOE knowledge base.

Output: Generates and plays back speech via edge-tts and pygame.

<img width="970" height="559" alt="image" src="https://github.com/user-attachments/assets/d98af2c3-b372-4bf1-bee8-b3911037ac69" />

## 📂 Project Structure

main.py: The core application script managing the pipeline and API calls.


knowledge.txt: A customized knowledge base containing KOE-specific data such as lab locations, staff contacts, and academic rules .


requirements.txt: List of Python dependencies required to run the project.

## ⚙️ Installation & Setup
Clone the repository:

Bash
git clone https://github.com/AlimAbdul777/IIUM-Voice-Assistant.git
cd IIUM-Voice-Assistant

Install dependencies: 

Bash
pip install -r requirements.txt
Configure API Key: Open main.py and replace the GROQ_API_KEY placeholder with your valid Groq API key.

## 🎙️ Usage
Run the assistant using the following command: 

Bash
python main.py
Once active, you can ask Mira about:


Lab Locations: "Where is the Robotics Lab?".


Faculty Contacts: "Who is the Head of Mechatronics?".


Academic Rules: "What is the penalty for late assignments?".


Facility Info: "Where is the surau in KOE?".


## 📄 License
This project is for educational purposes as part of the IIUM NLP Course Project.

Would you like me to help you draft a specific "How to Run" guide for your classmates who might not have Python experience?


