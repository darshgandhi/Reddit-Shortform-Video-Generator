from google.cloud import texttospeech
import os
from dotenv import load_dotenv
import pandas as pd

# Get data from output.xlsx and convert to list
df = pd.read_excel("./data/output.xlsx", engine="openpyxl")
list_items = df.values.tolist()

# Set up Google Cloud client
load_dotenv()
gc_details_tts_path = os.getenv("GC_DETAILS_TTS_PATH")
if gc_details_tts_path is None:
    raise EnvironmentError("GC_DETAILS_TTS_PATH is not set. Please check your .env or environment variables.")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gc_details_tts_path
client = texttospeech.TextToSpeechClient()

voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Wavenet-D"
)


audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

for idx, post in enumerate(list_items):
    synthesis_input = texttospeech.SynthesisInput(text=" ".join(str(x) for x in post))
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    with open(f"./data/audio/output_{idx}.mp3", "wb") as out:
        out.write(response.audio_content)
