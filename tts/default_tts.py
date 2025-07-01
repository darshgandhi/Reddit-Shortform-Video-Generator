import pyttsx3
import pandas as pd
import os

# Load Excel data
df = pd.read_excel("./data/output.xlsx", engine="openpyxl")
list_items = df.values.tolist()

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Set voice
voices = engine.getProperty('voices')
for voice in voices:
    if "male" in voice.name.lower() or "david" in voice.name.lower() or "alex" in voice.name.lower():
        male_voice_id = voice.id
        break

# Rate and volume
engine.setProperty('rate', 180)
engine.setProperty('volume', 0.9)

# Generate audio files for each row
for idx, post in enumerate(list_items):
    text = " ".join(str(x) for x in post)

    filename = f"./data/audio/output_pytts_{idx}.mp3"
    
    # Save to file
    engine.save_to_file(text, filename)
    print(f"Saved {filename}")

# Finalize the engine
engine.runAndWait()