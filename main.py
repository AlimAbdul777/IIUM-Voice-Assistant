import asyncio
import os
import time
import datetime
import speech_recognition as sr
from groq import Groq
import edge_tts
import pygame
from colorama import Fore, Style, init

# ==========================================
#  CONFIGURATION
# ==========================================
GROQ_API_KEY = "" 

ASSISTANT_NAME = "Mira"
VOICE = "en-US-AriaNeural"

# ==========================================
#  INITIALIZATION
# ==========================================
init(autoreset=True)
client = Groq(api_key=GROQ_API_KEY)
recognizer = sr.Recognizer()
pygame.mixer.init()

# ==========================================
#  TOOLS
# ==========================================
def get_current_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_current_date():
    return datetime.datetime.now().strftime("%A, %B %d, %Y")

def load_knowledge():
    try:
        with open("knowledge.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

# ==========================================
#  BRAIN (System Prompt)
# ==========================================
SYSTEM_PROMPT = f"""
You are {ASSISTANT_NAME}. 
CONTEXT: {load_knowledge()}

INSTRUCTIONS:
1. If asked for time, reply ONLY: "ACTION:TIME"
2. If asked for date, reply ONLY: "ACTION:DATE"
3. Otherwise, answer concisely (max 2 sentences).
"""

conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

# ==========================================
#  PIPELINE
# ==========================================
def listen():
    with sr.Microphone() as source:
        print(Fore.CYAN + f"\n[{ASSISTANT_NAME}] Listening... " + Style.RESET_ALL, end="", flush=True)
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            # Listens for 5 seconds max to keep it snappy
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            print(Fore.GREEN + "Done." + Style.RESET_ALL)
            with open("input.wav", "wb") as f:
                f.write(audio.get_wav_data())
            return "input.wav"
        except sr.WaitTimeoutError:
            print(Fore.RED + "\n[!] Silence." + Style.RESET_ALL)
            return None

def transcribe(file_path):
    if not file_path: return None
    try:
        with open(file_path, "rb") as file:
            return client.audio.transcriptions.create(
                file=(file_path, file.read()), 
                model="whisper-large-v3", 
                language="en"
            ).text
    except:
        return None

def think(user_text):
    print(Fore.YELLOW + f"User: {user_text}" + Style.RESET_ALL)
    conversation_history.append({"role": "user", "content": user_text})
    
    # FIX: Uses the NEW Llama 3.1 model
    chat = client.chat.completions.create(
        messages=conversation_history, 
        model="llama-3.1-8b-instant"
    )
    raw = chat.choices[0].message.content.strip()

    if "ACTION:TIME" in raw:
        reply = f"The time is {get_current_time()}."
    elif "ACTION:DATE" in raw:
        reply = f"Today is {get_current_date()}."
    else:
        reply = raw

    conversation_history.append({"role": "assistant", "content": reply})
    return reply

async def speak(text):
    print(Fore.CYAN + f"{ASSISTANT_NAME}: {text}" + Style.RESET_ALL)
    
    # FIX: Generates a unique filename (reply_12345.mp3) to avoid Permission Errors
    filename = f"reply_{int(time.time())}.mp3"
    
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)
    
    # Load and Play
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    # Wait until audio finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    # FIX: Unload and Delete the file to keep folder clean
    pygame.mixer.music.unload()
    try:
        os.remove(filename)
    except PermissionError:
        pass # If it fails to delete, just ignore it.

async def main():
    print(Fore.GREEN + f"--- {ASSISTANT_NAME} ONLINE ---" + Style.RESET_ALL)
    
    # Startup Sound (Optional)
    await speak("System online. I am ready.")
    
    while True:
        try:
            audio = listen()
            if audio:
                text = transcribe(audio)
                if text:
                    # Voice Command to Stop
                    if "exit" in text.lower() or "stop" in text.lower():
                        await speak("Shutting down. Goodbye.")
                        break
                    
                    resp = think(text)
                    await speak(resp)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())