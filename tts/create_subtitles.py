import assemblyai as aai
import os
from dotenv import load_dotenv

load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def transcribe_mp3(filepath, filename):
    transcript = aai.Transcriber().transcribe(filepath)
    subtitles = transcript.export_subtitles_srt()

    with open(f"./data/subtitles/{filename}.srt", "a") as out:
        out.write(subtitles)


transcribe_mp3("./data/audio/output_pytts_0.mp3", "output_pytts_0")